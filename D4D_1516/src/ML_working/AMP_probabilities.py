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


Credits: Michael Baldwin, Bishal Chamlin, Jon Leidig,
         Morgan Oneka, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt

def main():
        path_fileIn = "tstAMPagg.txt"
        path_fileOut = "oSmallAMP_probabilities.txt"

	#variables to make tokenized line use more clear
	UID = 0
	AMP = 1
	OCCUR = 2
	NUM_CALLS = 1

        #universal dictionary between users to hold the index of each pattern
	patternIndices  = {} 
	#list of userlists
	userLists = [[]]
	curUsrList = []
	currIndex = 2 #so this can be used directly with userList 0:uid, 1:Total
	#array of lists, each list is one users results
	cUID = -1
	print "running\n"
        with open(path_fileIn, 'r') as infile:
 		for curLine in infile:
			curLineTknized = curLine.split(',')
			if(cUID != curLineTknized[UID]): #we have a new user
				userLists.append(curUsrList) #append old list
				curUsrList = []
				curUsrList.append(curLineTknized[UID])
				curUsrList.append(0)
				for l in range(currIndex-2):
					curUsrList.append("0")
					curUsrList[0] = curLineTknized[UID]
			cUID = curLineTknized[UID]
			cAMP = curLineTknized[AMP].strip("\n")		
			cOCCUR = curLineTknized[OCCUR].strip("\n")
					
			#increment the total number of calls the usr made
			curUsrList[NUM_CALLS] += int(cOCCUR)
			#if the current AMP is not already in the patternIndex
			if not cAMP in patternIndices:
				patternIndices[cAMP] = currIndex
				currIndex += 1
				curUsrList.append(cOCCUR)
		        else: #the pattern is in the patternIndex
				curUsrList[patternIndices.get(cAMP)] = cOCCUR
		userLists.append(curUsrList)
		orderIndices = sorted(patternIndices.items(), key=lambda x: x[1])
		print orderIndices
		print str(userLists)
		with open(path_fileOut, "w") as outfile:
			outfile.write("userID, total Calls, ")
			for pattern in orderIndices:
				outfile.write(str(pattern[0])+', ')
			outfile.write('\n')

			for ul in userLists:
				if ul:
					for i in range(len(orderIndices)+2):#+2 because two of the cols are uid and totalCalls
 						if i < len(ul):
							outfile.write(str(ul[i])+ ', ')
						else:
							outfile.write('0, ')  
				#outfile.write( str(i).strip('[]') + '\n')			
				outfile.write("\n")
	return 0;

if __name__ == "__main__":
    main()
