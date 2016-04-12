#!/usr/bin/python


import csv
from home_calc_days_functions_BC import *

day = 31
all_day = []
for i in range(day):
    i = i +1
    input_dir = "/opt2/D4D/senegal/code/D4D_working/src/BC_working/out_data_BC/out_data/output_new/"
    data_file = input_dir + "nofilter_" + str(i)+"_"+ "sample_SET3_M01" + ".csv"
    data_array = read_csv_to_matrix(data_file)
    pop_day = []
    for line in data_array:
        d = line[1]
        pop_day.append(d)
    all_day.append(pop_day)

#create csv file as a month
with open('total.csv', 'wb') as f:
    wtr = csv.writer(f, delimiter= ',')
    wtr.writerows(all_day)
