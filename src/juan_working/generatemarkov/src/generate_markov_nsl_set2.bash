#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov_nsl.py -s -w -f $fn
done
chmod 660 ../output/heatmap/nsl/seasons/*.csv
chmod 660 ../output/heatmap/nsl/weekends/*.csv
chmod 660 ../output/heatmap/nsl/weekdays/*.csv
chmod 660 ../output/heatmap/nsl/days/*.csv

chmod 660 ../output/heatmap/nsl/raw/seasons/*.csv
chmod 660 ../output/heatmap/nsl/raw/weekends/*.csv
chmod 660 ../output/heatmap/nsl/raw/weekdays/*.csv
chmod 660 ../output/heatmap/nsl/raw/days/*.csv
chgrp -R D4D ../output/heatmap
exit
