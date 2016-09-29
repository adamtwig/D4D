#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
     Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation

         Helper functions used in main program --
             home_calc_AT.py

Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt

# given a csv, generate a numpy array of lists 
def read_csv_to_matrix(csv_file):
    data_list = []
    with open(csv_file,'rb') as myfile:
        for line in myfile:
            list_line = line.strip('\n"\r').split(',')
            data_list.append(list_line)
    return np.array(data_list)

# get distinct values from 2d numpy array
def count_active_ids(array_2d, id_index):
    ids = set([])
    for array in array_2d:
        ids.add(int(array[id_index]))
    return sorted(list(ids))

# use datetime module to get date from string
def get_date(timestamp):
    return dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

# create date object given hours, minutes, seconds
def create_date(h, m, s):
    return dt.datetime.now().replace(hour=h, minute=m, second=s)

# aggregate 2d numpy array on x axis
# for each user return the index of antenna made max calls
# return 1d array for each antenna num users made max calls
def agg_ant_freq(array_2d):
    max_ant_indices = np.argmax(array_2d, axis=1)
    return max_ant_indices

# generate file of form:
# antennaID, numUsersMadeMaxCalls
def output_write(prefix, filename, antID_array, antDict):
    outfile = open(prefix+filename, 'w')
    for i in range(len(antID_array)):
        # add 1 since frequency matrices run from 0 to n-1
        outfile.write(str(antDict[i]) + ',' + str(antID_array[i]+1) + "\n")

