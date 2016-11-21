#!/bin/bash

FILES=/opt2/D4D/senegal/data/SET2/raw/*.CSV
for f in $FILES
do
  	echo "Processing $f file..."
  	fn=`echo "$f" | awk -F\/ '{print $NF}'`	
	python generatemarkov_homelocation.py -s -w -l $1 -f $fn
done
chmod 660 ../output/home_location/$1/seasons/*.csv
chmod 660 ../output/home_location/$1/weekends/*.csv
chmod 660 ../output/home_location/$1/weekdays/*.csv
chmod 660 ../output/home_location/$1/days/*.csv

chmod 660 ../output/home_location/$1/raw/seasons/*.csv
chmod 660 ../output/home_location/$1/raw/weekends/*.csv
chmod 660 ../output/home_location/$1/raw/weekdays/*.csv
chmod 660 ../output/home_location/$1/raw/days/*.csv
chgrp -R D4D ../output/home_location
exit
