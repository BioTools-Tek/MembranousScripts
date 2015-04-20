#!/bin/bash

#egrep "\sGBR\s" 1kg0.pedfile | awk '{print $2}' > british.ids

echo "GBR" > british.ids
echo -e "CEU\nTSI\nFIN\nGBR\nIBS" > europe.ids

# Get 107 british ids
./europeExtractor.py british.ids 1kg0.pedfile --idcol=2 --popcol=7 > british.ids.list

# Get 670 european ids
./europeExtractor.py europe.ids 1kg0.pedfile --idcol=2 --popcol=7 > europe.ids.list


