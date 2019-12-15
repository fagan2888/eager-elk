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
$ python3 convert_nxml 9999999
```

The script assumes that a few global variables are set to the appropriate files and directories. See the docstring for more information. Results will be written to the directory specified in the OUT_DIR variable.
