# -*- coding: utf-8 -*-
"""
===================================
GENERATE ALL YEAR LONG MATRIX
===================================
Create matrix of all year movements based on Call Records
And some statistics.
"""

import os
import sys
import glob
import errno
import getopt
import time
import cPickle as pickle
import numpy as np

from pickle import PicklingError
from haversine import haversine
from models import D4Duser
from utils import *

users = {}
antennas = np.array([])

def get_key_date(timestamp):
    return dt.datetime.strptime(timestamp, "%m-%d-%Y")

def load_antennas(antennas_file_path):
    global antennas
    if antennas.size == 0:
        antennas = read_csv_to_matrix(antennas_file_path)

def load_pickle(pickle_file_path):
    global users
    if not users:
        pkl_file = open(pickle_file_path, 'rb')
        users = pickle.load(pkl_file)
        pkl_file.close()

def write_to_csv(csv_file_path, headers, array):
    #checking if the distance path exist
    if not os.path.exists(os.path.dirname(csv_file_path)):
        try:
            os.makedirs(os.path.dirname(csv_file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #Saving antennas
    with open(csv_file_path, "w") as f:
        f.write(headers)
        i = 0
        for row in array:
            
            #need to eliminate column 0, there's no antenna 0
            row_to_list = [str(x) for x in row]
            row_str = str(i+1)+','+','.join(row_to_list)+'\n'
            f.write(row_str)
            i+=1

def normalize_array(array):
    i = 0
    for row in array:
        row_sum = np.sum(row)
        if row_sum > 0.0:
            array[i,:] /= row_sum
        i+=1
    return array

def generate_year(filespath, output):
    print "YEAR ******** Path to files: ",filespath
    files_list = glob.glob(filespath+'/*.csv')
    year_numpy_list = []
    for csv_file in files_list:
        tmpArray = read_csv_to_matrix(csv_file)
        tmpArray = tmpArray[1:,1:]
	year_numpy_list.append(tmpArray)
    if year_numpy_list:
        print "loaded %d arrays"%(len(year_numpy_list))
    year_array = np.zeros((year_numpy_list[0].shape[0], year_numpy_list[0].shape[0]))
    
    for season_array in year_numpy_list:
        season_array = season_array.astype(float)
        year_array = year_array + season_array 
    
    antennafilename = '/opt2/D4D/senegal/data/ContextData/SITE_ARR_LONLAT.CSV'
    outputdir  = '../output/'
    load_antennas(antennafilename)
    file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'
    
    raw_year_array = np.copy(year_array)
    year_array = normalize_array(year_array)
    
    output_folder = '.'

    #check in case the output name is just the name of the file and not the complete filepath
    output_filepath_list = output.split('/')
    output_file_name = output_filepath_list[-1]
    if len(output_filepath_list) > 1:
        del output_filepath_list[-1]
        output_folder = '/'.join([str(x) for x in output_filepath_list])
    
    
    raw_output_filepath = output_folder + '/raw_' + output_file_name
    output_filepath = output_folder + '/' + output_file_name
    
    write_to_csv(raw_output_filepath,file_headers,raw_year_array)
    write_to_csv(output_filepath,file_headers,year_array)

def main(argv):
    filespath = ''
    output = ''
    try:
        opts, args = getopt.getopt(argv,"h:f:o:",["help","filespath=","output="])
    except getopt.GetoptError:
        print 'Syntax error: \n Usage: yearlongmatrix.py  -f <files_path> -o <output_name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print 'yearlongmatrix.py  -f <file_path> -o <output_name>'
            sys.exit()
        elif opt in ("-f", "--filespath"):
            filespath = arg
        elif opt in ("-o", "--output"):
            output = arg

    if filespath == '':
        print 'Syntax error: Filespath can\'t be empty\n Usage: yearlongmatrix.py  -f <file_path> -o <output_name>'
        print ' example filespath: ../output/heatmap/seasons/raw'
        sys.exit(2)
    if output  == '':
        print 'Syntax error: output can\'t be empty\n Usage: yearlongmatrix.py  -f <file_path> -o <output_name>'
        print ' example output: ../output/heatmap/seasons/raw/2013.csv'
        sys.exit(2)    

    generate_year(filespath, output)

if __name__ == "__main__":
    main(sys.argv[1:])

