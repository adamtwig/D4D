#!/usr/bin/python

'''
Developer: Matt Lukas
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: aggrigating results for 1 user.


Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe

TODO: think of a way to make the 'mer' output in a better order

'''

import numpy as np
import sys
import datetime as dt


def main():
        #dictionary to hold each unique mer and the number of occurences
	results = {} 
	UID = 0
	currentUsr = "-1"
        path_fileOut = "agg_sample3_user10.txt"
        #path_fileIn = "opt2/D4D/senegal/code/D4D_working/output/userAMP_sample6.txt"
	path_fileIn = '../../output/sample3_user10.txt'
	with open(path_fileOut, "w") as outfile:
        	with open(path_fileIn, 'r') as infile:
 			for lineToCheck in infile:
				newUsr = lineToCheck.split(',')[UID].strip()
				#check if we have started a new user,
  				if newUsr == currentUsr:	
					if lineToCheck in results:
						results[lineToCheck] += 1	
                        		#the line is new, add it to the dict if it is not blank
					elif len(lineToCheck) > 3:			
						results[lineToCheck] = 1; #init occurance = 1
				else: # dump the results to the outfile and clear the dict
				        #write the results dict to the outfile
					for line, occur in results.items():
						outfile.write(line.strip('\n')+","+str(occur)+'\n')
					results.clear()
					currentUsr = newUsr
	return 0;

if __name__ == "__main__":
    main()
