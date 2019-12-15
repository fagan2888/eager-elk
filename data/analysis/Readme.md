**abstracts-01000.txt**

Created with ../code/utils/analyze_abstracts.py using END=1000 and piping into the file.

To get a view on what attributes we have in abstracts-01000.txt do

```bash
$ grep -v 0000 abstracts-01000.txt | cut -f2 -d'{' | sort | uniq -c
```
