#!/bin/bash

python yearlongmatrix.py -f ../output/home_location/$1/raw/seasons/ -o ../output/home_location/$1/year/season-2013.csv
python yearlongmatrix.py -f ../output/home_location/$1/raw/weekends/ -o ../output/home_location/$1/year/weekends-2013.csv
python yearlongmatrix.py -f ../output/home_location/$1/raw/weekdays/ -o ../output/home_location/$1/year/weekdays-2013.csv

python yearlongmatrix.py -f ../output/home_location/$1/nsl/raw/seasons/ -o ../output/home_location/$1/nsl/year/season-2013.csv
python yearlongmatrix.py -f ../output/home_location/$1/nsl/raw/weekends/ -o ../output/home_location/$1/nsl/year/weekends-2013.csv
python yearlongmatrix.py -f ../output/home_location/$1/nsl/raw/weekdays/ -o ../output/home_location/$1/nsl/year/weekdays-2013.csv

chmod 660 ../output/home_location/$1/year/*.csv 
chmod 660 ../output/home_location/$1/nsl/year/*.csv 

chgrp -R D4D ../output/home_location/$1/year/
chgrp -R D4D ../output/home_location/$1/nsl/year/
exit
