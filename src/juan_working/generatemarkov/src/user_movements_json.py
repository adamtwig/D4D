# -*- coding: utf-8 -*-
"""
===================================
GENERATE USER MOVEMENT GEOJSON
===================================
Create a geo_json of movements based on Call Records
"""

import os
import sys
import errno
import getopt
import time
import json
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

def load_home_locations(home_locations_file_path):
    global home_locations_array
    if home_locations_array.size == 0:
        home_locations_array = read_csv_to_matrix(home_locations_file_path)

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

def geo_json_by_user(filename, user_id):
    print "BY USER ******** file:%s user:%d"%(filename,user_id)
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

    print "Starting process for user",user_id

    
    geo_jsons_dict={}
    if user_id in users:
        print "user found"
        user = users[user_id]
        for key in sorted(user.antennas_visited_by_date):
            i = 1
            feature_list=[]
            for antenna in users[user_id].antennas_visited_by_date[key]:
                lat = float(antennas[int(antenna),2])
                lon = float(antennas[int(antenna),3])
                feature = {'type':'Feature', 'geometry':{'type':'Point','coordinates':[lat,lon]},'properties':{'user_id':user_id, 'time':i, 'latitude':lat, 'longitude':lon } }
                feature_list.append(feature)
                #print json.dumps(feature, sort_keys=True, indent=4, separators=(',', ': '))
                i+=1
            geo_json_date={'type': 'FeatureCollection','features': feature_list}
            geo_jsons_dict.update({key:geo_json_date})
    else:
        print "too bad, user doesn't exist"
    
    print "Processed completed, writing json files"
    
    for key in sorted(geo_jsons_dict):
        print "   Writing json for: ",key
        file_path='./data/'+key+'.json'
        
        #checking if the distance path exist
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        #Saving file
        with open(file_path, "w") as f:
            f.write(json.dumps(geo_jsons_dict[key], sort_keys=True, indent=4, separators=(',', ': ')))

    print "Finished creating the jsons" 

def main(argv):
    required_by_user   = False
    filename = ''
    user_id = -1
    days_list = []
    try:
        opts, args = getopt.getopt(argv,"hu:f:",["help","user=","file="])
    except getopt.GetoptError:
        print 'Syntax error: \n Usage: user_movements_json.py -u <user_id> -f <file_name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print 'Usage: user_movements_json.py -u <user_id> -f <file_name>'
            sys.exit()
	elif opt in ("-u", "--user"):
            user_id=int(arg)
            required_by_user=True
        elif opt in ("-f", "--file"):
            filename = arg

    if filename == '':
        print 'Syntax error: Filename can\'t be empty\n Usage: user_movements_json.py -u <user_id> -f <file_name>'
        print ' example filename: sample_SET2_P01.csv'
        sys.exit(2)
    if user_id  < 0:
        print 'Syntax error: user_id has to be a number and it can\'t be empty\n Usage: user_movements_json.py -u <user_id> -f <file_name>'
        print ' example user_id: 0'
        sys.exit(2)

    print(__doc__)
    if required_by_user:
        geo_json_by_user(filename,user_id)

if __name__ == "__main__":
    main(sys.argv[1:])

