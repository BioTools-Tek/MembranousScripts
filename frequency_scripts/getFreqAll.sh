#!/bin/bash

usage(){
	echo "Produces variant frequency files for each chromosome 1kG0 VCF.GZ file
	
	usage: `basename $0` <output_dir> <[input_files.vcf.gz]> [--names=list_ids.list] [--snps=list_rs.list] ">&2
	exit
}

[ $# -lt 2 ] && usage

folder=$1
namesfile=""
snpsfile=""
files=""

for arg in ${@:2}; do
	if [[ "$arg" =~ "--names=" ]];then
		namesfile=`echo $arg | sed s'/--names=//' `
	elif [[ "$arg" =~ "--snps=" ]];then
		snpsfile=`echo $arg | sed s'/--snps=//' `
	else
		files=$files" "$arg
	fi
done


#1. Parallel, why not
parallel -u ./getFreqSingle.sh '{}' $folder $namesfile $snpsfile ::: $files

# OR

#2. Singular
#for file in files; do
#	./getFreqSingle.sh $file $folder;
#done
