#!/bin/bash

usage(){
	echo "Produces SNP id position files for each chromosome 1kG0 VCF.GZ file
	
	usage: `basename $0` <output_dir> <[input_files.vcf.gz]> ">&2
	exit
}

[ $# -lt 1 ] && usage

folder=$1
files="${@:2}"


#1. Parallel, why not
parallel -u ./getSNPSingle.sh '{}' $folder ::: $files

# OR

#2. Singular
#for file in files; do
#	./getFreqSingle.sh $file $folder;
#done
