"""keywords.py

Gets the pubmed directory from PUBMED_DIR and uses a list of abstracts in
FILE_LIST, which has relative paths from the PUBMED_DIR.

Usage:

$ python3 keywords.py

Two files are created:

- out-keywords1.txt
- out-keywords2.txt

The first has all keywords for each file and the second has all files for each
keyword as well as a count for each keyword.

"""


import os
import sys
import bs4


PUBMED_DIR = '/data/pubmed/pmc/oa_bulk/decompressed/'
PUBMED_DIR = '/DATA/eager/pmc/sample-01000/src'

FILE_LIST = '/data/pubmed/pmc-processed/files-random-all.txt'
FILE_LIST = '../../data/files-random-01000.txt'

OUT1 = 'out-keywords1.txt'
OUT2 = 'out-keywords2.txt'


def keywords1(filelist):

    with open(filelist) as IN, open(OUT1, 'w') as fh_out:
        c = 0
        for line in IN:
            c += 1
            if c > 10: break
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

    with open(OUT1) as fh_in, open(OUT2, 'w') as fh_out:
        kwd2fname = {}
        for line in fh_in:
            fields = line.strip().split('\t')
            if len(fields) > 1:
                fname = fields[0]
                for kwd in fields[1:]:
                    kwd2fname.setdefault(kwd, []).append(fname)
        for kwd, fnames in kwd2fname.items():
            fh_out.write("%d %s\n" % (len(fnames), kwd))
            for fname in fnames:
                fh_out.write("\t%s\n" % fname)
            

if __name__ == '__main__':

    keywords1(FILE_LIST)
