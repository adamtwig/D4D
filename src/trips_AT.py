#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Create trips file for each day

         Helper functions imported from --
		home_calc_functions_AT.py

Credits: Jonathan Leidig, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt
from uHome_calc_functions_AT import *
np.set_printoptions(threshold='nan')

def main():

	#raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
	raw_dir = '/opt2/D4D/senegal/data/'
	sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'
	out_dir = '../output/trips/'


	if ( len(sys.argv) != 2 ):
		print 'program parameters incorrect'
		print 'usage: ./prog.py filename '
		print 'example dataset: sample_SET2_P01.csv'
		sys.exit(2)
	else:
		filename = sys.argv[1]
	
		if ('SET2' in sys.argv[1]):
		    raw_dir = raw_dir + 'SET2/raw/'
		else:
		    raw_dir = raw_dir + 'SET3/raw/'

		if ('sample' in sys.argv[1]):
		    input_file = sample_dir + filename
	            out_dir = out_dir + 'sample_trips/'    
                        
        	else:    
		    input_file = raw_dir + filename
	            out_dir = out_dir + 'full_trips/'    
        
	data_array_2d = read_csv_to_matrix(input_file)

	user_ids = count_active_ids(data_array_2d, 0)
	site_ids = count_active_ids(data_array_2d, 2)
    
        dayTripDict = {}
        
        for x in range(len(data_array_2d)):
	    
            user_prev = int(data_array_2d[x-1][0])
            time_prev = get_date(data_array_2d[x-1][1])
            ant_prev = int(data_array_2d[x-1][2])
            user_curr = int(data_array_2d[x][0])
            time_curr = get_date(data_array_2d[x][1])
            ant_curr = int(data_array_2d[x][2])
        
            day_curr = time_curr.timetuple().tm_yday	
            
	    if user_prev == user_curr and ant_prev != ant_curr:
                outString = str(user_curr)+","+str(ant_prev)+","+str(ant_curr)+","+str(time_prev)+","+str(time_curr)
                if day_curr not in dayTripDict:
                    dayTripDict[day_curr] = [outString]
                else:
                    dayTripDict[day_curr].append(outString)

        for day in dayTripDict:
            outfile = open(out_dir+'trips_'+str(day)+'.csv', 'w')
            for trip in dayTripDict[day]:
                outfile.write(trip+"\n")

def output_write(prefix, filename, antID_array):
    outfile = open(prefix+filename, 'w')
    for i in range(len(antID_array)):
        # add 1 since frequency matrices run from 0 to n-1
        outfile.write(str(i + 1) + ',' + str(antID_array[i]) + "\n")

if __name__ == "__main__":
    main()
