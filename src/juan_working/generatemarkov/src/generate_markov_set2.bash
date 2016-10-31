#!/bin/bash

FILES=/opt/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov.py -s -w -f $fn
done
chmod 664 ../output/heatmap/*.* 
chgrp -R D4D ../output/heatmap
exit
