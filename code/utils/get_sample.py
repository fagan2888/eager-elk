"""get_sample.py

Get a random sample of the pubmed files and write them to a directory.

Usage

$ python3 get_sample.py DIRECTORY LIMIT

DIRECTORY is the directory to write the files to and LIMIT is how many
files you write. Directory structure is the same as in the source,
that is, it has directories for each journal.

Relies on having the file with the randomized list of file names in
FILELIST.

This can be used to generate a mini corpus that can be easily zipped
and moved elsewhere. Note that for local processing we tend to use
file lists that point to the source.

"""


import os
import sys
import shutil


PUBMED_DIR = '/data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed'
FILELIST = 'files_random.txt'


output_dir = sys.argv[1]
limit = int(sys.argv[2])

print("Writing %d files to %s" % (limit, output_dir))

file_list = open('files_random.txt')

journals = set()
files = []

c = 0
for line in file_list:
    c += 1
    if c > limit:
        break
    fname = line.strip()
    journal = os.path.split(fname)[0]
    journals.add(journal)
    files.append(fname)

for i, journal in enumerate(sorted(journals)):
    print(i, journal)

os.mkdir(output_dir)
for journal in journals:
    os.mkdir(os.path.join(output_dir, journal))
for fname in files:
    source = os.path.join(PUBMED_DIR, fname)
    target = os.path.join(output_dir, fname)
    shutil.copyfile(source, target)
