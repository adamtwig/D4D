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
	out_user_dir = '../output/days/'
	out_site_dir = '../output/days/'


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
        
	# inefficient looping over file first time to put in matrix
	data_array_2d = read_csv_to_matrix(input_file)
	
	user_ids = count_active_ids(data_array_2d, 0)
	#site_ids = count_active_ids(data_array_2d, 2)
	site_ids = range(123+1+1)

	#user_ids = range(146352+1)
	#site_ids = range(123+1)

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
		(len(user_ids), max(site_ids)+1, numDaysInMonth)) for _ in xrange(5)] 

	# for different defintions of home need 7pm to 7am
	today7am = create_date(7, 0, 0)
	today7pm = create_date(19, 0, 0)

	for x in range(len(data_array_2d)):
		# using dictionary for efficient storage of userIDs
		original_userID = int(data_array_2d[x][0])
		user_index = userIDdict[original_userID]
		#user_index = int(data_array_2d[x][0]) - 1
        
		# subtract 1 since original data runs from 1 to n
		#site_index = int(data_array_2d[x][2]) - 1
		site_index = int(data_array_2d[x][2]) + 1

		date = get_date(data_array_2d[x][1])
		ic = date.isocalendar()
		tt = date.timetuple()	
		
		# week id from 1 to 52
		weekOfYear = ic[1]

		# day id from 1 to 365
		dayOfYear = tt.tm_yday       

        # for every pair of user/site increment 1
		nofilter[user_index, site_index, dayOfYear]+=1

	# aggregrate frequencies by site and write output to csv
	#site_output_write(out_site_dir+'out_nofilter', filename, agg_site_freq(nofilter))

	# get user home location and write output to csv
	#user_output_write(out_user_dir+'out_user_nofilter_', filename, 
	#				agg_user_freq(nofilter), userIDdict2)

	user_days = agg_user_freq(nofilter)

	csv_file = '../output/user/out_data/out_user_nofilter_SET3_M01.CSV'
 
	# get dict of home location for each user in January
	user_months = {}
	with open(csv_file,'rb') as myfile:
		for line in myfile:
			list_line = line.strip('\n"\r').split(',')
			user = int(list_line[0])
			home = int(list_line[1])
			if user not in user_months:
				user_months[user] = home

	user_daysCopy = user_days

	# replace 0s with monthly home location
	for key in userIDdict2:
		#print key, userIDdict2[key]
		for day in range(31+1):
			if user_days[key,day] == 0:
				user_daysCopy[key,day] = user_months[userIDdict2[key]]
			else:
				user_daysCopy[key,day] -= 1
			#print key, day, userIDdict2[key], user_daysCopy[key,day], user_months[userIDdict2[key]]

	# output matrix (extra padding for 0 indexing)
	arrDays = np.zeros([123+1,123+1,30+1])
	
	# find migrations by comparing currDay and nextDay to see diff
	for key in userIDdict2:
		for day in range(1, 31):
			currDayArr = user_daysCopy[key, day]
			nextDayArr = user_daysCopy[key, day+1]
			#print key, day, day+1, currDayArr, nextDayArr
			arrDays[currDayArr, nextDayArr, day] += 1

	arrDaysCopy = arrDays.astype(int)

	import csv

	outputLoc = "../output/dailyMigrationTest_AT.csv"

	outputFile = csv.writer(open(outputLoc, 'w'))
	outputFile.writerow(['Arr1', 'Arr2', 'Day', 'NumMigratedArr1toArr2onDay','TotalMigratedFromArr1onDay','Percent'])
	# output migrations
	for arr1 in range(1, 124):
		for arr2 in range(1, 124):
			for day in range(1, 31):
				currVal = arrDaysCopy[arr1, arr2, day]
				total = sum(arrDaysCopy[arr1, :, day])
				if total == 0:
					percent = 0.0
				else:
					percent = float(currVal) / float(total)
				#print arr1, arr2, day, currVal, total, float(currVal) / float(total) 
				outputFile.writerow([arr1, arr2, day, currVal, total, percent])

	# ideas for output include all, floats, and only non-self migration

if __name__ == "__main__":
    main()
