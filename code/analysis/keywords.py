"""keywords.py

Gets the pubmed directory from PUBMED_DIR and uses a list of abstracts in
FILE_LIST, which has relative paths from the PUBMED_DIR.

Usage:

$ python3 keywords.py --collect
$ python3 keywords.py --tabulate
$ python3 keywords.py --select

--collect - Creates out-keywords1.txt which on each line has a file
  name and all the keywords defined for that file.

--tabulate - Creates out-keywords2.txt which has a line with a count
  and a keyword keyword followed by zero or more tab-indented lines
  with the filenames where it occurred.

--select - Selects those keywords that occur at least MINCOUNT times
  in out-keywords2.txt and for each keyword writes a file with all
  file names for the keyword to out-keywords.

Running --collect broke after about 1M lines, no idea why.

"""


import os
import sys
import bs4


PUBMED_DIR = '/data/pubmed/pmc/oa_bulk/decompressed/'
#PUBMED_DIR = '/DATA/eager/pmc/sample-01000/src'

FILE_LIST = '/data/pubmed/pmc-processed/files-random-all.txt'
#FILE_LIST = '../../data/files-random-01000.txt'

MINCOUNT = 2000

OUT1 = 'out-keywords1.txt'
OUT2 = 'out-keywords2.txt'


def collect_keywords(filelist):

    with open(filelist) as IN, open(OUT1, 'w') as fh_out:
        c = 0
        for line in IN:
            c += 1
            # if c > 10: break
            fname = line.strip()
            #print(fname)
            source = os.path.join(PUBMED_DIR, fname)
            with open(source) as fh_in:
                soup = bs4.BeautifulSoup(fh_in, 'lxml')
                kwds = soup.find_all('kwd')
                fh_out.write(fname)
                for kwd in kwds:
                    kwd = kwd.text.replace('\t', ' ').strip()
                    fh_out.write("\t%s" % kwd)
                fh_out.write('\n')


def tabulate_keywords():
    with open(OUT1) as fh_in, open(OUT2, 'w') as fh_out:
        kwd2fname = {}
        c = 0
        for line in fh_in:
            c += 1
            if c % 100 == 0:
                print(c)
            # hack to skip some weird input
            if line.startswith("indicus sp. n."):
                continue
            fields = line.strip().split('\t')
            if len(fields) > 1:
                fname = fields[0]
                # use set in case there are duplicates, which happens sometimes
                for kwd in set(fields[1:]):
                    kwd2fname.setdefault(kwd, []).append(fname)
        for kwd, fnames in kwd2fname.items():
            fh_out.write("%d %s\n" % (len(fnames), kwd))
            for fname in fnames:
                fh_out.write("\t%s\n" % fname)
            

def select_keywords():
    store_fname = False
    fh = None
    for line in open('out-keywords2.txt'):
        if line.startswith('\t'):
            if fh is not None:
                fh.write(line.strip('\t'))
        else:
            try:
                count, keyword = line.strip().split(' ', 1)
                if int(count) >= MINCOUNT:
                    fh = open('out-keywords/%s.txt' % keyword.lower().replace(' ', '_'), 'w')
                    print(count, keyword)
                else:
                    if fh is not None:
                        fh.close()
                        fh = None
            except:
                print("ERROR:", line.strip())


if __name__ == '__main__':

    if sys.argv[1] == '--collect':
        collect_keywords(FILE_LIST)
    elif sys.argv[1] == '--tabulate':
        tabulate_keywords()
    elif sys.argv[1] == '--select':
        select_keywords()

