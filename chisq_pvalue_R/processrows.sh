#!/bin/bash

usageExit(){
	echo "`basename $0` <4_column.tables>
	" >&2
	exit
}

[ $# != 1 ] && usageExit
table=$1

while read line;do
	vals=$(Rscript chisq_pvalue_oneline.r --args $line)
	vals_correct=$(echo $vals | sed s'/e/E/g' )
	echo $line" "$vals_correct
done < $table
