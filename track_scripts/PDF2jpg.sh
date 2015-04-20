#!/bin/bash

pdfs=$(ls *.pdf.*)

imgs=""

#for p in $pdfs; do
#	dir=$(dirname $p)
#	base=$(basename $p)
#	newbase=$dir/"IMG_"$( echo $base | awk -F ".pdf." '{print $1"."$2}')".jpg"

#	convert -density 120 $p test.jpg
#	#produces test-0.jpg and test-1.jpg. we want 0.

#	rm test-1.jpg
#	mv test-0.jpg $newbase
#	imgs=$imgs" "$newbase
#done


#Tile all
imgs=*.jpg
montage $imgs -tile x2 -geometry +5+5 -border 10 -shadow PLA2R1.jpg
