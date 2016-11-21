# -*- coding: utf-8 -*-
"""
===================================
GENERATE MARKOV MATRIX
===================================
Create matrix of transition probabilities based on Call Records
"""

import os
import sys
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
            if i != 0:
                #need to eliminate column 0, there's no antenna 0
                row_to_list = [str(x) for x in row]
                row_to_list.pop(0)
                row_str = str(i)+','+','.join(row_to_list)+'\n'
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

def generate_season(filename):
    print "SEASON ******** ",filename
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt2/D4D/senegal/data/'

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

    raw_antennas_array = np.copy(antennas_array)
    antennas_array = normalize_array(antennas_array)

    file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'
    
    new_raw_antennas_file_path=outputdir+'/heatmap/nsl/raw/seasons/'+userfilename.split('/')[-1].split('.')[0]+'-season.csv'
    new_antennas_file_path=outputdir+'/heatmap/nsl/seasons/'+userfilename.split('/')[-1].split('.')[0]+'-season.csv'
    write_to_csv(new_raw_antennas_file_path,file_headers,raw_antennas_array)
    write_to_csv(new_antennas_file_path,file_headers,antennas_array)

def generate_season_raw(filename):
    print "SEASON ******** ",filename
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt2/D4D/senegal/data/'

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
    new_antennas_file_path=outputdir+'/heatmap/nsl/seasons/raw/'+userfilename.split('/')[-1].split('.')[0]+'-season.csv'
    write_to_csv(new_antennas_file_path,file_headers,antennas_array)

def generate_weekends(filename):
    print "WEEKDAY v. WEEKENDS ******** ",filename
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt2/D4D/senegal/data/'

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

    antennas_weekdays_array = np.zeros((antennas.shape[0],antennas.shape[0]))
    antennas_weekends_array = np.zeros((antennas.shape[0],antennas.shape[0]))
    
    print "Getting all the data from D4Dusers list"
    for user_id in sorted(users):
        print "processing user ", user_id
        prev_antenna = -1
        for key in sorted(users[user_id].antennas_visited_by_date):
            #print 'day:',key
            date = get_key_date(key)
            for antenna in users[user_id].antennas_visited_by_date[key]:
                current_antenna = int(antenna)
                if prev_antenna != -1 and current_antenna != prev_antenna:
                    if date.weekday() <= 4:
                        antennas_weekdays_array[prev_antenna,current_antenna] = antennas_weekdays_array[prev_antenna,current_antenna] + 1
                    else:
                        antennas_weekends_array[prev_antenna,current_antenna] = antennas_weekends_array[prev_antenna,current_antenna] + 1
                prev_antenna = current_antenna

    raw_antennas_weekdays_array = np.copy(antennas_weekdays_array)
    raw_antennas_weekends_array = np.copy(antennas_weekends_array)

    antennas_weekdays_array = normalize_array(antennas_weekdays_array)
    antennas_weekends_array = normalize_array(antennas_weekends_array)    

    file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'

    new_raw_antennas_weekdays_file_path=outputdir+'/heatmap/nsl/raw/weekdays/'+userfilename.split('/')[-1].split('.')[0]+'-weekdays.csv'
    new_raw_antennas_weekends_file_path=outputdir+'/heatmap/nsl/raw/weekends/'+userfilename.split('/')[-1].split('.')[0]+'-weekends.csv'

    new_antennas_weekdays_file_path=outputdir+'/heatmap/nsl/weekdays/'+userfilename.split('/')[-1].split('.')[0]+'-weekdays.csv'
    new_antennas_weekends_file_path=outputdir+'/heatmap/nsl/weekends/'+userfilename.split('/')[-1].split('.')[0]+'-weekends.csv'

    write_to_csv(new_raw_antennas_weekdays_file_path,file_headers,raw_antennas_weekdays_array)
    write_to_csv(new_raw_antennas_weekends_file_path,file_headers,raw_antennas_weekends_array)
    write_to_csv(new_antennas_weekdays_file_path,file_headers,antennas_weekdays_array)
    write_to_csv(new_antennas_weekends_file_path,file_headers,antennas_weekends_array)


def generate_days(filename, days_list):
    print "DAYS ********", filename, days_list
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt2/D4D/senegal/data/'

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

    antennas_days_array = np.zeros((antennas.shape[0],antennas.shape[0]))
    antennas_others_array = np.zeros((antennas.shape[0],antennas.shape[0]))

    print "Getting all the data from D4Dusers list"
    for user_id in sorted(users):
        print "processing user ", user_id
        prev_antenna = -1
        for key in sorted(users[user_id].antennas_visited_by_date):
            for antenna in users[user_id].antennas_visited_by_date[key]:
                current_antenna = int(antenna)
                if prev_antenna != -1 and current_antenna != prev_antenna:
                    if key in days_list:
                        antennas_days_array[prev_antenna,current_antenna] = antennas_days_array[prev_antenna,current_antenna] + 1
                        #print "antenna_in_days[%d,%d] count up"
                    else:
                        antennas_others_array[prev_antenna,current_antenna] = antennas_others_array[prev_antenna,current_antenna] + 1
                        #print "antenna_others[%d,%d] count up"
                prev_antenna = current_antenna

    raw_antennas_days_array = np.copy(antennas_days_array)
    raw_antennas_others_array = np.copy(antennas_others_array)

    antennas_days_array = normalize_array(antennas_days_array)
    antennas_others_array = normalize_array(antennas_others_array)

    file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'
    days_list_name = '_'.join([str(x) for x in days_list])

    new_raw_antennas_days_file_path=outputdir+'/heatmap/nsl/raw/days/'+userfilename.split('/')[-1].split('.')[0]+'_'+days_list_name+'_days.csv'
    new_raw_antennas_others_file_path=outputdir+'/heatmap/nsl/raw/days/'+userfilename.split('/')[-1].split('.')[0]+'_other_days.csv'

    new_antennas_days_file_path=outputdir+'/heatmap/nsl/days/'+userfilename.split('/')[-1].split('.')[0]+'_'+days_list_name+'_days.csv'
    new_antennas_others_file_path=outputdir+'/heatmap/nsl/days/'+userfilename.split('/')[-1].split('.')[0]+'_other_days.csv'

    write_to_csv(new_raw_antennas_days_file_path,file_headers,raw_antennas_days_array)
    write_to_csv(new_raw_antennas_others_file_path,file_headers,raw_antennas_others_array)
    write_to_csv(new_antennas_days_file_path,file_headers,antennas_days_array)
    write_to_csv(new_antennas_others_file_path,file_headers,antennas_others_array)

def main(argv):
    required_raw   = False
    required_season   = False
    required_weekends = False
    required_days     = False
    filename = ''
    days_list = []
    try:
        opts, args = getopt.getopt(argv,"hrswd:f:",["help","raw","season","weekends","days=","file="])
    except getopt.GetoptError:
        print 'Syntax error: \n Usage: generatemarkov.py [[ -r|--raw] | [-s|--season] | [-w|--weekends] | [-d|--days=]  <comma sep list_dates>] -f <file_name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print 'generatemarkov.py [[-r|--raw] | [-s|--season] | [-w|--weekends] | [-d|--days=]  <comma sep list_dates>] -f <file_name>'
            sys.exit()
	elif opt in ("-r", "--raw"):
            required_raw = True
        elif opt in ("-s", "--season"):
            required_season = True
        elif opt in ("-w", "--weekends"):
            required_weekends = True
        elif opt in ("-d", "--days"):
            required_days = True
            days_list = [x.strip() for x in arg.split(',')]
            print days_list
        elif opt in ("-f", "--file"):
            filename = arg

    if filename == '':
        print 'Syntax error: Filename can\'t be empty\n Usage: generatemarkov.py [[-r|--raw] | [-s|--season] | [-w|--weekends] | [-d|--days=]  <comma sep list_dates>] -f <file_name>'
        print ' example filename: sample_SET2_P01.csv'
        sys.exit(2)

    if not required_raw and not required_season and not required_weekends and not required_days:
        print 'Syntax error: Please use at least of the flags: season, weekends or days\n Usage: generatemarkov.py [[-r|--raw] | [-s|--season] | [-w|--weekends] | [-d|--days=]  <comma sep list_dates>] -f <file_name>'
        print ' example: generatemarkov.py -s -f  sample_SET2_P01.csv'
        sys.exit(2)

    print(__doc__)
    if required_raw:
        generate_season_raw(filename)
    if required_season:
        generate_season(filename)
    if required_weekends:
        generate_weekends(filename)
    if required_days:
        if not days_list:
            print 'Syntax error: For days please provide at least one day\n Usage: generatemarkov.py [[-s|--season] | [-w|--weekends] | [-d|--days=]  <comma sep list_dates>] -f <file_name>'
            print ' example: generatemarkov.py -d "01-07-2013, 01-08-2013" -f  sample_SET2_P01.csv'
            sys.exit(2)
        generate_days(filename, days_list)

if __name__ == "__main__":
    main(sys.argv[1:])

