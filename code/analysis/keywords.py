"""keywords.py


Gets the pubmed directory from PUBMED_DIR and uses a list of abstracts in
FILE_LIST, which has relative paths from the PUBMED_DIR.

Usage:

$ python3 analyze_abstracts.py END
$ python3 analyze_abstracts.py START END

START and END are line numbers in FILE_LIST to include, START defaults to 1.

"""


import os
import sys
import bs4


PUBMED_DIR = '/data/pubmed/pmc/oa_bulk/decompressed/'
PUBMED_DIR = '/DATA/eager/pmc/sample-01000/src'

FILE_LIST = '/data/pubmed/pmc-processed/files-random-all.txt'
FILE_LIST = '../../data/files-random-01000.txt'


def keywords(filelist):
    kwd2fname = {}
    c = 0
    for line in open(filelist):
        c += 1
#        if c > 10: break
        fname = line.strip()
        #print('%s' % fname)
        source = os.path.join(PUBMED_DIR, fname)
        with open(source) as fp:
            soup = bs4.BeautifulSoup(fp, 'lxml')
            kwds = soup.find_all('kwd')
            for kwd in kwds:
                kwd = kwd.text.replace('\t', ' ').strip()
                kwd2fname.setdefault(kwd, []).append(fname)
    for kwd, fnames in kwd2fname.items():
        print("%d %s" % (len(fnames), kwd))
        for fname in fnames:
            print("\t%s" % fname)
            

if __name__ == '__main__':

    keywords(FILE_LIST)
