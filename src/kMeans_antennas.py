#!/usr/bin/python
'''
Author: Roderick Vogel
Project: Data for Development Kmeans Of Antenna distance between eachother

Description: This project reads in a csv file where each row and column represents a matrix of antennas
and each value of the matrix is the distance between two antennas.
After reading the the file its data is converted to an array of arrays. Where the kmeans are calculated and it returns the centroids.
This operation is performed from 2 up to the number of antennas (nA) present in the file.
Each calculation of k-means is returns a centriods list, from this centroid list \
each antenna is assigned to a cluster in an array called idx.
Finally a matix is created assigning the value of idx data to the respective antenna \
making each matrix column hold the cluster for that antena from 2 up to nA clusters.
'''

from pylab import plot,show
import numpy as np
import time 
from scipy.cluster.vq import kmeans,vq

# data generation
#stre distance in a list of list
print("reading file")
def read_file(filePath):
    with open(filePath, 'rb') as file:
        data = list()
        for line in file:
            
            antenna = line.strip('\n').split(',')
            aList = list(antenna)
            for index, item in enumerate(aList):
                aList[index] = float(item)
            data.append(aList)
        return data
csvFile = "SITE_DIST_LATLNG.CSV"  
print("file read")

data = read_file(csvFile)   
#convert data to an array of arrays
a = np.array([x[0:] for x in data])   

f = open('output.csv','wb+')

i=1;



antennaAmount = 1666
#set index to 2 because this will be used from the number of clusters and there will at least be 2 clusters
index = 2
# create 2d array 1 added to to first paramter so that the number of clusters equals the # of antennas
clusters =np.ndarray(shape=(antennaAmount+1,antennaAmount), dtype=object, order='F')
clusters[0][0] = "" # set corner to blank because of labels 
print("list being made")
# creates antenna labels with the antenna number labels in first coluymn of csv
# creates cluster labels which represents the number of cluster in each column
while i<antennaAmount+1:
    s = str(i) + " antenna"
    u = i+1
    if i<antennaAmount:
        t = str(u) +"  Clusters"
        clusters[0][i] = t
    clusters[i][0]= s
    i+=1
print("finished antenna thing")
# x and y = 1 to make up for labels
x =1
y = 1
#iterates through the kmeans with the number of clusters ranging from 2- number of attenas
while y< antennaAmount:
    centroids,_ = kmeans(a,index)
    #print("Cluster Number:   " , index)
    # assign each antenna to a clusters
    idx,_ = vq(a,centroids)
    #print(idx)
    #sets all of the anttennas to a cluster number which is stored vertically in a 2darray
    while x < antennaAmount+1:
        clusters[x][y] =idx[x-1]
        x+=1
    y+=1
    x=1
    index +=1


print("list made: Time \n")
print(time.clock())
#stores the 2d array of Antenna# by #ofClusters into a csv file called output
np.savetxt("output.csv", clusters,fmt= '%s', delimiter=',')   # Clusters  is a 2d array