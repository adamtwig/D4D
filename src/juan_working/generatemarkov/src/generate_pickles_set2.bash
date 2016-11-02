#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python createusrdistancepickle.py $fn
	python processusrdistancepickle.py $fn
done
exit
