#!/usr/bin/python

'''
Developer: Juan Carcamo
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Distance and Time between call data by day.
         Helper functions imported from -- utils.py
Credits: Adam Terwilliger, Grahm Roderick, Jon Leidig,
         , Greg Wolffe
'''

import os
import sys
import errno
import time
import cPickle as pickle
import numpy as np

from pickle import PicklingError
from haversine import haversine
from models import D4Duser
from utils import *

def main():
    antennafilename = 'ContextData/SITE_ARR_LONLAT.CSV'
    userfilename = 'SET2/raw/SET2_P01.CSV'
    inputpath = '/opt2/D4D/senegal/data/'

    if ( len(sys.argv) != 2 ):
        print 'program parameters incorrect'
        print 'usage: ./createusrdistancematrix.py <filename> '
        print 'example dataset: sample_SET2_P01.csv'
        sys.exit(2)
    else:
        filename = sys.argv[1]
        filename_list = filename.split('_') 
        if (filename_list[0] == 'SET2'):
            userfilename = 'SET2/raw/' + filename
        elif (filename_list[0] == 'SET3'):
            userfilename = 'SET3/raw/' + filename
        elif (filename_list[0] == 'sample'):
            antennafilename = 'SITE_ARR_LONLAT.CSV'
            userfilename = filename
            inputpath = '../data/'
        else:
            print 'Not a valid dataset'
            print 'make sure that your file exist at:'
            print '\t /opt2/D4D/senegal/data/<SET[2|3]>/raw/SET<[2|3]>_<name_of_set>.CSV'
            print '\nor if it is a \"sample\" that a file with the name \"sample_<any_name>\" exist at:'
            print '\t../data/'
            sys.exit(2)

    outputfile = '../output/'+userfilename.split('/')[-1].split('.')[0]
    
    antennas = read_csv_to_matrix(inputpath+antennafilename)
    users_raw = read_csv_to_matrix(inputpath+userfilename)
    
    user_ids = count_active_ids(users_raw, 0)
    site_ids = count_active_ids(users_raw, 2)

    userIDdict = {}
    usersResultDict = {}    

    # need to create a dictionary for userIDs in SET3
    for i in range(len(user_ids)):
        userIDdict[user_ids[i]] = i

    for x in range(len(users_raw)):
        try:
            original_userID = int(users_raw[x][0])
        except ValueError:
            continue
        user_index = userIDdict[original_userID]
        antenna_index = int(users_raw[x][2])

        date = get_date(users_raw[x][1])
        ic = date.isocalendar()
        tt = date.timetuple()    
  
        current_position = (float(antennas[antenna_index][3]), float(antennas[antenna_index][2]))

        features_index = date.strftime("%m-%d-%Y")
        if not user_index in usersResultDict:
            new_user = D4Duser()

            new_user.user_id = user_index
            usersResultDict.update({user_index:new_user})
        
        current_user = usersResultDict[user_index]
        
        if not features_index in current_user.antennas_visited_by_date:
            current_user.antennas_visited_by_date.update({features_index:[antenna_index]})
        else:
            current_user.antennas_visited_by_date[features_index].append(antenna_index)
       
        if not features_index in current_user.distance_features:
            current_user.distance_features.update({features_index:[0.0]})
        else:
            # lets calculate the distance between current call and last call!!!
            prev_position = current_user.last_known_pos
            current_user.distance_features[features_index].append(haversine(current_position, prev_position)*1000) 
        
        current_user.last_known_pos = current_position
        
        if not features_index in current_user.time_features:
            current_user.time_features.update({features_index:[0]})
        else:
            # lets calculate the time difference  between current call and last call!!!
            prev_date = current_user.last_known_date
            prev_date_ts = time.mktime(prev_date.timetuple())
            current_date_ts = time.mktime(date.timetuple()) 
            current_user.time_features[features_index].append(int(current_date_ts - prev_date_ts))
        
        current_user.last_known_date = date


    print "Saving D4Dusers list pickle for "+userfilename.split('/')[-1].split('.')[0]
    new_file_path=outputfile+'/'+userfilename.split('/')[-1].split('.')[0]+'.pkl'
    if not os.path.exists(os.path.dirname(new_file_path)):
        try:
            os.makedirs(os.path.dirname(new_file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    try:
        pickle.dump(usersResultDict, open(new_file_path,'wb'))
    except PicklingError:
        print "Error saving objects to pickle"

    print "D4Dusers list saved"

if __name__ == "__main__":
    main()

