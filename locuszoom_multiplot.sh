#!/bin/bash

if [ $# -lt 3 ];then
	echo "Prints several zoomplots centered around each SNP in the names file, for each input file detected in the folder.
Requires input files to be named with *.input.* regex

usage:`basename $0` <output_postfix> <names> <chrN:start-end> [maxY]

tabix r-base-core and plink must be installed" >&2
	exit
fi 

outfix=$1
snpnames=$2
range=$3		#chr2:12345-123456
maxY=$4
[ "$maxY" = "" ] && maxY=10

chr=`echo $range | awk -F ':' '{print $1}' | awk -F "chr" '{print $NF}'`
start=`echo $range | awk -F ':' '{print $2}' | awk -F '-' '{print $1}'`
ender=`echo $range | awk -F ':' '{print $2}' | awk -F '-' '{print $2}'`

#	  --chr 2 --start 160794947 --end 160936686\

#Input files
inputs=`ls 1_zoomplot.input*`

plotMe(){
	if [ $# != 3 ];then echo "Missing args¬!" >&2; exit; fi 
	
	metal=$1
	ref=$2
	title=$3
	
	block=-1 # hide
					#1,4,20,21,22
	
#	dot=20
#	cross=4
	
#	circle=1, cirx=10, fci=16, fci2=19, fci1=20, bci=21
#	tri_up=2, btr1=24, btr2=25, tri_dn=6
#	cross=3, ex=4
#	kite=5, bki=23, fdm=18

#	xbox=7
#	aster=8
#	diamx=9
	
#	dav=11
#	boxx=12, bsq=22
#	wick=13, tent=14, fsq=15, ftr=17


	
#	bin/locuszoom --refsnp=$ref\
#	  --plotonly --verbose --metal $metal\
#	  --chr $chr --start $start --end $ender\
#	  --prefix EUR --build hg19 --pop EUR --source 1000G_March2012\
#	  --delim tab --pvalcol P.value --snpset HapMap\
#	  geneFontSize=.8 smallDot=.3 largeDot=.9 format=pdf ymax=$maxY\
#	  title=\""$title""_hg19_2012_EUR"\" legend=auto\
#	  metalRug='Plotted SNPs' rfrows=10 weightCol=Weight showRecomb=TRUE\
#	  warnMissingGenes=T showAnnot=TRUE annotPch=24,24,25,22,22,8,7,$block,$block


# vanilla
#	pop=EUR
	pop=AFR

	bin/locuszoom --refsnp=$ref\
	 --verbose --metal $metal\
	  --chr $chr --start $start --end $ender\
	  --prefix $pop --build hg19 --pop $pop --source 1000G_March2012\
	  --delim tab --pvalcol P.value --snpset HapMap\
	  geneFontSize=.8 smallDot=.3 largeDot=.9 format=pdf ymax=$maxY\
	  title=\""$title""_hg19_2012_$pop"\" legend=auto\
	  metalRug='Plotted SNPs' rfrows=10 weightCol=Weight showRecomb=TRUE\
	  warnMissingGenes=T showAnnot=TRUE annotPch=24,24,25,22,22,8,7,21,21

}

new_out="$outfix"
detailed=$new_out/"details"
plots_only=$new_out/"plots_only"
mkdir -p $plots_only $detailed

while read line;do
	refsnp=`echo $line | awk '{print $1}'`

	[[ "$line" =~ "#" ]] && continue # ignore comments
	
	for input in $inputs; do
		postfix=$(echo `basename $input` | awk -F '.' '{print $3}')
		plotMe $input $refsnp "PLA2R1_$postfix"
		
		output_fold=`ls -t | head -1`  #newest
		basehead=$(basename $output_fold)
		
		mv $output_fold $detailed/
		cp $detailed/$basehead/*.pdf $plots_only/`basename $detailed/$basehead/*.pdf .pdf`"_$refsnp".pdf
	done
	
done < $snpnames
