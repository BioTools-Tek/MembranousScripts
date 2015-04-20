#!/bin/bash

usage(){
	echo "`basename $0` <output_dir> [chrom]" >&2
	exit
}

chroms="`seq 1 22` X Y"

[ $# -lt 1 ] && usage
[ $# = 2 ] && chroms=$2


fold=$1
mkdir -p $fold

for chrom in $chroms; do
	chr="chr$chrom";

	echo -n "$chr...">&2
	#mysql -ugenome --host=genome-mysql.cse.ucsc.edu -A --execute="SELECT chrom,chromStart,chromEnd,name,score,strand from hg19.snp138 WHERE chrom=\"$chr\";" > $fold/snppos.$chr
	mysql -ugenome --host=genome-mysql.cse.ucsc.edu -A --execute="SELECT chrom,chromStart,chromEnd,name,score,strand from hg19.snp135 WHERE chrom=\"$chr\";" > $fold/snppos.$chr
	echo "`wc -l $fold/snppos.$chr`"

done
