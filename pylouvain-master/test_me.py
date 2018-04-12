#!/usr/bin/env python3

import math
# import unittest
from LV import PyLouvain
'''
class PylouvainTest(unittest.TestCase):

	def test_arxiv(self):
		pyl = PyLouvain.from_file("data/networkdata.txt")
		partition, q = pyl.apply_method()
		
	# function to write txt file
	def writefile(list_input,filename2):
		fw = open (filename2, 'w') 
		for cnt1 in range( len(list_input) ) :  
			for cnt2 in range( len(list_input[0])-1 ):
				fw.write("%s\t" % list_input[cnt1][cnt2])
			fw.write("%s\n" % list_input[cnt1][len(list_input[0])-1] )
'''

'''
	def test_citations(self):
		pyl = PyLouvain.from_file("data/hep-th-citations")
		partition, q = pyl.apply_method()

	def test_karate_club(self):
		pyl = PyLouvain.from_file("data/karate.txt")
		partition, q = pyl.apply_method()
		q_ = q * 10000
		self.assertEqual(4, len(partition))
		self.assertEqual(4298, math.floor(q_))
		self.assertEqual(4299, math.ceil(q_))

	def test_lesmis(self):
		pyl = PyLouvain.from_gml_file("data/lesmis.gml")
		partition, q = pyl.apply_method()

	def test_polbooks(self):
		pyl = PyLouvain.from_gml_file("data/polbooks.gml")
		partition, q = pyl.apply_method()
'''

def test_arxiv():
	pyl = PyLouvain.from_file("data/networkdata.txt")
	partition, q = pyl.apply_method()
	input_lst = []
	group_num = len(partition)
	cluster = {}
	for group in range(group_num):
		for group_member in range(len(partition[group])):
			cluster[(partition[group][group_member])] = (group+1)
	for cnt in range(1000):
		input_lst.append([])
	for cnt in range(1000):
		input_lst[cnt].append((cnt+1))
		input_lst[cnt].append(cluster[(cnt)])
	# print(input_lst)
	return input_lst
		
# function to write txt file
def writefile(list_input,filename2):
	fw = open (filename2, 'w') 
	for cnt1 in range( len(list_input) ) :  
		for cnt2 in range( len(list_input[0])-1 ):
			fw.write("%s\t" % list_input[cnt1][cnt2])
		fw.write("%s\n" % list_input[cnt1][len(list_input[0])-1] )

if __name__ == '__main__':
	# unittest.main()
	lst_input = test_arxiv()
	writefile(lst_input,"Ans_v1.txt")