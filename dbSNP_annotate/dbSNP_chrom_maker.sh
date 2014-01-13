#!/bin/bash

usage(){
	echo "`basename $0` <output_dir>" >&2
	exit
}

[ $# != 1 ] && usage

fold=$1
mkdir -p $fold

for chrom in `seq 1 22` X; do
	chr="chr$chrom";

	echo -n "$chr...">&2
#	mysql -ugenome --host=genome-mysql.cse.ucsc.edu -A --execute="SELECT chrom,chromStart,chromEnd,name,score,strand from hg19.snp137 WHERE chrom=\"$chr\";"\
	mysql -ugenome --host=genome-mysql.cse.ucsc.edu -A --execute="SELECT chrom,chromStart,chromEnd,name,score,strand from hg18.snp130 WHERE chrom=\"$chr\";"\ > $fold/snppos.$chr
	echo "`wc -l $fold/snppos.$chr`"

done
