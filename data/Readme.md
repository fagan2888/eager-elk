#### files-sorted-01000.txt

This file contains the file names of the 1000 article sample of the full data
that was created with `code/utils/get_sample.py`.

The list itself was created by `code/utils/get_filenames.py`.

This file is included in the repository as an example. When you run the
conversion code in `code/pipeline/convert_nxml.py` on the entire set you should
use `get_filenames.py` to create a list of all file names.


#### files-random-01000.txt

Randomized version of `files-sorted-01000.txt`.

To get a random sort do one of the following:

```bash
$ sort --random-sort files-sorted.txt > files-random.txt
$ cat files-sorted.txt | perl -MList::Util -e 'print List::Util::shuffle <>' > files-random.txt
```

Again, this file is for the 1000 element sample, you should create a full one
for running the conversion code.
