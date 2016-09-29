#!/usr/bin/python
import numpy as np
import sys
import datetime

'''
Developers: Michael Baldwin, Adam Terwilliger
Version: October 29, 2015
Purpose: D4D (Data for Development) Challenge
     Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation

SET 2

Format:
[
    ['user_id', 'timestamp', 'site_id']
    ['user_id', 'timestamp', 'site_id']
    ...
]

Info:
1666 sites
~300,000 users

How to run:
./src/home_calc.py sample_SET2_P01.csv s

How to run with time output:
{ time ./src/home_calc.py sample_SET2_P01.csv s ; } 2> test.txt
'''

np.set_printoptions(threshold=np.nan)


'''
# create dictionary indices mapping from (user, site) to (row, col) in matrix
def create_dict_indices(user_ids, site_ids):
    
    # create empty dictionary
    dict_indices = {}
    
    # iterate over users and then sites
    for x in range(len(user_ids)):
        for y in range(len(site_ids)):
    
            # at key of (user_ids[x], site_ids[y]) tuple with value of (x,y) tuple
            # maps (user, site) to (row, col)
            dict_indices[(user_ids[x], site_ids[y])] = (x, y)
    return dict_indices

# function to create matrix using data 2d array, dictionary mapping data elements to indices
def create_matrix(array_2d, dict_indices, num_user_ids, num_site_ids, user_id_index, site_id_index):
    
    # create matrix and initialize to all zeroes
    matrix = np.zeros((num_user_ids, num_site_ids))
    
    # for each array in 2d array
    for array in array_2d:
        
        # map (user_id, site_id) to (row, col) in matrix
        location = dict_indices[(int(array[user_id_index]), int(array[site_id_index]))]
            
        # since data tells us we've got a user making a call at that site, increment matrix's corresponding location
        matrix[location[0], location[1]]+=1
    return matrix
'''





def count_active_site_ids(array_2d, site_id_index):
    site_ids=set([])
    for array in array_2d:
        site_ids.add(int(array[site_id_index]))
    return sorted(list(site_ids))



def count_active_user_ids(array_2d, user_id_index):
    user_ids=set([])
    for array in array_2d:
        user_ids.add(int(array[user_id_index]))
    return sorted(list(user_ids))   



# get date from timestamp
'''
timestamp format:

2013-01-07 13:10:00

desired format:
'''
# http://strftime.org/
# http://stackoverflow.com/questions/16286991/converting-yyyy-mm-dd-hhmmss-date-time
def get_date(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

# get time from date
def get_time(date):
    return date.time()

# get day of week from date
# http://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
def get_weekday(date):
    return date.weekday()

# aggregate antenna frequency
def agg_ant_freq(numpy_matrix):
    max_ant_indices = np.argmax(numpy_matrix, axis=1)
    
    return np.bincount(max_ant_indices) #.astype(int))



# function write to csv
def output_write(prefix, filename, antID_array):
    outfile = open(prefix+filename, 'w')
    for i in range(len(antID_array)):
        # add 1 because subtracted 1 for index in matrix 
        outfile.write(str(i + 1) + ',' + str(antID_array[i]) + "\n")


raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
sample_dir = '/opt2/D4D/senegal/code/D4D_working/sample_data/'

def read_csv_to_matrix(csv_file):
    list_of_lists = []
    with open(csv_file,'rb') as myfile:
        for line in myfile:
            list_line = line.strip('\n"\r').split(',')
            list_of_lists.append(list_line)
    return np.array(list_of_lists)

def main():
    if ( len(sys.argv) != 3 ):
        print 'program parameters incorrect'
        print 'usage: ./prog.py filename \'r/s\''
        print 'r = raw file, s = sample file'
        sys.exit(2)    
    else:
        filename = sys.argv[1]
        if ( sys.argv[2] == 'r' ):
            input_file = raw_dir + filename
        elif ( sys.argv[2] == 's' ):
            input_file = sample_dir + filename
        
    data_array_2d = read_csv_to_matrix(input_file)

    # count active user ids and site ids
    user_ids = count_active_user_ids(data_array_2d, 0)
    site_ids = count_active_site_ids(data_array_2d, 2)

    # use max value from each sorted list to account for all possible ids 
    # if used length, then mapping would be off for matrix access 
    num_user_ids = max(user_ids)
    num_site_ids = max(site_ids)

    # create matrices and initialize to all zeroes
    matrix_nofilter = np.zeros((num_user_ids, num_site_ids))
    matrix_daytime = np.zeros((num_user_ids, num_site_ids))
    matrix_nighttime = np.zeros((num_user_ids, num_site_ids))
    matrix_weekdays = np.zeros((num_user_ids, num_site_ids))
    matrix_weekends = np.zeros((num_user_ids, num_site_ids))

    # create dates to compare the times
    today7am = datetime.datetime.now().replace(hour=7, minute=0, second=0)
    today7pm = datetime.datetime.now().replace(hour=19, minute=0, second=0) 

    # for each array in 2d array
    for x in range(len(data_array_2d)):

        # get user, date, antenna
        user = int(data_array_2d[x][0])
        date = datetime.datetime.strptime(data_array_2d[x][1], "%Y-%m-%d %H:%M:%S")
        antenna = int(data_array_2d[x][2])

        # indexes are subtracted by 1 since matrix is zero based
        user_index = user - 1
        antenna_index = antenna - 1

        # increment matrix's location using userid, antennaid of this data's row
        matrix_nofilter[user_index, antenna_index]+=1

        # if date is between 7:01am and 6:59pm then daytime, else nighttime
        if (date.time() > today7am.time() and date.time() < today7pm.time()):
            matrix_daytime[user_index, antenna_index]+=1
        else:
            matrix_nighttime[user_index, antenna_index]+=1

        # if weekday is M,T,W,T,F (0,1,2,3,4) then weekday, else S,S (5,6)
        if (date.weekday() <= 4):
            matrix_weekdays[user_index, antenna_index]+=1
        else:
            matrix_weekends[user_index, antenna_index]+=1
    

    # aggregate matrices by antenna frequency
    nofilter = agg_ant_freq(matrix_nofilter)
    daytime = agg_ant_freq(matrix_daytime)
    nighttime = agg_ant_freq(matrix_nighttime)
    weekdays = agg_ant_freq(matrix_weekdays)
    weekends = agg_ant_freq(matrix_weekends)

    out_dir = 'out_data/'

    output_write(out_dir+'out_nofilter', filename, nofilter)
    output_write(out_dir+'out_daytime_', filename, daytime)
    output_write(out_dir+'out_nighttime_', filename, nighttime)
    output_write(out_dir+'out_weekdays_', filename, weekdays)
    output_write(out_dir+'out_weekends_', filename, weekends)



if __name__ == "__main__":
    main()
