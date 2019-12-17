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
1.
1.


### 1. Converting nxml files into JSON

Use the script `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 convert_nxml.py -s SOURCE_DIR -d DATA_DIR -f FILELIST -e 9999999
```

The JSON created is very similar to the output of science-parse. This was done because it would make it possible to reuse the DTRA demo pipeline. In retrospect, we could have just created LIF files directly.

See the docstring for more information. Files are taken from `SOURCE_DIR/src` and results are written to `DATA_DIR/jsn` which is created if it does not exist, existing files inside that directory may be overwritten. Filenames are the same (extensions are not changed).

Run time on full data set is about 40-50 hours on `tarski.cs.brandeis.edu` (with 36 Intel(R) Xeon(R) CPU E5-2695 v4 @ 2.10GHz processors and 125G of memory). Size of processed data is 8.2G.


### 2. Creating LIF files

Script: `code/pipeline/convert_nxml.py`:

```bash
$ cd code/pipeline
$ python3 create_lif.py -d DATA_DIR -f FILELIST -e 9999999
```

Files are read from `DATA_DIR/jsn`, LIF files are written to `DATA_DIR/lif`, all with the `.lif` extension, plain text files are written to `DATA_DIR/txt` with the `.txt` extension.

Run time is a bit less than an hour, he size of the `lif` directory is 12G.


### 3. Adding topics

Script: `code/pipeline/generate_topics.py`

First create a model:

```
$ python3 generate_topics --build -d DATA_DIR -f FILELIST -e 10000
```

This needs to be done only once. The model itself is saved in `../../data/topcs` and will b eloaded as needed.

Run the model on LIF files:

```
$ python3 generate_topics -d DATA_DIR -f FILELIST -e 10000
```

Creating the model from the 10K files took about 8 minutes. Run time is .
Size of created data is .
