#!/usr/bin/python
'''
Author: Michael Baldwin
Project: Data for Development
'''
import os.path
import numpy as np
from geopy.distance import vincenty



with open(fileName, 'rb') as f:
  reader = csv.reader(f)
  for row in reader:
    print row


# @return list of lists, where each inner list is made up of strings
def read_file(filePath):
    with open(filePath, 'rb') as file:
        data = list()
        header = True
        for line in file:
            if header:
                header = False
            else:
                tokens = line.strip('\n').split(',')
                data.append(list(tokens))
        return data


# @data is list of lists
def write_file(filePath, data):
    with open(filePath, 'wb') as file:
        file.write('id1, lat1, lng1, id2, lat2, lng2, dist (miles)\n')
        for itemList in data:
            file.write(str(itemList).strip('[]') + '\n')



# https://pypi.python.org/pypi/geopy
def calc_vincenty_dist(pointA, pointB):
    return vincenty(pointA, pointB).miles



# @input is list of lists, 
#    where each list is [site_id, arr_id, lng, lat]
# @output is list of lists, 
#    where each list is [idA, latA, lngA, idB, latB, lngB, dist]
def calc_output(input):
    output = list()
    for listA in input[0:4]:
        for listB in input[0:4]:
            between = list()
            
            idA = int(listA[0])
            latA = float(listA[3])
            lngA = float(listA[2])

            idB = int(listB[0])
            latB = float(listB[3])
            lngB = float(listB[2])
            
            between.append(idA)   
            between.append(latA)
            between.append(lngA)
            between.append(idB)
            between.append(latB)
            between.append(lngB)
            
            pointA = (latA, lngA)
            pointB = (latB, lngB)
            dist = calc_vincenty_dist(pointA, pointB)
            between.append(dist)
            
            output.append(between)
    return output

def main():
    csvFile = "SITE_ARR_LONLAT.CSV"
    numSites = 1666

    resDir = "res"
    filePathInput = os.path.join(resDir, csvFile)
    data = read_file(filePathInput)
    
    distBetween = calc_output(data)
    # print distBetween
    # print distBetween[0]
    # print distBetween[0][0]

    outFile = "SITE_DIST_LATLNG.csv"
    outDir = "out"
    filePathOutput = os.path.join(outDir, outFile)
    write_file(filePathOutput, distBetween)



if __name__ == '__main__':
    main()
