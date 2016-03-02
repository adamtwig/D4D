#!/usr/bin/python

'''
Developer: Matt Lukas
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: uses the aggrigation of AMPs to create an
output file used to calculate the probablity each AMP

InFile Format:
$userID,$AMP,$numOccurences
.
.
.

OutFile Format:
$userID,$totalCalls,numOccurencesForAMP1,numOccurencesForAMP2, ...
.
.
.
-There will be one row for every user.
-The AMPs will be in no specific order

Things to fix:
list initialization
if the UIDs, are not abstracted, there will be issues
	maybe use of a dictionary instead of a list could help here?

	only init the uid and total calls to zero,
		then append everything else can we do this 
		even though the agg results are out of order???

might be easier to directly take the unaggrigated file as input?

writing to the output file takes too long


Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt

def main():
        path_fileIn = "smallAMPaggs.txt"
        path_fileOut = "oSmallAMP_probabilities.txt"

	#variables to make tokenized line use more clear
	UID = 0
	AMP = 1
	OCCUR = 2

        #universal dictionary between users to hold the index of each pattern
	patternIndices  = {} 
	currIndex = 2 #so this can be used directly with userList 0:uid, 1:Total
	#array of lists, each list is one users results
	#for 6 usr, op file was 3000
	userLists = [[0]*100]*10#10 is num users 50 is elements in array?
	
	print "running\n"
        with open(path_fileIn, 'r') as infile:
 		for curLine in infile:
			curLineTknized = curLine.split(',')
			#increment the total number of calls the usr made
			userLists[int(curLineTknized[UID])][1] +=1
			#if the current AMP is not already in the patternIndex
			if not curLineTknized[AMP] in patternIndices:
				patternIndices[curLineTknized[AMP]] = currIndex
				currIndex += 1
			
			#if the pattern is in the users list... it shouldnt be
			if curLineTknized[AMP] in userLists[int(curLineTknized[UID])]:
				print "error, user has duplicate patterns in their aggragation file, exiting"
				return 0
			else: #the pattern is not yet in the users lists
				userLists[int(curLineTknized[UID])][patternIndices.get(curLineTknized[AMP])] = curLineTknized[OCCUR].strip("\n")
			with open(path_fileOut, "w") as outfile:
				for i in range(len(userLists)): 
					for item in userLists:
						outfile.write("%s\n" % str(item))
					outfile.write("\n")
	return 0;

if __name__ == "__main__":
    main()
