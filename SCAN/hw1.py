# -*- coding: utf-8 -*-

#This program is used to find the shortest chain of friendships.

import sys
import networkx as nx
from collections import deque
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import *
from scipy import *

# function to read csv file
def readfile(filename):

	dataReadIn = []

	with open (filename, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split('\t')])
	f.close ()
	return dataReadIn
	
def writefile(list_input,filename2):
	fw = open (filename2, 'w') 
	for cnt1 in range( len(list_input) ) :  
		for cnt2 in range( len(list_input[0])-1 ):
			fw.write("%s\t" % list_input[cnt1][cnt2])
		fw.write("%s\n" % list_input[cnt1][len(list_input[0])-1] )
	
def struct_similarity(vcols, wcols):
	""" Compute the similartiy normalized on geometric mean of vertices"""
	# count the similar rows for unioning edges
	count = [index for index in wcols if (index in vcols)]
	# geomean
	#need to account for vertex itself, add 2(1 for each vertex)
	ans = (len(count) +2) / (((vcols.size+1)*(wcols.size+1)) ** .5)
	return ans

def neighborhood(G, vertex_v, eps):
	""" Returns the neighbors, as well as all the connected vertices """
	N = deque()
	vcols = vertex_v.tocoo().col
	#check the similarity for each connected vertex
	for index in vcols:
		wcols = G[index,:].tocoo().col
		if struct_similarity(vcols, wcols)> eps:
			N.append(index)
	return N, vcols

def scan(G, eps =0.7, mu=2):
	"""
	Vertex Structure = sum of row + itself(1)
	Structural Similarity is the geometric mean of the 2Vertex size of structure
	"""
	
	c = 0
	v = G.shape[0]
	# All vertices are labeled as unclassified(-1)
	vertex_labels = -np.ones(v)
	# start with a neg core(every new core we incr by 1)
	cluster_id = -1
	for vertex in range(v):
		N ,vcols = neighborhood(G, G[vertex,:],eps)
		# must include vertex itself
		N.appendleft(vertex)
		if len(N) >= mu:
			#print "we have a cluster at: %d ,with length %d " % (vertex, len(N))
			# gen a new cluster id (0 indexed)
			cluster_id +=1
			while N:
				 y = N.pop()
				 R , ycols = neighborhood(G, G[y,:], eps)
				 # include itself
				 R.appendleft(y)
				 # (struct reachable) check core and if y is connected to vertex
				 if len(R) >= mu and y in vcols:
					 #print "we have a structure Reachable at: %d ,with length %d " % (y, len(R))
					 while R:
						 r = R.pop()
						 label = vertex_labels[r]
						 # if unclassified or non-member
						 if (label == -1) or (label==0): 
							 vertex_labels[r] =  cluster_id
						 # unclassified ??
						 if label == -1:
							 N.appendleft(r)
		else:
			vertex_labels[vertex] = 0
	
	#classify non-members
	for index in np.where(vertex_labels ==0)[0]:
		ncols= G[index,:].tocoo().col
		if len(ncols) >=2:
			## mark as a hub
			vertex_labels[index] = -2
			continue
			
		else:
			## mark as outlier
			vertex_labels[index] = -3
			continue

	return vertex_labels

if __name__ == "__main__" :

	raw_data = readfile('networkdata.txt')
	
	raw_data_rows = []
	raw_data_cols = []
	
	for cnt in range(len(raw_data)):
		raw_data_rows.append(raw_data[cnt][0])
		raw_data_cols.append(raw_data[cnt][1])
	data = np.ones(len(raw_data_rows))
	G = csr_matrix((data,(raw_data_rows,raw_data_cols)),shape=(1001,1001))
	# print(G.todense())
	# sys.exit()
	cluster_lst = (scan(G,0.1,6))
	cluster_lst = cluster_lst.tolist()
	del(cluster_lst[0])
	
	# print(cluster_lst)

	cluster_lst_set = sorted(set(cluster_lst))
	cluster_lst_set_dic ={}
	for cnt in range(len(cluster_lst_set)):
		cluster_lst_set_dic[cluster_lst_set[cnt]] = str(cnt+1)
	# print(cluster_lst_set_dic)
	
	input_lst = [[] for cnt in range(1000)]
	for cnt in range(1000):
		input_lst[cnt].append(str(cnt+1))
		input_lst[cnt].append(cluster_lst_set_dic[float(cluster_lst[cnt])])
	# print(input_lst)
	
	writefile(input_lst,"Ans_v3.txt")
	
	'''
	a_2= 0
	a_3 =0
	for cnt in range(len(cluster_lst)):
		if(float(cluster_lst[cnt]) == -2.0):
			a_2=a_2+1
		if(float(cluster_lst[cnt]) == -3.0):
			a_3=a_3+1
	print(a_2 , a_3)

	print(len(set(cluster_lst)))
	'''
