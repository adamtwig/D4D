mport numpy as np
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


        # create map or array of user & home location, one for each home loc
	# create a map of user -> (home loc 1, total dist from home loc 1, total calls away from home loc 1, avg dist from home loc 1, etc....)
	# ex: 1 -> (1, 253, 10, 25.3, etc......)



outfile = open('/opt2/D4D/senegal/code/D4D_working/src/MO_working/out_test_' + fileout + '.csv', 'w')
        outfile.write('user_id,total_dist,total_calls,avg_dist\n')
        for key in user_to_dist:
                outfile.write(str(key) + ',' + str(user_to_dist[key][0]) + ',' + str(user_to_dist[key][1]) + ',' + str(user_to_dist[key][2]) + "\n")

if __name__ == "__main__":
        main()

