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

    pickle_file_path = outputfile+'/'+userfilename.split('/')[-1].split('.')[0]+'.pkl'
    pkl_file = open(pickle_file_path, 'rb')
    users = pickle.load(pkl_file)
    pkl_file.close()

    print "Starting process for "+userfilename.split('/')[-1].split('.')[0] 

    distance_data_dict={} #used to store the distance_index data for result
    time_data_dict={} #used to store the distance_index data for result


    print "Getting all the data from D4Dusers list"
    #create a dictionary with results by
    for user_id in sorted(users):
        print "processing user ", user_id
        for key in sorted(users[user_id].distance_features):
            if not key in distance_data_dict:
                distance_data_dict.update({key:[str(user_id)+','+users[user_id].get_one_feature_str(feature_key=key)]})
            else:
                distance_data_dict[key].append(str(user_id)+','+users[user_id].get_one_feature_str(feature_key=key))

            if not key in time_data_dict:
                time_data_dict.update({key:[str(user_id)+','+users[user_id].get_one_feature_str(feature_name='time',feature_key=key)]})
            else:
                time_data_dict[key].append(str(user_id)+','+users[user_id].get_one_feature_str(feature_name='time',feature_key=key))

    print "Saving distance and time data to csv"    
    for key in sorted(distance_data_dict):
        print "   Writing time and distance files for: ",key
        new_distance_file_path=outputfile+'/distance/'+key+'.csv'
        new_time_file_path=outputfile+'/time/'+key+'.csv'

        #checking if the distance path exist
        if not os.path.exists(os.path.dirname(new_distance_file_path)):
            try:
                os.makedirs(os.path.dirname(new_distance_file_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        #checking if the time path exist
        if not os.path.exists(os.path.dirname(new_time_file_path)):
            try:
                os.makedirs(os.path.dirname(new_time_file_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        #Saving distances
        with open(new_distance_file_path, "w") as f:
            f.write('\n'.join(distance_data_dict[key]))
        #Saving times
        with open(new_time_file_path, "w") as f:
            f.write('\n'.join(time_data_dict[key]))

    print "Finished creating the csv"        

    #outfile = open(outputfile+'_result.csv', 'w')
    #for user_id in sorted(usersResultDict):
        #print "processing user ", user_id
        ####### Naive print
        #outfile.write(str(user_id)+","+usersResultDict[user_id].get_features_str() + "\n")
        #outfile.write(str(user_id)+","+usersResultDict[user_id].get_features_str('time') + "\n")
        #outfile.write(str(user_id)+","+usersResultDict[user_id].get_features_headers_str() + "\n")

        ##### NUMPY TEST
        #distances = np.fromstring(usersResultDict[user_id].get_features_str(), dtype=np.float64 , sep=',')
        #times = np.fromstring(usersResultDict[user_id].get_features_str('time'), dtype=np.int32, sep=',')
        #days = np.array(usersResultDict[user_id].get_features_headers_str().split(','))
        #user_array = np.array([days,distances,times])
        #print user_array.T

        ##### Class test
        #tmp_user_distances = usersResultDict[user_id].distance_features
        #for distance_key in sorted(tmp_user_distances):
        #     print user_id,",",usersResultDict[user_id].get_one_feature_str(feature_key=distance_key)
        #print user_id,",",usersResultDict[user_id].get_features_str()
        #print user_id,",",usersResultDict[user_id].get_features_str('time')
        #print user_id,",",usersResultDict[user_id].get_features_headers_str()
        #usersResultDict[user_id].print_user()
    #outfile.close() 

if __name__ == "__main__":
    main()

