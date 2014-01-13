#!/bin/bash


if [ $# -lt 2 ];then
	echo "Produces allele frequency for a single VCF.gz file.
	usage: `basename $0` <file.vcf.gz> <out_folder> [id_names.list]
	
	where:
	  id_names.list is an optional list of individual IDs in the VCF file to filter for and then produce a frequency calculation from that subset
	
	">&2
	exit
fi


file=$1
folder=$2
names_file=$3

chr=$(echo $file | egrep -o "chr[0-9XY]{1,2}")
names=""

if [ "$names_file" != "" ];then
	names=""
	while read line;do
		names=$names"--indv $line "
	done < $names_file
fi

mkdir -p $folder

/opt/vcftools/vcftools --gzvcf $file $names --freq --out $folder/$chr


#mv $chr.frq $folder/
#mv $chr.log $folder/
