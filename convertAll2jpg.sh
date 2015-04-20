#!/bin/bash

if [ $# != 2 ];then
	echo -e "Converts first page of all PDFs in directory to an image and tiles them by nubmer of rows given
\tusage:	`basename $0` <rows> <input_folder>"

	exit -1
fi


function getName() {
	file=$1

	poss=("Default SNPs"\
 "Known SNPs" "Known SNPs + dummy controls"\
 "Unknown SNPs"\
 "Greater than 5%" "Greater than 5% dummy controls"\
 "Greater than 1%" "Greater than 1% dummy controls")

	map=( "\.all"\
 "\.known_BAR" "\.known_swnmaf"\
 "\.a_unknown"\
 "\.gt5perc_BAR" "\.gt5perc_swnmaf"\
 "\.gt1perc_BAR" "\.gt1perc_swnmaf" )

	count=0
	max_len=$(( ${#map[@]} ))

	res="NA"

	until [ "$count" = "$max_len" ];do
		m="${map[$count]}"
#		echo "looking for $m in $file" >&2

		if [ "$(echo $file | grep $m | wc -w)" != "0" ]; then
			res="${poss[$count]}"
#			echo "FOUND" >&2
			break
		fi
		count=$(( $count + 1 ))
	done
	echo $res
}



rows=$1
inpfold=$2

cd $inpfold

pdfs=$(ls *.pdf* | grep -v "jpg" 2>/dev/null)
if [ "$pdfs" != "" ];then
	for p in $pdfs; do
		dir=$(dirname $p)
		base=$(basename $p .pdf)
		newbase=$dir/"IMG_"$base".jpg"

		#put all and unknown together
		if [ "$(echo $newbase | grep "unkn" | wc -w)" != "0" ];then
			newbase=$(echo $newbase | sed 's/unkn/a_unkn/')	
		fi

		if ! [ -f $newbase ]; then
			convert -density 200 $p -crop -40+120 test.jpg
			#produces test-0.jpg and test-1.jpg. we want 0.

			temp=temp.jpg

			mv test.jpg $temp 2>/dev/null
			mv test-0.jpg $temp 2>/dev/null
		
			rm test-*.jpg 2>/dev/null

			name=$(getName $newbase)
#			exit -1

			convert $temp -gravity NorthWest\
			  -font Verdana-regular -pointsize 60\
			  -undercolor white\
			  -gravity Center\
			  -draw "text 0,595 \"$name\"" $newbase
			  #-annotate 0 '@-' $newbase

			rm $temp

		fi
#		echo $newbase >&2
	done
fi

#Tile all
imgs=*.jpg

echo $imgs | sed 's/\s/\n/g' >&2

montage $imgs -tile x$rows -geometry +5+5 -border 10 -shadow ../$(basename $inpfold .jpg).jpg

cd ..
