import numpy as np
import csv
import datetime
from collections import defaultdict
import json
import sys
'''
'       Load in file paths
'''
def load_in_files(file_paths_file):
    data_files = []
    with open(file_paths_file,'rb') as file_list:
        for line in file_list:
            line = line.strip('\n"\r')
            data_files.append(line)
    return data_files


#####################################################
'''
Name:           Useful Functions
Project:        D4D
Description:
Purpose:
Author:         Nikko Vogel
Version:        15:52 5/16/2014
'''
#####################################################

## Count Keys in dictionary
def count_keys(dictionary):
    return len(dictionary.keys())

## Write a list of objects to a csv file
def write_list_to_csv(mylist, output_file_name, dlmtr):
    with open(output_file_name, 'wb') as myfile:
        wr = csv.writer(myfile, delimiter = dlmtr)
        wr.writerow(mylist)

## Write a matrix of objects to a csv file
def write_matrix_to_csv(mymatrix, output_file_name, dlmtr):
    with open(output_file_name, 'wb') as myfile:
        wr = csv.writer(myfile, delimiter = dlmtr)
        for mylist in mymatrix:
            wr.writerow(mylist)

## Read in csv file to numpy 2D array
def read_csv_to_matrix(csv_file):
    matrix = []
    with open(csv_file,'rb') as myfile:
	for line in myfile:
	    nline =line.strip('\n"\r').split(',')
	    matrix.append(nline)
    return np.array(matrix)

## Read in csv file to numpy array
def read_csv_to_array(csv_file):
    with open(csv_file,'rb') as myfile:
        for line in myfile:
            array =line.strip('\n"\r').split(',')                                 
    return np.array(array)


################################################################################
# Construct a sample data for testing
################################################################################
def sample_set(record_file,outfile,size):
    fp = open(record_file,'rb')
    fout = open(outfile,'wb')
    writer = csv.writer(fout,delimiter='\t')
    for x in range(size):
	line = fp.readline()
	#print line
	writer.writerow([line.strip('\n')])
    #print fp.readline()
    fout.close()
    fp.close()



################################################################################
# Identify the active caller IDs in the data file
################################################################################
def active_caller_IDs(files):
#def active_caller_IDs(files,outfile):
    callerIDs=set([])
    for f in files:
	fp=open(f,'rb')
        for line in fp:
            #line = line.strip('\n"\r').split('\t')
   	    line = line.strip('\n"\r').split(',')
	    caller = int(line[0])
	    callerIDs.add(caller)
	   # print callerIDs
	fp.close()
    callerIDs = sorted(list(callerIDs))
    #print callerIDs
    #fout = open(outfile,'wb')
    #writer = csv.writer(fout, delimiter=',')
    #writer.writerow(callerIDs)
    #fout.close()
    return callerIDs

################################################################################
# Identify the active antennas in the data file
################################################################################
def active_antennas(files):
#def active_antennas(files,outfile):
    antennas=set([])
    for f in files:
	fp=open(f,'rb')
        for line in fp:
            #line = line.strip('\n"\r').split('\t')
   	    line = line.strip('\n"\r').split(',')
	    antenna = int(line[2])
	    antennas.add(antenna)
	fp.close()
    antennas = sorted(list(antennas))
    #print antennas
    #fout = open(outfile,'wb')
    #writer = csv.writer(fout, delimiter=',')
    #writer.writerow(antennas)
    #fout.close()
    return antennas

################################################################################
# Create a cronalogical array of the locations each caller made a call from
################################################################################
def caller_Movement(files,outfile, num_sites, users_file): 
    user_ids = np.array(map(int,read_csv_to_array(users_file)))
    num_users = len(user_ids)
    callerLocs = np.zeros((num_users,num_sites))
    
    for f in files:
	with open(f,'rb') as fp:
	    try:
            	for line in fp:
                    nline = line.strip('\n"\r').split(',')
		    user_id = int(nline[0])
		    user_index = np.argmax(user_ids == user_id)
		    callerLocs[user_index][int(nline[2]) - 1] += int(1)
	    except IndexError:
	    	print nline
	    	sys.exit(1)
    write_matrix_to_csv(callerLocs,outfile,',')


#############################################################################
#  Determine home and work location of users
#############################################################################
def determine_home_and_work_location(locations_visited):
    print locations_visited
    home_tract = np.argmax(locations_visited)
#    print home_tract
#    print len(counts), home_tract
    locations_visited[home_tract] = 0
    print home_tract
    work_tract = np.argmax(locations_visited)
    if work_tract == 0 and locations_visited[0] == 0:
  	work_tract = home_tract
    return home_tract+1, work_tract+1



############################################################################    
#Construct Worker Flow TSV file and tract population CSV file for FLUTE
#	Construct a (#Arrondisements)^2 by  numpy matrix.
#	Add region,Dept,Arr to matrix
#	Identify Home and Work location of each user and add values to matrix.
################################################################################
def construct_worker_flow_tsv(region_info_file, coordinates_file, caller_movement_file, output_worker_flow_file, output_populations, num_tracts):
    worker_flow = np.zeros((num_tracts*num_tracts,7))
    tract_population = np.zeros((num_tracts,6))
    # Add region,Dept,Arr to matrix
    with open(region_info_file,'rb') as myfile:
        for line in myfile:
            nline =line.strip('\n"\r').split(',')
            region_id = int(nline[0])
            dept_id = int(nline[1])
            tract_id = int(nline[2])-1
	    try:
            	for x in range(0,num_tracts):
		    tract_population[x][0] = region_id
		    tract_population[x][1] = dept_id
	  	    tract_population[x][2] = tract_id
		    worker_flow[x+tract_id*num_tracts][0] = region_id
		    worker_flow[x+tract_id*num_tracts][1] = dept_id
		    worker_flow[x+tract_id*num_tracts][2] = tract_id
		    worker_flow[x*num_tracts+tract_id][3] = region_id
		    worker_flow[x*num_tracts+tract_id][4] = dept_id
		    worker_flow[x*num_tracts+tract_id][5] = tract_id
	    except IndexError:
		print x, num_tracts, tract_id
		sys.exit(1)
    # Add GPS coordinates to tract population matrix
    with open(coordinates_file,'rb') as myfile:
	for i,line in enumerate(myfile):
	    nline = line.strip('\n"\r').split(',')
	    tract_population[i][4] = '+' + nline[0]
	    tract_population[i][5] = nline[1]

    # Identify Home and Work location of each user and add values to matrix.
    with open(caller_movement_file,'rb') as myfile:
	for line in myfile:
	    print line
	    locations_visited = np.array(map(float,line.strip('\n"\r').split(',')))
	    print locations_visited
	    home_tract,work_tract = determine_home_and_work_location(locations_visited)
#	    print home_tract
	    tract_population[home_tract-1][3] +=1
	    worker_flow[(home_tract-1)*num_tracts+work_tract-1][6] += 1
    # Write two flute files
    write_list_to_csv(tract_population, output_populations, ',')
    write_matrix_to_csv(worker_flow, output_worker_flow_file, '\t')
