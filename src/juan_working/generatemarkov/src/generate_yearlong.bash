#!/bin/bash

python yearlongmatrix.py -f ../output/heatmap/raw/seasons/ -o ../output/heatmap/year/season-2013.csv
python yearlongmatrix.py -f ../output/heatmap/raw/weekends/ -o ../output/heatmap/year/weekends-2013.csv
python yearlongmatrix.py -f ../output/heatmap/raw/weekdays/ -o ../output/heatmap/year/weekdays-2013.csv

python yearlongmatrix.py -f ../output/heatmap/nsl/raw/seasons/ -o ../output/heatmap/nsl/year/season-2013.csv
python yearlongmatrix.py -f ../output/heatmap/nsl/raw/weekends/ -o ../output/heatmap/nsl/year/weekends-2013.csv
python yearlongmatrix.py -f ../output/heatmap/nsl/raw/weekdays/ -o ../output/heatmap/nsl/year/weekdays-2013.csv

chmod 660 ../output/heatmap/year/*.csv 
chmod 660 ../output/heatmap/nsl/year/*.csv 

chgrp -R D4D ../output/heatmap/year/
chgrp -R D4D ../output/heatmap/nsl/year/
exit
