#!/bin/bash

if [ $# != 1 ];then
	echo "This is a much slower implementation of dbSNP_annotator.py for querying each line with UCSC's dbSNPAll mysql table, variant by variant
	
	usage: `basename $0` <chr\tposition.hg19.input>
	" >&2
fi

