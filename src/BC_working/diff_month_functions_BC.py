
def read_csv(filename):
	datalist=[]
	with open(filename,'rb') as myfile:
		for line in myfile:
			datalist.append(line.split(','))
		return datalist

def find_diff(file1,file2):
	diff= []
	for i in range(len(file1)):
		a = int(file1[i][1])
		b = int(file2[i][1])
		c = a- b
		diff.append(c)
	return diff

def output_write(prefix, filename, difference)
	outfile = open(prefix+filename,'w')
	for i in range(len(difference)):
		outfile.write(str(i+1) + ',' +str(difference[i] + '\n')


