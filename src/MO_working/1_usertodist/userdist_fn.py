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

	if ( len(sys.argv) != 3 ):
		print 'program parameters incorrect'
		print 'usage: ./prog.py filename '
		print 'example dataset: sample_SET2_P01.csv'
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
        
	
	ant_distance = {}
	#reading in the distance data
	with open('/opt2/D4D/senegal/code/output/SITE_DIST_LATLNG.csv') as fl:
		reader = csv.DictReader(fl)
		for row in reader:
			a1 = row['id1']
			#print(a1)
			a2 = row[' id2']
			#print (a2)
			dist = row[' dist (miles)'][1:-1]
			#print(dist)
			
			if (a1 < a2):
				ant_distance[int(a1),int(a2)] = float(dist)
			else:
				ant_distance[int(a2),int(a1)] = float(dist)

	#print(ant_distance)
#	outfile = open("/opt2/D4D/senegal/code/D4D_working/src/MO_working"+ "ant_distance_pairs", 'w')
#	outfile.write('ant1,ant2,dist')
#	for key in ant_distance:
#		outfile.write(str(key[0])+','+str(key[1])+','+str(ant_distance[key])+"\n")

#	exit(42)
	
	#read in data
	data_list = []
	with open(input_file, 'rb') as fl:
		for line in fl:
			list_line = line.strip('\n"\r')
			no_coms = list_line.split(',')
			data_list.append(no_coms)
			
			#print(data_list[len(data_list)-1][0]) 
			#print(data_list[len(data_list)-1][2]) prints comma???


	
	user_id = 1
	count = 0 
	total_dist = 0
	prev_ant = -1
	diff_calls_count = 0

	# user -> total_dist, count, avg_dist
	user_to_dist = {}

	for index in range(0,len(data_list)):
		# if current user is the same as previous
		if data_list[index][0] == user_id:
			count = int(count) + 1
			
			#won't execute very first line
			if int(prev_ant) > 0:
				if int(prev_ant) > int(data_list[index][2]):
					total_dist += float(ant_distance[int(data_list[index][2]),int(prev_ant)])
					diff_calls_count += 1
				elif int(prev_ant) == int(data_list[index][2]):
					total_dist += 0
				else:
					diff_calls_count += 1
					total_dist += float(ant_distance[int(prev_ant), int(data_list[index][2])])
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
		
												


	outfile = open('/opt2/D4D/senegal/code/D4D_working/output/user_dist_travelled/out_SET2_' + fileout + '.CSV', 'w')
#	outfile = open('/opt2/D4D/senegal/code/D4D_working/src/MO_working/1_usertodist/SAMPLE_' + fileout + '.CSV', 'w')
	outfile.write('user_id,total_dist,total_calls,avg_dist,diff_calls,distance_no_repeats\n')
	for key in user_to_dist:
		outfile.write(str(key) + ',' + str(user_to_dist[key][0]) + ',' + str(user_to_dist[key][1]) + ',' + str(user_to_dist[key][2]) + ',' + str(user_to_dist[key][3]) + ',' + str(user_to_dist[key][4]) + "\n")

if __name__ == "__main__":
	main()
