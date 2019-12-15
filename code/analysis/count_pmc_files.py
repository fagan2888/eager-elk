"""check_pubmed_central_files.py

Just counting the files and printing some counts for large journals.

"""

import os

PUBMED_DIR = '/data/random-dataset-trunk/ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/decompressed'

journals = os.listdir(DIR)
doc_count = 0
c = 0
for journal in journals:
    c += 1
    journal_dir = os.path.join(DIR, journal)
    files = os.listdir(journal_dir)
    journal_files = len(files)
    doc_count += journal_files
    if journal_files > 10000:
        print("%6d  %9d  %s" % (journal_files, doc_count, journal))

print("\nTOTAL =", doc_count)
