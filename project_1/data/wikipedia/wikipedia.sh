#!/bin/bash

python3 wikipedia_from_wikidata.py
python3 wikipedia_new.py
python3 clean.py
python3 merge.py