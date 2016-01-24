#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation

         Helper functions imported from --
		home_calc_functions_AT.py

Credits: Michael Baldwin, Bishal Chamling, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt
from home_calc_functions_BC import *

def main():
    
    raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
    sample_dir = '/opt2/D4D/senegal/code/D4D_working/sample_data/'

    if ( len(sys.argv) != 2 ):
        print 'program parameters incorrect'
        print 'usage: ./prog.py filename '
        sys.exit(2)    
    else:
        filename = sys.argv[1]
        if ('sample' in sys.argv[1]):
            input_file = sample_dir + filename
        else:    
            input_file = raw_dir + filename
        
    data_array_2d = read_csv_to_matrix(input_file)

    user_ids = count_active_ids(data_array_2d, 0)
    site_ids = count_active_ids(data_array_2d, 2)
    ''' 
    print user_ids, site_ids
    print max(user_ids), max(site_ids)
    print len(user_ids), len(site_ids)
    '''
    # create five matrices using max id because
    # ids are ordered with few missing (for antennas) 
    nofilter, daytime, nighttime, weekdays, weekends = [np.zeros(
	(max(user_ids), max(site_ids))) for _ in xrange(5)] 

    today7am = create_date(7, 0, 0)
    today7pm = create_date(19, 0, 0)

    for x in range(len(data_array_2d)):

        # subtract 1 since original data runs from 1 to n
        user_index = int(data_array_2d[x][0]) - 1
	antenna_index = int(data_array_2d[x][2]) - 1

        date = get_date(data_array_2d[x][1])
        
        # for every pair of user/ant increment 1
        nofilter[user_index, antenna_index]+=1

        if (date.time() > today7am.time() and date.time() < today7pm.time()):
            daytime[user_index, antenna_index]+=1
        else:
            nighttime[user_index, antenna_index]+=1

        if (date.weekday() <= 4):
            weekdays[user_index, antenna_index]+=1
        else:
            weekends[user_index, antenna_index]+=1
    
    out_dir = 'out_data_BC/'

    # aggregrate frequencies and write output to csv
    output_write(out_dir+'out_nofilter', filename, agg_ant_freq(nofilter))
    output_write(out_dir+'out_daytime_', filename, agg_ant_freq(daytime))
    output_write(out_dir+'out_nighttime_', filename, agg_ant_freq(nighttime))
    output_write(out_dir+'out_weekdays_', filename, agg_ant_freq(weekdays))
    output_write(out_dir+'out_weekends_', filename, agg_ant_freq(weekends))

if __name__ == "__main__":
    main()
