#!/usr/bin/python

import numpy as np
import sys
from change_user_loc_functions_BC import*

def main():

	raw_dir = '/opt2/D4D/senegal/code/D4D_working/output/user/out_data/'
	
	if (len(sys.argv)!=3):
		print 'program parameters incorrect'
		print 'usage: ./prog.py filename1 filename2'
		sys.exit(3)
	else:
		filename1 = sys.argv[1]
		filename2 = sys.argv[2]
		input_file1 = raw_dir + filename1
		input_file2 = raw_dir + filename2

	file1_data = read_csv(input_file1)
	file2_data = read_csv(input_file1)

	file1_arr = []
	file2_arr = []

	for i in range(len(file2_arr)):
		file1_arr.append(file1_data[i][1])
		file2_arr.append(file2_data[i][1])
	file1_arr_ay = np.array(file1_arr)
	file2_arr_ay = np.array(file2_arr)
	final_array = np.column_stack((file1_arr_ay, file2_arr_ay))

	home1_arr_ids =count_active_ids(file1_data,1)
	home2_arr_ids =count_active_ids(file2_data,1)

 	nofilter = np.zeros((max(home1_arr_ids),max(home2_arr_ids)))

	for x in range(len(final_array)):
		home1_arr_ids = int(final_array[x][0])-1
		home2_arr_ids = int(final_array[x][1])-1
		
		nofilter[home1_arr_ids,home2_arr_ids] += 1

	output ="/opt2/D4D/senegal/code/D4D_working/src/BC_working/out_data_BC/out_data/"
	write_csv(output + "change_popu", filename2 , nofilter)

if __name__ =="__main__":
	main()
