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

def generate_year(filename,homelocation):
    print "YEAR ******** Path to files: ",filename
    files_list = glob.glob(filename+'/*.csv')
    year_numpy_list = []
    for csv_file in files_list:
        print(csv_file)
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
    year_raw_array = np.copy(year_array)
    year_array = normalize_array(year_array)
    year_file_path=outputdir+'/home_location/nsl/'+homelocation+'/year/2013.csv'
    year_raw_file_path=outputdir+'/home_location/nsl/'+homelocation+'/raw/2013.csv'
    write_to_csv(year_file_path,file_headers,year_array)
    write_to_csv(year_raw_file_path,file_headers,year_raw_array)
    '''
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt/D4D/senegal/data/'

    filename_list = filename.split('_')
    if (filename_list[0] == 'sample'):
        antennafilename = 'SITE_ARR_LONLAT.CSV'
        userfilename = filename
        inputpath = '../data/'
    elif (filename_list[0] == 'SET2'):
        userfilename = 'SET2/raw/' + filename

    load_antennas(inputpath+antennafilename)

    outputdir  = '../output/'
    outputfile = '../output/'+userfilename.split('/')[-1].split('.')[0]
    pickle_file_path = outputfile+'/'+userfilename.split('/')[-1].split('.')[0]+'.pkl'
    load_pickle(pickle_file_path)

    print "Starting process for "+userfilename.split('/')[-1].split('.')[0]

    antennas_array = np.zeros((antennas.shape[0],antennas.shape[0]))

    print "Getting all the data from D4Dusers list"
    for user_id in sorted(users):
        print "processing user ", user_id
        prev_antenna = -1
        for key in sorted(users[user_id].antennas_visited_by_date):
            #print ','.join([str(x) for x in users[user_id].antennas_visited_by_date[key]])
            for antenna in users[user_id].antennas_visited_by_date[key]:
                current_antenna = int(antenna)
                if prev_antenna != -1 and current_antenna != prev_antenna:
                    antennas_array[prev_antenna,current_antenna] = antennas_array[prev_antenna,current_antenna] + 1
                prev_antenna = current_antenna

    #antennas_array = normalize_array(antennas_array)

    file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'
    new_antennas_file_path=outputdir+'/heatmap/raw/'+userfilename.split('/')[-1].split('.')[0]+'-season.csv'
    write_to_csv(new_antennas_file_path,file_headers,antennas_array)
    '''

def main(argv):
    filename = ''
    homelocation = ''
    try:
        opts, args = getopt.getopt(argv,"h:l:f:",["help","location=","filepath="])
    except getopt.GetoptError:
        print 'Syntax error: \n Usage: yearlongmatrix_homelocation.py -l <homelocation> -f <file_path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print 'yearlongmatrix.py  -f <file_path>'
            sys.exit()
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-l", "--location"):
            homelocation = arg

    if filename == '':
        print 'Syntax error: Filename can\'t be empty\n Usage: yearlongmatrix_homelocation.py -l <homelocation>  -f <file_path>'
        print ' example filepath: ../output/home_location/269/raw'
        sys.exit(2)
    if homelocation == '':
        print 'Syntax error: Home location can\'t be empty\n Usage: yearlongmatrix_homelocation.py -l <homelocation>  -f <file_path>'
        print ' example homelocation: 269'
        sys.exit(2)

    generate_year(filename,homelocation)

if __name__ == "__main__":
    main(sys.argv[1:])

