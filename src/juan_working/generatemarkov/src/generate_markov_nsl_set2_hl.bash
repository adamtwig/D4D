#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov_homelocation_nsl.py -s -w -l $1 -f $fn
done
chmod 660 ../output/home_location/$1/nsl/seasons/*.csv
chmod 660 ../output/home_location/$1/nsl/weekends/*.csv
chmod 660 ../output/home_location/$1/nsl/weekdays/*.csv
chmod 660 ../output/home_location/$1/nsl/days/*.csv

chmod 660 ../output/home_location/$1/nsl/raw/seasons/*.csv
chmod 660 ../output/home_location/$1/nsl/raw/weekends/*.csv
chmod 660 ../output/home_location/$1/nsl/raw/weekdays/*.csv
chmod 660 ../output/home_location/$1/nsl/raw/days/*.csv
chgrp -R D4D ../output/home_location
exit
