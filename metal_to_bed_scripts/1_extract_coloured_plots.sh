#!/bin/bash

[ $# != 1 ] && echo "$0 <foldername_with_details_plotonly_subfolders>

Places the uncoloured plots from a batch locuszoom_multi.sh job into a subfolder in plotonly" && exit


nani=$1

files="";

cd $nani/details;

for posses in $(grep "No usable" ./ -R | egrep -o "chr[0-9]+:[0-9]+"); do 
	nam=$(ls ../plots_only/chr*$posses.pdf);
	files="$files
$nam";
done;

echo "$files" | sort -h > ../plots_only/"uncoloured_plot.filenames"

uncool_fold="../plots_only/uncoloured_plots/"

mkdir -p $uncool_fold

for f in $files; do
	mv $f $uncool_fold
done
