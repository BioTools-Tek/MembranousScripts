#!/bin/bash

[ $# != 1 ] && echo "$0 <metal_folder>

Creates bed tracks for all SNPs in metal data that are red or orange" && exit


metal_fold=$1
out_fold=$1/"BED"

mkdir -p $out_fold
outfile=$out_fold/"217_SNPs_with_colored_LD_in_180.85-180.89.track"

metals=$(ls $metal_fold/*.metal)

for metal in $metals;do
	echo -n "$metal"
	./3i_metal_extractor.py $metal >> $outfile
	echo " X"
done
