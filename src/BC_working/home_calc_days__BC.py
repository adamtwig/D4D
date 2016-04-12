#!/usr/bin/python

import numpy as np
import csv
import datetime as dt
from home_calc_days_functions_BC import *


def main():
    raw_dir = '/opt2/D4D/senegal/data/SET3/raw/'
    sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'

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




	nofilter = [np.zeros(
		(len(user_ids), max(site_ids))) for _ in xrange(5)]

	# get list of dates

	#output directory
	out_ant_dir = "/opt2/D4D/senegal/code/D4D_working/src/BC_working/out_data_BC/out_data/output_new/"


	def get_date1(timestamp):
    		return dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

#number of days
	'''
	days =[]
	for x in range(len(data_array_2d)):
    		date = get_date1(data_array_2d[x][1])
    		days.append(date.day)
    		days.sort()
	'''
	for y in range(2):
    		y=y+1
    		days = []
    		for line in data_array_2d:

        		if(y == (get_date1(line[1])).day):
            			days.append(line)


    		for x in range(len(days)):

        # subtract 1 since original data runs from 1 to n
		#user_index = int(data_array_2d[x][0]) - 1
				user_index = int(days[x][0])
				antenna_index = int(days[x][2]) - 1

				date = get_date1(days[x][1])

				nofilter[user_index, antenna_index]+=1
				agg_ant = agg_ant_freq(nofilter)



	# get user home location and write output to csv

	# aggregrate frequencies by antenna and write output to csv

				ant_output_write(out_ant_dir+'nofilter_' + str(y)+ '_', filename , agg_ant_freq(nofilter))

if __name__ == "__main__":
    main()

