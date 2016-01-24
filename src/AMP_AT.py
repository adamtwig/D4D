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

	#uniqueIDs = set(data_array_2d[0:104,2])

	#patterns = np.chararray(104,104)
	#patterns = np.chararray((11,11))
	#patterns = np.array(dtype=object)
	patterns = list()
	#patterns = list(patterns)
	#print patterns

	#for i in range(2,104):
	#	for j in range(2, 104):
	for i in range(104):
		subPatterns = list()
		for j in range(i+1):
			#print i, data_array_2d[i, 2], data_array_2d[j:(i+1), 2]
			#print data_array_2d[j:(i+1), 2]	
			#patterns[i,j] = str(data_array_2d[j:(i+1),2])
			#patterns.append(list(data_array_2d[j:(i+1), 2]))	
			subPatterns.append(list(data_array_2d[j:(i+1), 2]))
		patterns.append(subPatterns)
    #for i in range(len(data_array_2d)):
	#for i in range(104):
	#	print i, data_array_2d[i,0], data_array_2d[i,2]

	#for i in range(len(patterns)):		
	#	for j in range(len(patterns)):
	#		print patterns[i,j]
	#print patterns

	#print set(patterns)
	
	patternDict = {}

	for i in range(1, 104):
		for j in range(104):
			if len(patterns[j]) > i:
				print 1, i, patterns[j][-i]			
				patternDict[i*104+j] = patterns[j][-i]

	#print patternDict
	#wordstring = str(patterns[-1])

	#wordlist = wordstring.split()

	#wordlist = patterns

	#wordfreq = []
	#for w in wordlist:
	#	wordfreq.append(wordlist.count(w))

	#print "String\n" + wordstring +"\n"
	#print "List\n" + str(wordlist) + "\n"
	#print "Frequencies\n" + str(wordfreq) + "\n"
	#print "Pairs\n" + str(zip(wordlist, wordfreq))

	

	#print patterns[:][-1]

	#tPatterns = list(map(list, zip(*patterns)))

	#print tPatterns

'''

    out_dir = '../anon_data/'
    prefix = out_dir+"anon_"
    outfile = open(prefix+filename, 'w')
    for i in range(len(data_array_2d)):
        # add 1 since frequency matrices run from 0 to n-1
        outfile.write(str(data_array_2d[i,0]) + ',' + str(data_array_2d[i,2]) + "\n")
'''

if __name__ == "__main__":
    main()
