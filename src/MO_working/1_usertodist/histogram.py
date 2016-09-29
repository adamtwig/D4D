import matplotlib.pyplot as plt
#import matplotlib as plt
import numpy as np
import csv

# input the file
f = open("/opt2/D4D/senegal/code/D4D_working/output/user_dist_travelled/out_SET2_P01.CSV")
data = csv.reader(f)

x = []
count = 0

for row in data:
	if count > 0:
		x.append(float(row[5]))
	if count is 0:
		count = 1
	#print(row[5])

plt.figure()
plt.hist(x, bins=50)		
plt.savefig('hist.png', bbox_inches='tight')
