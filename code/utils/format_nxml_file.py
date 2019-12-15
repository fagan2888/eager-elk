"""format_nxml_file.py

Take an nxml file in the pubmed central directory and create a pretty
printed version in the samples directory.

Usage example:

$ python3 format_nxml_file.py PLoS_Pathog/PMC4965185.nxml

"""

import os
import sys


PUBMED_DIR = '/data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed'
PUBMED_DIR = '/DATA/eager/pubmed-01000'
PUBMED_DIR = '/DATA/eager/pubmed-10000'

SAMPLES_DIR = '../../data/samples'


fname = sys.argv[1]
fname_target = fname.replace('/', '-')

source = os.path.join(PUBMED_DIR, fname)
target = os.path.join(SAMPLES_DIR, fname_target)
if target.endswith('.nxml'):
    target = target[:-4] + 'xml'


command = "xmllint --format %s > %s" % (source, target)
print(command)
os.system(command)
