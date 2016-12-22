#!/usr/bin/python

'''
Developer: Adam Terwilliger
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Create trips file for each day

         Helper functions imported from --
		home_calc_functions_AT.py

Credits: Jonathan Leidig, Greg Wolffe
'''

import numpy as np
import sys
import datetime as dt
import matplotlib.pyplot as plt

from uHome_calc_functions_AT import *
#np.set_printoptions(threshold='nan')
np.set_printoptions(suppress=True)
#np.set_printoptions(precision=3)

def main():
    
    if ( len(sys.argv) != 2 ):
        print 'program parameters incorrect'
        print 'usage: ./prog.py filename '
        print 'example dataset: sample_SET2_P01.csv'
        sys.exit(2)
    else:
        filename = sys.argv[1]
    
    data_array_2d = read_csv_to_matrix(filename)

    num_ant = 1666
    # initialize 2d matrix for each pair of antennas
    markovChainCounts = np.zeros((num_ant+1,num_ant+1))

    # initiliaze time array for each ten min segment
    timeDist = np.zeros(24*6)

    # no user makes more than 1000 trips in one day
    # reshape once find max num trips
    userLengths = np.zeros(1000)

    user_id = 1
    num_trips = 1
    maxNum_trips = 1
    #for x in range(100):	 
    for x in range(len(data_array_2d)):

        user_curr = int(data_array_2d[x][0])
        ant_curr = int(data_array_2d[x][1])
        ant_next = int(data_array_2d[x][2])
        time_curr = get_date(data_array_2d[x][3])
        time_next = get_date(data_array_2d[x][4])

        # step 1. generate markov chain counts 
        markovChainCounts[ant_curr,ant_next] += 1
    
        # step 2. acculumate time of trips
        time_index = int(time_next.hour*6.0+time_next.minute/10.0)
        timeDist[time_index] +=1

        # step 3. acculumate trips per user
        # assumption: user ids are sorted
        if user_id == user_curr:
            num_trips+=1
        else:
            userLengths[num_trips]+=1
            user_id = user_curr
            if num_trips > maxNum_trips:
                maxNum_trips = num_trips
            num_trips = 1   
 
        # overall debugging print statements
        #outString = str(user_curr)+","+str(ant_prev)+","+str(ant_curr)+","+str(time_prev)+","+str(time_curr)
        #print outString
    
        # trip debugging
        if x % 10000 == 0:
            print "trip", x, "out of", len(data_array_2d)

    # normalize markov chains so all outgoing trip prob = 1.0 (by row)
    row_sums = markovChainCounts.sum(axis=1)
    markovChain = np.nan_to_num(markovChainCounts / row_sums[:, np.newaxis])

    # markov chain 2d array debug
    for row in range(len(markovChain)):
        for col in range(len(markovChain[row])):
            if markovChain[row,col] != 0:
                print row, col, markovChain[row,col]


    #for row in range(len(markovChainCounts)):
    #    for col in range(len(markovChainCounts[row])):
    #        if markovChainCounts[row,col] != 0:
    #            print row,col, markovChainCounts[row,col], sum(markovChainCounts[row]), markovChainCounts[row,col] / sum(markovChainCounts[row])

    # time dist array debug
    print timeDist
    #plt.plot(timeDist)
    #plt.show()

    # user length array debug
    print userLengths[:maxNum_trips+1]

if __name__ == "__main__":
    main()
