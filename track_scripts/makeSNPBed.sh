#!/bin/bash

if [ $# != 1 ];then
	echo -e "Takes in an input file list where first column is name of SNP.If second column exists, then denotes mutation:
\tMISS = green, SYN = blue, NONS(ense) = red
" >&2
	echo -e "\t`basename $0` <list.markers>" >&2
	exit -1
fi


file=$1

chr=""
max=0
min=99999999999999


lineout=""
while read line; do
	snp=$(echo $line | awk '{print $1}')
	mut=$( echo $line | awk '{print $2}')
	
	color=""
	if   [[ "$mut" =~ "MISS"   ]]; then
		color="250,20,20"   #Br. Red
	elif [[ "$mut" =~ "NONS"   ]]; then
		color="150,0,0"     #Dark Red
	elif [[ "$mut" =~ "SYN"    ]]; then
		color="0,200,0"     #Green
	elif [[ "$mut" =~ "5'UTR"  ]]; then
		color="20,20,250"   #Br. Blue
	elif [[ "$mut" =~ "3'UTR"  ]]; then
		color="0,0,150"     #Dark Blue
	elif [[ "$mut" =~ "INTRON" ]]; then
		color="10,10,10"    #Black
	elif [[ "$mut" =~ "SPL_D"  ]]; then
		color="250,20,250"  #Br. Purple
	elif [[ "$mut" =~ "SPL_A"  ]]; then
		color="150,0,150"   #Dark Purple
	fi
	
	other=$(echo $line | awk '{for(i=2;i<=NF;i++){print $i;}}')
	
	chr_start_end_name=$(mysql -ugenome -hgenome-mysql.cse.ucsc.edu -A -e"SELECT chrom,chromStart,chromEnd,name FROM hg19.snp138 WHERE name=\"$snp\""  | egrep "[0-9]")
	
	chr=$(echo $chr_start_end_name | awk '{print $1}')
	start=$(( $(echo $chr_start_end_name | awk '{print $2}') + 0 ))
	end=$(( $(echo $chr_start_end_name | awk '{print $3}') + 0 ))
	
	[ $start -lt $min ] && min=$start
	[ $end -gt $max ] && max=$end
	
	lineout=$lineout"\n"$chr_start_end_name" 0 + $start $end "$color # "$other
	
done < $file

## Print header
echo "track name=\"`basename $1 .input`\" description=\"`basename $1 .input`\" visibility=1 itemRgb=\"On\""
echo -n "browser position $chr:$min-$max"
echo -e $lineout


