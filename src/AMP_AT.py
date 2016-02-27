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
from uHome_calc_functions_AT import *

def main():
    
	raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
	sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'

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

	patAmount = len(data_array_2d)
	#patAmount = 1000

	#windowSize = 10

	#for i in range(patAmount):
	#	print i, data_array_2d[i] 
	'''	
			if i > patAmount - (windowSize+1):
				endWindow = i + patAmount - (patAmount - windowSize+1)
			else:
				endWindow = 
'''

	ampList = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

	ampDict = {}

	for i in range(patAmount):
		windowSize = 10
		if i > (patAmount - windowSize):
			windowSize = patAmount - i
		for j in range(1,windowSize+1):
			userPatDict = {}
			userPatString = ""
			ampID = 0
			for k in data_array_2d[i:i+j,2]:
				if k in userPatDict:
					userPatString+=userPatDict[k]
				else:
					userPatDict[k] = ampList[ampID]
					userPatString+=userPatDict[k]
					ampID+=1

			#print str(data_array_2d[i,0])+","+str(data_array_2d[i:i+j,2])
			print str(data_array_2d[i,0])+","+userPatString
			'''
			ampKey = str(data_array_2d[i,0])+","+str(data_array_2d[i:i+j,2])
			if ampKey in ampDict:
				ampDict[ampKey] += 1
			else:
				ampDict[ampKey] = 1

	print ampDict
	'''
	#patterns = list()
	#userWindow = 1
	#windowStart = 1
	#for i in range(887):
	#for i in range(patAmount):	
		#user_index = int(data_array_2d[i][0])
		#subPatterns = list()
		#if userWindow != int(user_index):
		#	userWindow = user_index
		#	windowStart = i
		#for j in range(i+1):
		#for j in range(1,11):	
			#print i, data_array_2d[i, 0],
			#print i,",",j,",",data_array_2d[i, 0],",",data_array_2d[j:(i+1), 2]	
			#print i, j, data_array_2d[i,0],data_array_2d[i:(i+j), 2]
			#patterns[i,j] = str(data_array_2d[j:(i+1),2])
			#patterns.append(list(data_array_2d[j:(i+1), 2]))	
			#userIndex = data_array_2d[i, 0]
			#patternIndex = data_array_2d[j:(i+1),2]
			#subPatterns.append(list(data_array_2d[j:(i+1), 2]))
			#subPatterns.append(userIndex+str(patternIndex))
		#patterns.append(subPatterns)
	
	#print patterns
'''
	patternDict = {}

	#for i in range(1, 887):
	#	for j in range(887):
	for i in range(1, 150):
		for j in range(150):
			if len(patterns[j]) > i:
				#print 1, i, patterns[j][-i]			
				#patternDict[i*104+j] = patterns[j][-i]
				if not patterns[j][-i] in patternDict:
					patternDict[patterns[j][-i]] = 1
				else:
					patternDict[patterns[j][-i]] += 1
	
	#print patternDict

	import operator

	sorted_patternDict = sorted(patternDict.items(), 
							key=operator.itemgetter(1), reverse=True)

	#print sorted_patternDict
'''

if __name__ == "__main__":
    main()
