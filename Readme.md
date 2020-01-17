# EAGER-ELK

Code used to created the Elastic Search database for PubMed Central documents.

Requirements

	bs4
	lxml
	genzim
	nltk

For nltk you need to load a few resources:

```python
>>> nltk.download('stopwords')
>>> nltk.download('punk')
>>> nltk.download('wordnet')
```

Processing steps:

1. Converting nxml files into json files
1. Converting json files into lif files
1. Adding topics
1. Running the Tarsqi Toolkit
1.


### 1. Converting nxml files into JSON

Use the script `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 convert_nxml.py -s SOURCE_DIR -d DATA_DIR -f FILELIST -e 9999999
```

The JSON created is very similar to the output of science-parse. This was done because it would make it possible to reuse the DTRA demo pipeline. In retrospect, we could have just created LIF files directly.

See the docstring for more information. Files are taken from `SOURCE_DIR/src` and results are written to `DATA_DIR/jsn` which is created if it does not exist, existing files inside that directory may be overwritten. Filenames are the same (extensions are not changed).

Run time on full data set is about 40-50 hours on `tarski.cs.brandeis.edu` (with 36 Intel(R) Xeon(R) CPU E5-2695 v4 @ 2.10GHz processors and 125G of memory). Size of generated data is 8.2G.


### 2. Creating LIF files

Script: `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 create_lif.py -d DATA_DIR -f FILELIST -e 9999999
```

Files are read from `DATA_DIR/jsn`, LIF files are written to `DATA_DIR/lif`, all with the `.lif` extension, plain text files are written to `DATA_DIR/txt` with the `.txt` extension.

Run time is a bit less than an hour, the size of the `lif` directory is 12G.


### 3. Adding topics

Script: `code/pipeline/generate_topics.py`

First create a model:

```bash
$ python3 generate_topics.py --build -d DATA_DIR -f FILELIST -e 10000
```

This needs to be done only once. The model itself is saved in `../../data/topics` and will be loaded as needed.

Run the model on LIF files:

```bash
$ python3 generate_topics.py -d DATA_DIR -f FILELIST -e 10000
```

Creating the model from the 10K files took about 8 minutes. Run time is just under 5 hours.
Size of created data is 22G.


### 4. Running the Tarsqi Toolkit

See https://github.com/tarsqi/ttk on how to install TTK, note that for our purposes here we do not need to install Mallet. We used the most recent commit on the develop branch as of Dec 18 2019 (commit 00c6a53). When installing TTK with a current version of the TreeTagger a change needed to be made to `wrapper.py` in `components/preprocessing/` where on line 35 you need to used `english-utf8.par` instead of `english-utf8.par`.

Once you have TTK installed first set the `PYTHONPATH` environment variable and have it point to where TTK is installed, for example:

```bash
$ export PYTHONPATH=/Users/marc/tools/ttk
```

Now use the `run_tarsqi.py` script in a similar way as before with other modules:

```bash
$ python2 run_tarsqi.py -d DATA_DIR -f FILELIST -e 10000
```

Note that TTK requires Python 2.7. One other difference is that unlike previous modules this module creates gzipped files. Without compression running this on the first 1000 files creates 151M of data, which translates to about 315G for the entire dataset. Compression reduces disk space usage by a factor 15.
