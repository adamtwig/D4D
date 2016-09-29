#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation

         Helper functions imported from --
		home_calc_functions_AT.py

Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt
from home_calc_functions_AT import *

def main():
    
    raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
    sample_dir = '/opt2/D4D/senegal/code/D4D_working/sample_data/'

    if ( len(sys.argv) != 3 ):
        print 'program parameters incorrect'
        print 'usage: ./prog.py filename size'
        sys.exit(2)    
    else:
        filename = sys.argv[1]
	percent_ap = (float)(sys.argv[2])	
        if ('sample' in sys.argv[1]):
            input_file = sample_dir + filename
        else:    
            input_file = raw_dir + filename
        
    data_array_2d = read_csv_to_matrix(input_file)

    user_ids = count_active_ids(data_array_2d, 0)
    site_ids = count_active_ids(data_array_2d, 2)
   
    ant_pairs = np.zeros((max(site_ids), max(site_ids)))

    user_calls = np.zeros((max(user_ids)))

    outgoing_calls = np.zeros((max(site_ids)))

    prev = int(data_array_2d[0][2]) - 1


    for x in range(1, len(data_array_2d)):
    #for x in range(1, 103):
    #for x in range(168769, 169621):

	curr = int(data_array_2d[x][2]) - 1

	user_index = int(data_array_2d[x][0]) - 1
	
	#print "call_num:", x, "moved from", prev, "to", curr

	user_calls[user_index]+=1        

	#if (user_index == 1375):
	#    print "x:",x,data_array_2d[x][:]	

	ant_pairs[prev, curr]+=1

	outgoing_calls[prev]+=1

	prev = curr

    #for i in range(1,max(site_ids)):
#	print "ant_id:", i, "outgoing_calls:",outgoing_calls[i]

    ant_pairs_perc = np.zeros((max(site_ids), max(site_ids)))

    outgoing_count = 0
    total_count = 0
    #percent_ap = 0.001

    #for i in range(1, max(user_ids)):
	#if (user_calls[i] > 1500):
		#print "user_id:", i, "num_calls:", user_calls[i] 


    for i in range(0, 1666):
	for j in range(0, 1666):
		if (outgoing_calls[i] > 0):
			ant_pairs_perc[i,j] = ant_pairs[i,j]/outgoing_calls[i]
		else:
			ant_pairs_perc[i,j] = 0
		#if (ant_pairs_perc[i,j] > percent_ap):			
		if (ant_pairs[i,j] > 0):
			#total_count+=1	
			#print "i:", i, "j:", j,"num_calls:",ant_pairs[i,j], "percent:", ant_pairs_perc[i,j]
			print "i:", i+1, "j:", j+1,"num_calls:",ant_pairs[i,j]
	    		#outgoing_count+=1
    #print "percent_ap:", percent_ap, "outgoing_count:", outgoing_count, "total_count:", total_count	
    
#print "total_count:", total_count
'''
    #out_dir = '../out_data/'

    # aggregrate frequencies and write output to csv
    output_write(out_dir+'out_nofilter', filename, agg_ant_freq(nofilter))
    output_write(out_dir+'out_daytime_', filename, agg_ant_freq(daytime))
    output_write(out_dir+'out_nighttime_', filename, agg_ant_freq(nighttime))
    output_write(out_dir+'out_weekdays_', filename, agg_ant_freq(weekdays))
    output_write(out_dir+'out_weekends_', filename, agg_ant_freq(weekends))
'''
if __name__ == "__main__":
    main()
