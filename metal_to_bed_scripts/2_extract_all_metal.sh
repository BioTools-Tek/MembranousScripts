#!/bin/bash

[ $# != 1 ] && echo "$0 <foldername_with_details_plotonly_subfolders>

Extracts all the metal data from plots that are left in the plot_only subfolder" && exit


nani=$1

cd $nani/details;

coloured_plot_ids="";

for posses in $(ls ../plots_only/*.pdf); do
	nam=$(echo $posses | awk -F"_" '{print $NF}' | awk -F"." '{print $1}');
	coloured_plot_ids="$coloured_plot_ids
$nam";
done;

echo "$coloured_plot_ids" > ../plots_only/coloured_plots.list

metal_fold="../coloured_metals"
mkdir -p $metal_fold

for id in $coloured_plot_ids; do
#	id=$( echo $id | sed 's/:/\\:/g')
	metal_file=*$id/chr*.Rdata

	! [ -f $metal_file ] && echo "$id cannot be found at $metal_file" && exit

	echo $metal_file
	Rscript ../../get_metal_data.Rscript $metal_file $metal_fold/$id.metal
done
