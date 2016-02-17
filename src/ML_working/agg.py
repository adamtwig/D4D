#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: aggrigating results for 1 user.


Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt

def main():
        #dictionary to hold each unique mer and the number of occurences
	results = {} 
	
	#sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'
	#out_ant_dir = '/opt2/D4D/senegal/code/output'

        path_fileOut = "aggregations.txt"
        path_fileIn = "/opt2/D4D/senegal/code/output/ML_testing.txt"
        with open(path_fileIn, 'r') as infile:
 		for lineToCheck in infile:
			if lineToCheck in results:
				results[lineToCheck] += 1	
                        #the line is new, add it to the dict if it is not blank
			elif len(lineToCheck) > 3:			
				results[lineToCheck] = 1; #init occurance = 1

        '''write the results dict to the outfile'''
	with open("aggregations.txt", "w") as outfile:
		for line, occur in results.items():
			outfile.write(line.strip('\n')+", "+str(occur)+'\n')
	return 0;

if __name__ == "__main__":
    main()
