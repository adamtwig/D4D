#!/usr/bin/python
'''
Developer: Michael Baldwin and Adam Terwilliger
Version: September 29, 2015
Purpose: D4D (Data for Development) Challenge
	 Data mining for Orange Cell Phone records
Details: Definition of "home" with matrix representation
'''
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from generate_flute_files import * 

np.set_printoptions(threshold='nan')

raw_file = '/opt2/D4D/senegal/data/SET2/raw/SET2_P01.CSV'
sample_file = "sample2_SET2_P01.csv"

#sample_set(raw_file, sample_file, 1000000)

#sample_matrix = read_csv_to_matrix(sample_file)

sample_matrix = read_csv_to_matrix(raw_file)

#acIDs = active_caller_IDs([sample_file])
#acAnt = active_antennas([sample_file])

acIDs = active_caller_IDs([raw_file])
acAnt = active_antennas([raw_file])

home2 = np.zeros([max(acIDs)+1, max(acAnt)+1])

for k in range(len(sample_matrix)):
    home2[int(sample_matrix[k,0]),int(sample_matrix[k,2])]+=1

home_maxs = np.argmax(home2, axis=1)

#print 'home_maxs: \n', home_maxs

home_max_freq = np.bincount(home_maxs.astype(int))

#print 'home_max_freq: \n', home_max_freq
'''
fig = plt.figure()
plt.plot(np.array(range(max(acAnt)+1)),np.array(home_max_freq),'o')
plt.xlabel('Antenna Location')
plt.ylabel('Frequency of Max Call Users')
plt.savefig('FreqMaxCall1.png')
plt.close(fig)

#plt.show()
'''

#home_max_list = list(home_maxs,home_max_freq)

#print home_max_list


#nonZero_home_freqs = np.nonzero(home_maxs)[0]

#print 'nonZero_home_freqs: \n', nonZero_home_freqs

#final_home_maxs = zip(nonZero_home_freqs, home_max_freq[nonZero_home_freqs-1])

#print 'final_home_maxs: \n', final_home_maxs

'''
plt.hist(sorted_maxs,bins=999000)
plt.axis([0,200,0,200])
plt.title("Max Frequency Antennas")

plt.show()
'''





'''
print len(sample_matrix)

print sample_matrix[(len(sample_matrix)-10):(len(sample_matrix)-1)]

lenacIDs = len(acIDs)
lenacAnt = len(acAnt)

maxacIDs = max(acIDs)
maxacAnt = max(acAnt)

print '\nacIDs', str(acIDs)
print '\nacAnt', str(acAnt)
print '\nlenacIDs', str(lenacIDs)
print '\nlenacAnt', str(lenacAnt)
print '\nmaxacIDs', str(maxacIDs)
print '\nmaxacAnt', str(maxacAnt)
'''

'''
antDict = dict()

for i in range(len(acAnt)):

  antDict[acAnt[i]] = i

#print antDict


home1 = numpy.zeros([len(acIDs), len(acAnt)])
#home1 = numpy.empty([lenacIDs+1, lenacAnt])

#for k in range(len(sample_matrix)):
for k in range(999000):
    index0 = int(sample_matrix[k,0]) - 1
    index2 = antDict[int(sample_matrix[k,2])]

    home1[index0,index2]+=1 

    #home1[int(sample_matrix[k,0]),antDict[int(sample_matrix[k,2])]]+=1
    #print 'user: ', str(sample_matrix[k,0])
    #print 'location: ', str(sample_matrix[k,2])
    #print 'user, location count: ', home1[int(sample_matrix[k,0]),antDict[int(sample_matrix[k,2])]]

#print home1[1:10]
'''

'''
sorted_maxs = np.sort(home_maxs)

print 'sorted_maxs: \n', sorted_maxs

home_max_freq = np.bincount(home_maxs.astype(int))

print 'home_max_freq: \n', home_max_freq

sorted_hmf = np.sort(home_max_freq)

print 'sorted_hmf: \n', sorted_hmf

reversed_hmf = sorted_hmf[::-1]

print 'reversed_hmf: \n', reversed_hmf

nonZero_home_freqs = np.nonzero(reversed_hmf)[0]

print 'nonZero_home_freqs: \n', nonZero_home_freqs

final_home_maxs = zip(nonZero_home_freqs, reversed_hmf[nonZero_home_freqs])

print 'final_home_maxs: \n', final_home_maxs
'''


