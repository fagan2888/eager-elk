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

1. Converting Pubmed files into LIF files
1. Adding topics
1. Running the Tarsqi Toolkit
1.


### 1. Converting nxml files into LIF

Use the script `code/pipeline/create_lif.py`:

```bash
$ cd code/pipeline
$ python3 create_lif.py -s SOURCE_DIR -d DATA_DIR -f FILELIST -e 9999999
```

Takes Pubmed nxml files from `SOURCE_DIR` and writes LIF files to `DATA_DIR/jsn` which is created if it does not exist, existing files inside that directory may be overwritten. Filenames are the same except that extensions are changed from `nxml` into `lif`. The file paths in `FILELIST` are relative paths that point to paths inside `SOURCE_DIR`, for example

```
Front_Endocrinol_(Lausanne)/PMC5632355.nxml
Plast_Reconstr_Surg_Glob_Open/PMC4236383.nxml
PLoS_Pathog/PMC4965185.nxml
```

On tarski, the source directory, data directory and file list are located at

```
/data/pubmed/pmc/oa_bulk/decompressed/
/data/pubmed/pmc-processed/all/
/data/pubmed/pmc-processed/files-random-all.txt
```

Run time on full data set is about 40-50 hours on `tarski.cs.brandeis.edu` (with 36 Intel(R) Xeon(R) CPU E5-2695 v4 @ 2.10GHz processors and 125G of memory). Size of generated data is about 8G.

You can parallelize this as follows:

```bash
$ python3 create_lif.py -s SOURCE -d DATA -f FILELIST -s 1 -e 100000 &
$ python3 create_lif.py -s SOURCE -d DATA -f FILELIST -s 100001 -e 200000 &
$ python3 create_lif.py -s SOURCE -d DATA -f FILELIST -s 200001 -e 300000 &
$ python3 create_lif.py -s SOURCE -d DATA -f FILELIST -s 300001 -e 400000 &
```

This will use four processors and give a good speedup overall. It is not clear when disk access becomes the bottle neck, but this is at least not the case when running up to six jobs at the time (haven't tried with more yet). Apart from processing time this was also done because I ran into mysterious crashes when I ran `create_lif.py` on all files, seemingly corresponding to the connection being broken. Mysterious because I always ran the script in the background and redirected input to a file. I did make some changes to how errors are printed, which may have solved the problem.


### 2. Adding topics

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

When you look at the files created here you will see something funky in the text property:

```json
"text": {
	"@value": null,
	"language": "en",
	"source": "/data/pubmed/pmc-processed/all/lif/Zookeys/PMC3082960.lif"
},
```

The text value is null but there is a `source` attribute that points to a lif file that does have the texts value. This is to save some space on tarski, for the topics this saves about 8G.

Creating the model from the 10K files took about 8 minutes. Run time is just under 5 hours. Size of created data is 14G.


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
