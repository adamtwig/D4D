#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation

         Helper functions imported from --
		days_functions_AT.py

Credits: Michael Baldwin, Bishal Chamling, Jon Leidig,
         Matt Lukas, Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt
from days_functions_AT import *
np.set_printoptions(threshold='nan')

def main():

	#raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
	raw_dir = '/opt2/D4D/senegal/data/'
	sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'
	out_user_dir = '../output/user/'
	out_site_dir = '../output/'


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
			out_user_dir = out_user_dir + 'sample_out_data/'
			out_site_dir = out_site_dir + 'sample_out_data/'
		else:    
			input_file = raw_dir + filename
			out_user_dir = out_user_dir + 'out_data/'
			out_site_dir = out_site_dir + 'out_data/'
        
	# inefficient looping over file first time to get matrix dimensions
	data_array_2d = read_csv_to_matrix(input_file)
	user_ids = count_active_ids(data_array_2d, 0)
	site_ids = count_active_ids(data_array_2d, 2)

	# need to create a dictionary for userIDs in SET3
	# since userIDs are not in order
	userIDdict = {}
	userIDdict2 = {}
	for i in range(len(user_ids)):
		userIDdict[user_ids[i]] = i
		userIDdict2[i] = user_ids[i]

	# use January to start
	numDaysInMonth = 31 + 1

    # create five matrices using max id because
    # ids are ordered with few missing (for sites) 
	nofilter, daytime, nighttime, weekdays, weekends = [np.zeros(
		(len(user_ids), max(site_ids), numDaysInMonth)) for _ in xrange(5)] 

	# for different defintions of home need 7pm to 7am
	today7am = create_date(7, 0, 0)
	today7pm = create_date(19, 0, 0)

	for x in range(len(data_array_2d)):
		# using dictionary for efficient storage of userIDs
		original_userID = int(data_array_2d[x][0])
		user_index = userIDdict[original_userID]
		#user_index = int(data_array_2d[x][0]) - 1
        
		# subtract 1 since original data runs from 1 to n
		site_index = int(data_array_2d[x][2]) - 1

		date = get_date(data_array_2d[x][1])
		ic = date.isocalendar()
		tt = date.timetuple()	
		
		# week id from 1 to 52
		weekOfYear = ic[1]

		# day id from 1 to 365
		dayOfYear = tt.tm_yday       

        # for every pair of user/site increment 1
		nofilter[user_index, site_index, dayOfYear]+=1

		# if wsite to include other definitions of home, uncomment
		'''
		if (date.time() > today7am.time() and date.time() < today7pm.time()):
			daytime[user_index, site_index]+=1
		else:
			nighttime[user_index, site_index]+=1

		if (date.weekday() <= 4):
			weekdays[user_index, site_index]+=1
		else:
			weekends[user_index, site_index]+=1
    	'''

	# aggregrate frequencies by site and write output to csv
	#site_output_write(out_site_dir+'out_nofilter', filename, agg_site_freq(nofilter))

	'''
	site_output_write(out_site_dir+'out_daytime_', filename, agg_site_freq(daytime))
	site_output_write(out_site_dir+'out_nighttime_', filename, agg_site_freq(nighttime))
	site_output_write(out_site_dir+'out_weekdays_', filename, agg_site_freq(weekdays))
	site_output_write(out_site_dir+'out_weekends_', filename, agg_site_freq(weekends))
	'''

	# get user home location and write output to csv
	user_output_write(out_user_dir+'out_user_nofilter_', filename, 
					agg_user_freq(nofilter), userIDdict2)
	'''
	user_output_write(out_user_dir+'out_user_daytime_', filename,
					agg_user_freq(daytime), userIDdict2)
	user_output_write(out_user_dir+'out_user_nighttime_', filename,
					agg_user_freq(nighttime), userIDdict2)
	user_output_write(out_user_dir+'out_user_weekdays_', filename, 
					agg_user_freq(weekdays), userIDdict2)
	user_output_write(out_user_dir+'out_weekends_', filename,
					agg_user_freq(weekends), userIDdict2)
	'''

if __name__ == "__main__":
    main()
