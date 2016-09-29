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
	#site_ids = count_active_ids(data_array_2d, 2)

	print sys.argv[1]+", "+str(len(user_ids))

if __name__ == "__main__":
    main()
