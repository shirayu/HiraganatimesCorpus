
# Scripts for HiraganatimesCorpus

## What's this?
- These scripts make the corpus machine-friendly

## Requirements
- python 2.X
- [NLTK](http://nltk.org/) for sentence split

## How to use
- ``find THE_CORPUS_DIRECROTY -type f | grep TXT | python ./converter.py PREFIX_OF_OUTPUT_FILE -``


##Known problems
- The numbers of both sentence of both languages are not equal in the new format (from 2011.01)

They are marked with ``FIXME`` in the script.

## License
- General Public License Version3
- Copyright (C) 2013- Yuta Hayashibe
