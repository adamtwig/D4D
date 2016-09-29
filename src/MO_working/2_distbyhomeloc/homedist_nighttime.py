import numpy as np
import sys
import datetime as dt
np.set_printoptions(threshold='nan')
import csv

def main():

        #raw_dir = '/opt2/D4D/senegal/data/SET2/raw/'
        raw_dir = '/opt2/D4D/senegal/data/'
        sample_dir = '/opt2/D4D/senegal/code/data/sample_data/'
        out_user_dir = '../output/user/'
        out_ant_dir = '../output/user/'
        out_dir = '../output/user/'

        if ( len(argv) != 3 ):
                print 'program parameters incorrect'
                print 'usage: ./prog.py sample_SET2_P03.csv P03'
#               print 'example dataset: sample_SET2_P01.csv'
                sys.exit(2)
        else:
                filename = sys.argv[1]
                fileout = sys.argv[2]

                if ('SET2' in sys.argv[1]):
                        raw_dir = raw_dir + 'SET2/raw/'
                else:
                        raw_dir = raw_dir + 'SET3/raw/'

                if ('sample' in sys.argv[1]):
                        input_file = sample_dir + filename
                        out_dir = out_dir + 'sample_out_data/'
                else:
                        input_file = raw_dir + filename
                        out_dir = out_dir + 'out_data/'

	user_to_home_loc = {}
	filename = '/opt2/D4D/senegal/code/D4D_working/output/user/out_data/out_user_nighttime_SET2_' + fileout + '.CSV'


#	reads in home locations
	with open(filename, 'rb') as fl:
		for line in fl:
			list_line = line.strip('\n"\r')
			no_coms = list_line.split(',')
			user_to_home_loc[no_coms[0]] = no_coms[1]

#	reads in call data
	data_list = []
	with open(input_file, 'rb') as fl:
		for line in fl:
			list_line = line.strip('\n"\r')
			no_coms = list_line.split(',')
			data_list.append(no_coms)

	user_id = 1
	count = 0
	total_dist = 0
	diff_calls_count = 0

	user_to_dist = {}

	for index in range (0, len(data_list)):
		if data_list[index][0] == user_id:
			homeloc = user_to_home_loc[user_id]
			count = int(count) + 1

			#doesn't execute first line
			if int(prev_ant) > 0:
				if int(homeloc) > int(data_list[index][2]):
					total_dist += float(ant_distance[int(data_list[index][2]),int(homeloc)])
					diff_calls_count += 1
				elif int(homeloc) == int(data_list[index][2]):
					total_dist += 0
				else:
					diff_calls_count += 1
					total_dist += float(ant_distance[int(homeloc), int(data_list[index][2])])
				prev_ant = data_list[index][2]
		else:
			if diff_calls_count > 1:
				user_to_dist[user_id] = (total_dist, int(count)+1, float(total_dist)/int(count), int(diff_calls_count), float(total_dist)/int(diff_calls_count-1))
			elif count > 0:
				user_to_dist[user_id] = (total_dist, int(count)+1, float(total_dist)/int(count), int(diff_calls_count), float(total_dist)/int(count), int(diff_calls_count)-1)
			else:
				user_to_dist[user_id] = (total_dist, 1, total_dist, diff_calls_count, total_dist, diff_calls_count-1)

			user_id = data_list[index][0]
			count = 0
			total_dist = 0
			prev_ant = data_list[index][2]		
			diff_calls_count = 0
#outfile = open('/opt2/D4D/senegal/code/D4D_working/src/MO_working/out_test_' + fileout + '.csv', 'w')
#        outfile.write('user_id,total_dist,total_calls,avg_dist\n')
#        for key in user_to_dist:
#                outfile.write(str(key) + ',' + str(user_to_dist[key][0]) + ',' + str(user_to_dist[key][1]) + ',' + str(user_to_dist[key][2]) + "\n")

if __name__ == "__main__":
        main()

