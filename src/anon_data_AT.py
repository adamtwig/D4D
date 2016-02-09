#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Output an anonymized version of dataset

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

    out_dir = '../anon_data/'

    prefix = out_dir+"anon_"

    outfile = open(prefix+filename, 'w')
    for i in range(len(data_array_2d)):
        # add 1 since frequency matrices run from 0 to n-1
        outfile.write(str(data_array_2d[i,0]) + ',' + str(data_array_2d[i,2]) + "\n")


if __name__ == "__main__":
    main()
