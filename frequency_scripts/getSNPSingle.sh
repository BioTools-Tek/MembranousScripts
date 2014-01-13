#!/bin/bash

if [ $# != 2 ]; then
	echo "Prints Chrom\\tPos\\DBSNP into a file labelled chr<N>.ids
	usage: `basename $0` <something.chrN.vcf.gz> <output_folder>
	" >&2
	exit
fi

vcf=$1
folder=$2

chr=$(echo $vcf | egrep -o "chr[0-9XY]{1,2}")

mkdir -p $folder
echo "Doing:" $chr >&2
cat $vcf | gunzip | cut -f 1,2,3 > $folder/$chr.ids
echo "DONE:" $chr >&2
