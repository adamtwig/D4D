# -*- coding: utf-8 -*-
"""
===================================
TESTING igraph python
===================================
Create matrix of all year movements based on Call Records
And some statistics.
"""

import os
import sys
import errno
import getopt
import time
import numpy as np
import cairocffi as cairo
import igraph
import json
from utils import *

antennas = np.array([])

def load_antennas(antennas_file_path):
    global antennas
    if antennas.size == 0:
        antennas = read_csv_to_matrix(antennas_file_path)

def write_to_csv(csv_file_path, headers, array):
    #checking if the distance path exist
    if not os.path.exists(os.path.dirname(csv_file_path)):
        try:
            os.makedirs(os.path.dirname(csv_file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #Saving antennas
    with open(csv_file_path, "w") as f:
        f.write(headers)
        i = 0
        for row in array:
            
            #need to eliminate column 0, there's no antenna 0
            row_to_list = [str(x) for x in row]
            row_str = str(i+1)+','+','.join(row_to_list)+'\n'
            f.write(row_str)
            i+=1

def generate_igraph(filename):
    print "igraph  ******** file: ",filename
    tmpArray = read_csv_to_matrix(filename)
    
    adj_matrix_array = tmpArray[1:,1:].astype(float)
    print "ADJ_MATRIX",adj_matrix_array
    conn_indices = np.where(adj_matrix_array)
    
    node_names = np.unique(np.asarray(conn_indices).flatten())+1 
    # get the weights corresponding to these indices
    weights = adj_matrix_array[conn_indices]

    # a sequence of (i, j) tuples, each corresponding to an edge from i -> j
    edges = zip(*conn_indices)

    nodes_index={}
    i=0
    for node in node_names:
        nodes_index.update({int(node):i})
        i+=1

    adjusted_edges=[]
    for edge in edges:
        tmp_tuple = (nodes_index[int(edge[0]+1)],nodes_index[int(edge[1]+1)]) 
        adjusted_edges.append(tmp_tuple)

    # initialize the graph from the edge sequence
    G = igraph.Graph(edges=adjusted_edges, directed=True)
    print "nodes:",len(node_names)
    print "edges:",len(adjusted_edges)
    # assign node names and weights to be attributes of the vertices and edges
    # respectively
    vs_width = np.zeros_like(node_names)
    vs_width = vs_width + 240
    G.vs['label'] = node_names.astype(str)
    G.vs['width'] = vs_width


    # I will also assign the weights to the 'width' attribute of the edges. this
    # means that igraph.plot will set the line thicknesses according to the edge
    # weights
    es_width = np.copy(weights)
    es_width = es_width*1.5
    G.es['width'] = es_width
    #G.es['width'] = weights
    G.es['weight'] = weights
    G.es['label'] = weights.astype('|S5')

    #g_layout = G.layout_kamada_kawai()
    #g_layout = G.layout_sugiyama(weights=weights)
    #g_layout = G.layout_fruchterman_reingold(weights=weights) 
    g_layout = G.layout_drl(weights=weights)

    # plot the graph, just for fun
    print "About to write the graph"
    #igraph.plot(G, "./test.svg", layout='kk',height=768, width=1600, labels=True, margin=80)
    igraph.plot(G,'graph.svg', bbox=(2048,2048), labels=True, margin=100)
    print "well that took a while"
    #antennafilename = '/opt2/D4D/senegal/data/ContextData/SITE_ARR_LONLAT.CSV'
    #outputdir  = '../output/'
    #load_antennas(antennafilename)
    #file_headers = ','.join([str(x) for x in antennas[:,0]]) + '\n'
    #year_array = normalize_array(year_array)
    #year_file_path=outputdir+'/heatmap/year/2013.csv'
    #write_to_csv(year_file_path,file_headers,year_array)

def generate_json(filename):
    print "Generate JSON from file  ******** file: ",filename
    tmpArray = read_csv_to_matrix(filename)
    adj_matrix_array = tmpArray[1:,1:].astype(float)
    conn_indices = np.where(adj_matrix_array)
    
    # get the weights corresponding to these indices
    weights = adj_matrix_array[conn_indices]
    # a sequence of (i, j) tuples, each corresponding to an edge from i -> j
    edges = zip(*conn_indices)
    nodes = np.unique(np.asarray(conn_indices).flatten())+1
    graph_dict = {"nodes":[], "links":[]}
    nodes_index={}
    i=0
    for node in nodes:
        node_dict = {}
        node_dict.update({"name":str(node)})
        node_dict.update({"group":int(node)})
        graph_dict["nodes"].append(node_dict)
        nodes_index.update({int(node):i})
        i+=1
        
    print "from DICT"
    print "nodes \n len:",len(graph_dict["nodes"])
    
    i = 0
    for edge in edges:
        link_dict = {}
        #print "edge",i,edge[0],edge[1]
        #print "nodes_index",nodes_index[edge[0]+1],nodes_index[edge[1]+1]
        link_dict.update({"source": nodes_index[int(edge[0]+1)]})
        link_dict.update({"target": nodes_index[int(edge[1]+1)]})
        link_dict.update({"value":int(weights[i])})
        graph_dict["links"].append(link_dict)
        i+=1

    print nodes_index[1045]
    print "links \n len:",len(graph_dict["links"])

    print "ORIGINAL VALUES"
    print "nodes \n len:", nodes.size #, "data:\n", nodes
    print "edges \n len:", len(edges)
    print "weights \n len:", weights.size #, "data\n", weights
    #print "Json:", json.dumps(graph_dict)
    #Saving antennas json
    with open("./antenna.json", "w") as f:
        f.write(json.dumps(graph_dict, sort_keys=True, indent=4))

def main(argv):
    filename = ''
    require_generate_igraph = False
    require_generate_json = False
    try:
        opts, args = getopt.getopt(argv,"hjif:",["help","json","igraph","filepath="])
    except getopt.GetoptError:
        print 'Syntax error: \n Usage: igraph_test.py  <[-j|-i]> -f <file_path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print 'igraph_test.py  -f <file_path>'
            sys.exit()
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-j", "--json"):
            require_generate_json = True
        elif opt in ("-i", "--igraph"):
            require_generate_igraph = True

    if filename == '':
        print 'Syntax error: Filename can\'t be empty\n Usage: igraph_test.py <[-j|-i]>  -f <file_path>'
        print ' example filepath: ../output/home_location/269/SET2_P01.csv'
        sys.exit(2)
    if not require_generate_json and not require_generate_igraph:
        print 'Syntax error: Please pick at least one option, json or igraph\n Usage: igraph_test.py <[-j|-i]>  -f <file_path>'
        print ' example:  igraph_test.py  -j -f ../output/home_location/269/SET2_P01.csv'
        sys.exit(2)

    if require_generate_json:
        generate_json(filename)
    if require_generate_igraph:
        generate_igraph(filename)
if __name__ == "__main__":
    main(sys.argv[1:])

