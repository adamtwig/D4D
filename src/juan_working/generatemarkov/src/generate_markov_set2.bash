#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov.py -s -w -f $fn
done
chmod 660 ../output/heatmap/seasons/*.csv
chmod 660 ../output/heatmap/weekends/*.csv
chmod 660 ../output/heatmap/weekdays/*.csv
chmod 660 ../output/heatmap/days/*.csv

chmod 660 ../output/heatmap/raw/seasons/*.csv
chmod 660 ../output/heatmap/raw/weekends/*.csv
chmod 660 ../output/heatmap/raw/weekdays/*.csv
chmod 660 ../output/heatmap/raw/days/*.csv
chgrp -R D4D ../output/heatmap
exit
