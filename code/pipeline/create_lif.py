"""create_lif.py

Convert Pubmed's nxml files into LIF files.

Usage:

$ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILE_LIST -b BEGIN -e END
$ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILE_LIST --crash
$ python3 create_lif.py (-h | --help)

The -s, -d and -f options are there to hand in the source directory to be
processed, the data directory to write results to and a file list with relative
file paths in SOURCE_DIR. SOURCE_DIR is as the pubmed central download and has
directories for each journal and nxml files in those directories. DATA_DIR is
assumed to be empty. A new directory DATA_DIR/lif will be created (if it exists,
contents may be overwritten) and after running this script the new directory
will have the same structure as SOURCE_DIR.

BEGIN and END refer to the line number in the FILE_LIST, only the files on the
lines starting at BEGIN and up to and including END will be processed. BEGIN and
END both default to 1 (in which case only the first file name will be processed).

The second invocation is like the first except that errors will not be trapped,
instead the code will exit with an error. For this example the -b and -e options
were omitted for space.

The third invocation prints a help message.

The following information is extracted:

- pubmed ids, both pmid and pmc
- titles
- abstract
- authors
- journal name
- publication year
- references (disabled at the moment)


== Top level article structure: front versus body versus back

There appears to be something wrong with these. In emacs they show up in
red. When I search inside of them nothing can be found.


== Title

There are two kinds of article-title and we only want the one in title-group,
not the ones in the citations.


== Abstracts

Some documents do not have abstracts, some have more than one. Some abstracts
aren't really the kinds of abstracts we want. Most abstracts tags do not have
any attributes (about 78% of a randomly selected sample of 1000 articles), but
some have an 'abstract-type' attribute (8%) and some have an 'id' attribute
(16%). All abstracts are children of the <article-meta> tag. For a list of the
abstract attributes see data-analysis/abstracts-01000.txt.

The following seem the be decent heuristics and they work for the random sample
of 1000:

- If you have only one abstract, go with it. This may include some fairly
  useless abstracts for some abstract types, but these do not seem to be
  harmful.

- If you have more than one abstract go for the one without an abstract-type
  property.


== References

We get the title, year, authors, pmid and source. References are ignored if
there is no year, title and authors.

References almost double processing time so I am leaving them out given our
current time crunch and the fact we did not use it last time for the Kibana
visualiation. Not doing this also reduces diskspace used by a factor 4.


== Runtime

Running this on 1000 random articles takes 90 seconds on a 2015 3.2GHz 32GB DDR3
iMac. The input is about 76Mb and the output about 4MB. For the full pmc (with
2M+ articles) it should take just over two days. If references are included
running time increases by about 65-70% and disk use quadruples.

"""


import os
import sys
import getopt
import bs4

import lif
from utils import ensure_directory, elements, time_elapsed, print_element


@time_elapsed
def process_filelist(source_dir, data_dir, filelist, start, end, crash=False):
    print("$ python3 %s\n" % ' '.join(sys.argv))
    for n, fname in elements(filelist, start, end):
        print_element(n, fname)
        if crash:
            process_list_element(source_dir, data_dir, fname)
        else:
            try:
                process_list_element(source_dir, data_dir, fname)
            except Exception as e:
                print("ERROR on %07d  %s\n" % (n, fname))
                print('ERROR:', Exception, e, '\n')


def process_list_element(source_dir, data_dir, fname):
    nxml_file = os.path.join(source_dir, fname)
    lif_file = os.path.join(data_dir, 'lif', fname[:-4] + 'lif')
    ensure_directory(lif_file)
    pmc_article = PmcArticle(nxml_file, lif_file)
    pmc_article.write()


class PmcArticle(object):

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.lif = lif.LIF()
        self.lif.metadata['authors'] = []
        self.lif.metadata['references'] = []
        with open(self.source) as fp:
            self.soup = bs4.BeautifulSoup(fp, 'lxml')
            self._add_ids()
            self._add_title()
            self._add_abstract()
            self._add_journal()
            self._add_authors()
            self._add_year()
            # self._add_references()

    @staticmethod
    def _get_text(tag):
        return tag.get_text().strip() if tag is not None else None

    def _set_metadata_field(self, field, tag):
        self.lif.metadata[field] = self._get_text(tag)

    def _add_ids(self):
        article_ids = self.soup.find_all('article-id')
        article_ids = [id for id in article_ids if id.parent.name == 'article-meta']
        for article_id in article_ids:
            if article_id.attrs.get('pub-id-type') == 'pmc':
                self._set_metadata_field('id-pmc', article_id)
            elif article_id.attrs.get('pub-id-type') == 'pmid':
                self._set_metadata_field('id-pmid', article_id)

    def _add_title(self):
        titles = self.soup.find_all('article-title')
        titles = [t for t in titles if t.parent.name == 'title-group']
        self.lif.metadata['title'] = self._get_text(titles[0]) if titles else None

    def _add_abstract(self):
        abstracts = self.soup.find_all('abstract')
        if len(abstracts) == 0:
            return None
        elif len(abstracts) == 1:
            abstract = abstracts[0]
        else:
            filtered_abstracts = [a for a in abstracts if a.attrs.get('abstract-type') is None]
            abstract = filtered_abstracts[0] if filtered_abstracts else abstracts[0]
        # Some abstracts have a section structure with headers like "background"
        # and "conclusion". Put the headers on their own line by inserting white
        # lines into the BeautifulSoup object.
        for p in abstract.find_all('p'):
            p.append("\n\n")
        for title in abstract.find_all('title'):
            title.append(".\n\n")
        self.lif.text.value = self._get_text(abstract)

    def _add_journal(self):
        titles = self.soup.find_all('journal-title')
        titles = [t for t in titles if t.parent.name == 'journal-title-group']
        self.lif.metadata['journal'] = titles[0].get_text() if titles else None

    def _add_authors(self):
        authors = self.soup.find_all('contrib')
        authors = [a for a in authors if a.parent.name == 'contrib-group']
        for author in authors:
            if author.attrs.get('contrib-type') == "author":
                first = self._get_text(author.find('given-names'))
                last = self._get_text(author.surname)
                self.lif.metadata['authors'].append(self._get_fullname(first, last))

    def _add_year(self):
        pubdates = self.soup.find_all('pub-date')
        pubdates = [pb for pb in pubdates if pb.parent.name == 'article-meta']
        self.lif.metadata['year'] = int(pubdates[0].year.get_text())

    def _add_references(self):
        refs = self.soup.find_all('ref')
        refs = [r for r in refs if r.parent.name == 'ref-list']
        for ref in refs:
            obj = { "authors": [], "year": None, "title": None, "source" : None, "pmid": None }
            year = ref.find('year')
            title = ref.find('article-title')
            source = ref.find('source')
            pmid = ref.find('pub-id')
            if year and title:
                obj['year'] = int(year.get_text()[:4])
                obj['title'] = title.get_text()
            if pmid is not None and pmid.attrs.get('pub-id-type') == 'pmid':
                obj['pmid'] =  pmid.get_text()
            obj['source'] = self._get_text(source)
            for n in ref.find_all('name'):
                first = self._get_text(n.find('given-names'))
                last = self._get_text(n.surname)
                obj['authors'].append(self._get_fullname(first, last))
            if year and title and obj['authors']:
                self.lif.metadata['references'].append(obj)

    @staticmethod
    def _get_fullname(first, last):
        return ' '.join([n for n in (first, last) if n is not None])

    def write(self):
        with open(self.target, 'w') as out:
            out.write(self.lif.as_json_string())


def usage():
    print("\nUsage:\n"
          + "\n    $ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILELIST"
          + "\n    $ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILELIST -s START -e END"
          + "\n    $ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILELIST --crash"
          + "\n    $ python3 create_lif.py (-h | --help)\n")


if __name__ == '__main__':

    source_dir = '/DATA/eager/pubmed-01000'
    data_dir = '/DATA/eager/sample-01000'
    filelist = '../../data/files-random-01000.txt'

    options = dict(getopt.getopt(sys.argv[1:], 's:d:f:b:e:h', ['crash', 'help'])[0])
    source_dir = options.get('-s', source_dir)
    data_dir = options.get('-d', data_dir)
    filelist = options.get('-f', filelist)
    begin = int(options.get('-b', 1))
    end = int(options.get('-e', 1))
    crash = True if '--crash' in options else False
    help_wanted = True if '-h' in options or '--help' in options else False

    if help_wanted:
        usage()
    else:
        process_filelist(source_dir, data_dir, filelist, begin, end, crash=crash)
