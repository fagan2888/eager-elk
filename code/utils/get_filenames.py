"""get_filenames.py

Get all the filenames from the Pubmed Central directory and write them to
files_sorted.txt. You can also run this on a directory that has a sample of all
files as long as the structure of the directory is the same (see get_sample.py
on how to create such a directory).

Next step often is to randomize that file using

$ sort -R files-sorted.txt > files-random.txt
$ cat files-sorted.txt | perl -MList::Util -e 'print List::Util::shuffle <>' > files-random.txt

"""


import os


PUBMED_DIR = '/data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed'
PUBMED_DIR = '/DATA/eager/pubmed-01000'
PUBMED_DIR = '/DATA/eager/pubmed-10000'


journals = os.listdir(PUBMED_DIR)
file_list = open('files-sorted.txt', 'w')

c = 0
for journal in journals:
    c += 1
    # if c > 10: break
    journal_dir = os.path.join(PUBMED_DIR, journal)
    fnames = os.listdir(journal_dir)
    print("%6d  %s" % (len(fnames), journal))
    for fname in os.listdir(journal_dir):
        file_list.write("%s\n" % os.path.join(journal, fname))
