#!/bin/bash

if [ $# != 2 ];then
	echo "Prints several zoomplots centered around each SNP in the names files

usage:`basename $0` <names> <chrN:start-end>" >&2
	exit
fi 


snpnames=$1
range=$2		#chr2:12345-123456

chr=`echo $range | awk -F ':' '{print $1}' | awk -F "chr" '{print $NF}'`
start=`echo $range | awk -F ':' '{print $1}' | awk -F '-' '{print $1}'`
ender=`echo $range | awk -F ':' '{print $1}' | awk -F '-' '{print $2}'`

#	  --chr 2 --start 160794947 --end 160936686\

while read line;do
	name=$line #trim

	echo bin/locuszoom --refsnp=$name\
	 --plotonly --verbose --metal 1_zoomplot_hg19.input\
	  --chr $chr --start $start --ender $finit\
	  --prefix EUR --build hg19 --pop EUR --source 1000G_March2012\
	  --delim tab --pvalcol P.value --snpset HapMap\
	  geneFontSize=.8 smallDot=.3 largeDot=.9 format=pdf ymax=10\
	  title='Batch0 ALL _hg19_2012_EUR_' legend=auto\
	  metalRug='Plotted SNPs' rfrows=10 weightCol=Weight showRecomb=TRUE\
	  warnMissingGenes=T showAnnot=TRUE annotPch=24,24,25,22,22,8,7,21,21;
done < $snpnames
