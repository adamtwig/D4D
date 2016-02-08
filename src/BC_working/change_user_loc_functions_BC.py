import sys
import numpy as np

def read_csv(csv_file):
	data_list=[]
	with open(csv_file,'rb') as the_file:
		for line in the_file:
			data_list.append(line.strip('\r"\n').split(','))
	return np.array(data_list)


def count_active_ids(array_2d , id_index):
	ids = set([])
	for array in array_2d:
		ids.add(int(array[id_index]))
	return sorted(list(ids))

def write_csv(prefix, filename, arr_freq):
	with open(prefix + filename, "wb") as final:
		for i in range(len(arr_freq)):
			for j in range(len(arr_freq)):
				final.write(str(i+1) +',' +str(j+1) + ','+str(arr_freq[i][j])+'\n')





