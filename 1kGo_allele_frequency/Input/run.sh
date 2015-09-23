#!/bin/bash


vcf_folder=$1
sites_file=$2

[ "$sites_file" = "" ] && echo "`basename $0` <vcf_folder> <input_sites.txt>

Where the sites file is a tab-delimited file of: chrN,gene_name,snp
" >&2 && exit

build_command(){
	file=$1
	chrom=$2
	snp=$3
	
	vcftools --gzvcf $file --chr $chrom --snp $snp --extract-FORMAT-info GT --out "out_$chrom"
}


# Handle input sites
while read line; do
	chr=$(echo $line | awk '{print $1}')
	snp=$(echo $line | awk '{print $3}')
	
	file=$(find $vcf_folder -type f -name "*.$chr.*.gz")
	
	[ "$file" = "" ] && echo "Could not find $chr" && exit
	
	build_command $file $chr $snp
	

done<$sites_file

