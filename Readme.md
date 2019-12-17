# EAGER-ELK

Code used to created the Elastic Search database for PubMed Central documents.

Requirements

	bs4
	lxml

Processing steps:

1. Converting nxml files into json files
1. Converting json files into lif files
1.
1.
1.


### 1. Converting nxml files

Use the script `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 convert_nxml.py -s SOURCE_DIR -d DATA_DIR -f FILELIST -e 9999999
```

See the docstring for more information. Files are taken from `SOURCE_DIR/src` and results are written to `DATA_DIR/jsn` which is created if it does not exist, existing files inside that directory may be overwritten. Filename are the same (extensions are not changed).

This took about about 40-50 hours to run on `tarski.cs.brandeis.edu` (with 36 Intel(R) Xeon(R) CPU E5-2695 v4 @ 2.10GHz processors and 125G of memory). Size of the processed data is 8.2G.


### 2. Creating LIF files

Use the script `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 create_lif.py -d DATA_DIR -f FILELIST -e 9999999
```

Files are read from `DATA_DIR/jsn`, LIF files are written to `DATA_DIR/lif`, all with the `.lif` extension, plain text files are written to `DATA_DIR/txt` with the `.txt` extension.

This took a bit less than an hour on `tarski.cs.brandeis.edu`. The size of the `lif` directory is 12G.
