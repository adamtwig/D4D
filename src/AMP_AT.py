#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: AMP -- Abstract Movement Patterns

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
	sample_dir = '/opt2/D4D/senegal/code/sample_data/'

	if ( len(sys.argv) != 2 ):
		print 'program parameters incorrect'
		print 'usage: ./prog.py filename '
		print 'example dataset: sample_SET2_P01.csv' 
		sys.exit(2)    
	else:
		filename = sys.argv[1]
		if ('sample' in sys.argv[1]):
			input_file = sample_dir + filename
		else:    
			input_file = raw_dir + filename
        
	data_array_2d = read_csv_to_matrix(input_file)

	patterns = list()
	for i in range(104):
		subPatterns = list()
		for j in range(i+1):
			#print i, data_array_2d[i, 2], data_array_2d[j:(i+1), 2]
			#print data_array_2d[j:(i+1), 2]	
			#patterns[i,j] = str(data_array_2d[j:(i+1),2])
			#patterns.append(list(data_array_2d[j:(i+1), 2]))	
			subPatterns.append(list(data_array_2d[j:(i+1), 2]))
		patterns.append(subPatterns)
	
	patternDict = {}

	for i in range(1, 104):
		for j in range(104):
			if len(patterns[j]) > i:
				#print 1, i, patterns[j][-i]			
				#patternDict[i*104+j] = patterns[j][-i]
				if not str(patterns[j][-i]) in patternDict:
					patternDict[str(patterns[j][-i])] = 1
				else:
					patternDict[str(patterns[j][-i])] += 1
	
	#print patternDict

	import operator

	sorted_patternDict = sorted(patternDict.items(), 
							key=operator.itemgetter(1), reverse=True)

	print sorted_patternDict


if __name__ == "__main__":
    main()
