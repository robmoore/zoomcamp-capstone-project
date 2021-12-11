#!/usr/bin/env bash

mkdir data
curl -s --output-dir data -O http://jse.amstat.org/v19n3/decock/AmesHousing.txt
# Convert encoding so that text renders properly
curl -s http://jse.amstat.org/v19n3/decock/DataDocumentation.txt | iconv -f CP1252 -t UTF-8 > data/DataDocumentation.txt
