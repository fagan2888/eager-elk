"""analyze_abstracts.py

Prints a few things about the abstracts in nxml files: parent tag and
attributes.

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


PUBMED_DIR = '/data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed'
PUBMED_DIR = '/DATA/eager/pubmed-01000'

FILE_LIST = '../../data/files_random.txt'


def analyze(filelist, start, end):
    process = False
    line_number = 1
    for line in open(filelist):
        fname = line.strip()
        if line_number == start:
            process = True
        if process:
            analyze_abstract(line_number, fname)
        if line_number == end:
            break
        line_number += 1


def analyze_abstract(line_number, fname):
    print('%07d  %s' % (line_number, fname))
    source = os.path.join(PUBMED_DIR, fname)
    with open(source) as fp:
        soup = bs4.BeautifulSoup(fp, 'lxml')
        abstracts = soup.find_all('abstract')
        for abstract in abstracts:
            print('  ', abstract.parent.name, abstract.attrs)


if __name__ == '__main__':

    start = 1
    if len(sys.argv) == 2:
        start, end = 1, int(sys.argv[1])
    elif len(sys.argv) == 3:
        start, end = int(sys.argv[1]), int(sys.argv[2])
    else:
        exit("\nERROR: wrong parameters.\n\n"
             + "Usage:\n\n"
             + "    $ python3 analyze_abstracts.py END\n"
             + "    $ python3 analyze_abstracts.py START END\n")

    analyze(FILE_LIST, start, end)
