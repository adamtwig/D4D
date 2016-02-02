import sys
from diff_month_function_BC import *

def main()
	raw_dir = '/opt2/D4D/senegal/code/output/out_data'
	sample_dir = '/opt2/D4D/senegal/code/output/sample_out_data'
	if (len(sys.argv) !=3):
		print 'program parameters incorrect'
		print 'usage: ./prog.py filname'
		sys.exit(3)
	else:
		file1 = sys.argv[1]
		file2 = sys.argv[2]

		input_file1 = raw_dir + file1
		input_file2 = raw_dir + file2

	month1 = read_csv(input_file1)
	month2 = read_csv(input_file2)

	diff = find_diff(month1,month2)

	out_dir = ' '

if__name__ =="__main__"
	main()
