"""get_sample.py

Get a random sample of the pubmed files and write them to a directory.

Usage

$ python3 get_sample.py FILELIST INDIR, OUTDIR, LIMIT

Copies LIMIT files from INDIR to OUTDIR. FILELIST contains a list of relative
paths in INDIR, typically in random order. This file is needed so we can do this
multiple types on directories that have the same structure but that contains the
results of different processing modules.

The directory structure is the same as in the source, but it assumes the pubmed
directory structure. That is, it has directories for each journal. This can be
used to generate a mini corpus that can be easily zipped and moved elsewhere.

Some directories that I have copied from in the past:

- /data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed
- /DATA/eager/sample-01000/lif
- /DATA/eager/sample-01000/top

Ditto for the file list:

- ../../data/files-random-01000.txt


"""


import os
import sys
import glob
import shutil



def collect_files_and_journals(file_list):
    journals = set()
    files = []
    c = 0
    for line in open(file_list):
        c += 1
        if c > limit:
            break
        fname = line.strip()
        fname = os.path.splitext(fname)[0]
        journal = os.path.split(fname)[0]
        journals.add(journal)
        files.append(fname)
    return journals, files


def make_directories(out_dir, journals):
    os.makedirs(out_dir)
    for i, journal in enumerate(sorted(journals)):
        print(i, journal)
        os.mkdir(os.path.join(out_dir, journal))


def copy_files(in_dir, out_dir, files):
    for fname in files:
        # this is the file path without any extension, we now find the extension
        base_path = os.path.join(in_dir, fname)
        matches = glob.glob(base_path + '*')
        ext = matches[0][len(base_path):]
        source = os.path.join(in_dir, fname + ext)
        target = os.path.join(out_dir, fname + ext)
        shutil.copyfile(source, target)


if __name__ == '__main__':

    file_list = sys.argv[1]
    in_dir = sys.argv[2]
    out_dir = sys.argv[3]
    limit = int(sys.argv[4])
    print("Copying %d files from %s to %s" % (limit, in_dir, out_dir))
    journals, fnames = collect_files_and_journals(file_list)
    make_directories(out_dir, journals)
    copy_files(in_dir, out_dir, fnames)
