#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov.py -r -f $fn
done
chmod 664 ../output/heatmap/raw/*.* 
chgrp -R D4D ../output/heatmap/raw
exit
