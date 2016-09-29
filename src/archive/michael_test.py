#!/usr/bin/python
'''
Dataset 2
1666 sites
~300,000 users
'''
import numpy as np
import datetime
import csv

# http://stackoverflow.com/questions/1987694/print-the-full-numpy-array
np.set_printoptions(threshold=np.nan)

'''
csv format:

user_id, timestamp, site_id
user_id, timestamp, site_id
user_id, timestamp, site_id
...


list of lists format:

[
   [site_id, site_id, site_id, ...],
   [site_id, site_id, site_id, ...],
   [site_id, site_id, site_id, ...],
...
]

where list_of_lists[user_id] corresponds to [site_id, site_id, site_id, ...]

i.e. user_id is used as index into list_of_lists to get list of sites
that the user called from

assumes that there are users 1 through n filling 0 through n-1 spaces in list of lists
if not, issues with accessing correct sites according to user_id

'''
def read_csv_to_list_of_lists(csv_file):
    
    # http://preshing.com/20110920/the-python-with-statement-by-example/    
    # https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
    with open(csv_file, 'rb') as my_file:
        list_of_lists = []
        users_to_sites = {}
        for line in my_file:
            list_line = line.strip('\n\r').split(',')
            user = int(list_line[0])
            site = int(list_line[2])
            
            if user in users_to_sites:
                if site not in users_to_sites[user]:
                    users_to_sites[user].append(site)
            else:
                users_to_sites[user] = []
                users_to_sites[user].append(site)
    
            #if 0 <= user < len(list_of_lists):
            #   if site not in list_of_lists[user - 1]:
            #       list_of_lists[user - 1].append(site)
            #else:
            #   list_of_lists.insert(user - 1, [])
            #   list_of_lists[user - 1].append(site)
        
    for key in sorted(users_to_sites.keys()):
        list_of_lists.append(sorted(users_to_sites[key]))

    return list_of_lists


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



# read csv and print datetime format
def read_csv(csv_file):
    with open(csv_file, 'rb') as myfile:
        index = 0
        for line in myfile:
            if index == 100:
                break
            else:
                list_line = line.strip('\n\r').split(',')
                date = get_date(str(list_line[1]))
                print get_weekday(date)
                print get_time(date) 
                index += 1
                



# http://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html
# function to read csv into numpy array
'''
[
    ['user_id', 'timestamp', 'site_id']
    ['user_id', 'timestamp', 'site_id']
    ...
]
'''
def read_csv_to_array_2d(csv_file):
    
    # create empty list
    list_of_lists = []
    
    # open file in read mode 
    with open(csv_file,'rb') as myfile:
        
    # for each line in file
        for line in myfile:
            
        # strip out newline and carriage return characters
            # split string line on comma into list of elements 
            list_line = line.strip('\n"\r').split(',')
            
        # append each list to the matrix list
            list_of_lists.append(list_line)
    
    # convert list of lists to numpy array
    return np.array(list_of_lists)



# function to count number of active user ids in 2d array of data
'''
[
    [user_id, timestamp, site_id],
    [user_id, timestamp, site_id],
    ...
]
'''
def count_active_user_ids(array_2d, user_id_index):
    
    # create empty mathematical set
    user_ids=set([])

    # iterate over arrays in 2d numpy array
    for array in array_2d:
        
        # add user id to set (ignores duplicates)
        # converting to int first makes sure sorting is not by strings
        user_ids.add(int(array[user_id_index]))
    
    # convert set to list, sort, and return user ids
    return sorted(list(user_ids))   



# function to count number of active site ids in 2d array of data
'''
[
    [user_id, timestamp, site_id],
    [user_id, timestamp, site_id],
    ...
]
'''
def count_active_site_ids(array_2d, site_id_index):
    site_ids=set([])
    for array in array_2d:
        site_ids.add(int(array[site_id_index]))
    return sorted(list(site_ids))



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
    # get index of antenna that has highest value for each user
    # so we have which antenna that user called from the most depending on
    # definition of home
    # indices are same as antenna ids
    max_ant_indices = np.argmax(numpy_matrix, axis=1)
    
    # for each antenna, aggregate number of users associated with that antenna
    # use 1d array of max antenna indices, to bincount
    # so at each antenna's index will be the number of times that antenna
    # appears
    return np.bincount(max_ant_indices) #.astype(int))


# write 1d array to csv file
# def ant_freq_to_csv(ant_freq_array, output_file):
#    with open(output_file, 'wb') as csvfile:
#        outputwriter = csv.writer(csvfile)
#        
#        for x in range(len(ant_freq_array)):
#            outputwriter.writerow(str(x) + ', ' + str(ant_freq_array[x]))
    

# files
#raw_csv = '/opt2/D4D/senegal/data/SET2/raw/SET2_P01.CSV'

raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
raw_file = 'SET2_P01.CSV'

raw_csv = raw_dir+raw_file

sample_csv = 'sample_SET2_P01.csv'

# read csv into numpy array -- sample
# data_array_2d = read_csv_to_array_2d(sample_csv)

# read csv into numpy array -- raw
data_array_2d = read_csv_to_array_2d(raw_csv)

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

# function write to csv
def output_write(prefix, antID_array):
    outfile = open(prefix+raw_file, 'w')
    for i in range(len(antID_array)):
        # add 1 because subtracted 1 for index in matrix 
        outfile.write(str(i + 1) + ',' + str(antID_array[i]) + "\n")

out_dir = 'out_data/'

output_write(out_dir+'out_nofilter', nofilter)
output_write(out_dir+'out_daytime_', daytime)
output_write(out_dir+'out_nighttime_', nighttime)
output_write(out_dir+'out_weekdays_', weekdays)
output_write(out_dir+'out_weekends_', weekends)

# ant_freq_to_csv(nofilter, 'out_nf' + sample_csv)
 

#for i in range(len(nofilter)):
#    print str(i) + ',' + str(nofilter[i])

# create dictionary mapping (user, site) data to (row, col) in matrix
# dict_indices = create_dict_indices(user_ids, site_ids)

# create matrix using sample data, dictionary for indices, and 
# number of user ids and number of site ids
# matrix = create_matrix(sample_data_array_2d, dict_indices, len(user_ids), len(site_ids), 0, 2)

#print matrix

#python_list_of_lists = read_csv_to_list_of_lists(raw_csv)
#print python_list_of_lists

