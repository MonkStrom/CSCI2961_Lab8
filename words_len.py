"""
Words/Ladder Graph
------------------
Generate  an undirected graph over the 5757 5-letter words in the 
datafile words_dat.txt.gz.  Two words are connected by an edge
if they differ in one letter, resulting in 14,135 edges. This example
is described in Section 1.1 in Knuth's book [1]_,[2]_.

References
----------
.. [1] Donald E. Knuth,
   "The Stanford GraphBase: A Platform for Combinatorial Computing",
   ACM Press, New York, 1993.
.. [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""
__author__ = """\n""".join(['Aric Hagberg (hagberg@lanl.gov)',
                            'Brendt Wohlberg',
                            'hughdbrown@yahoo.com'])
#    Copyright (C) 2004-2015 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

#Altered for CSCI-2961, Lab8
#Barry Hu, RPI

import networkx as nx
import sys
from collections import Counter
import itertools

#-------------------------------------------------------------------
#   The Words/Ladder graph of Section 1.1
#-------------------------------------------------------------------
def generate_graph(words):
    #Import lowercase ASCII characters
    from string import ascii_lowercase as lowercase
    #Initialize G as Graph from networkx
    G = nx.Graph(name="words")
    #Dictionary of each char in lowercase mapped to it's index
    lookup = dict((c,lowercase.index(c)) for c in lowercase)
    def edit_distance_one(word):
        for i in range(len(word)):
            left, c, right = word[0:i], word[i], word[i+1:]
            j = lookup[c] # lowercase.index(c)
            for cc in lowercase[j+1:]:
                yield left+cc+right 
    #Generator for words and their neighbors that exist in input data
    candgen = ((word, cand) for word in sorted(words) 
               for cand in edit_distance_one(word) if cand in words)
    #Add each word in words as a node into G
    G.add_nodes_from(words)
    #Add edge between a word and it's neighbor
    for word, cand in candgen:
        G.add_edge(word, cand)
    #Return generated graph
    return G

#Return the words example graph from the Stanford GraphBase
def words_graph(n):
    #Open appropriate input based on n
    if n==5:
        import gzip
        fh=gzip.open('words_dat.txt.gz','r')
    elif n==4:
        fh = open('words4.dat','r')

    words=set()
    for line in fh.readlines():
        #Decodes text one line based on default scheme
        line = line.decode()
        #Skip lines that start with *
        if line.startswith('*'):
            continue
        #Get the word the word is the first n char of the line
        w=str(line[0:n])
        #Add the word to the set
        words.add(w)
    #Generate graph from set words and return it
    return generate_graph(words)

def vary_n(W_n):
    for (source,target) in W_n:
        print("Shortest path between %s and %s is"%(source,target))
        try:
            sp=shortest_path(G, source, target)
            for n in sp:
                print(n)
        except nx.NetworkXNoPath:
            print("None")


if __name__ == '__main__':
    from networkx import *
    n = int(sys.argv[1])
    G=words_graph(n)
    print("Loaded words_dat.txt containing 5757 five-letter English words.")
    print("Two words are connected if they differ in one letter.")
    print("Graph has %d nodes with %d edges"
          %(number_of_nodes(G),number_of_edges(G)))
    print("%d connected components" % number_connected_components(G))
    W_4 = [('cold','warm'),('love','hate')]
    W_5 = [('chaos','order'),('nodes','graph'),('pound','marks'),('moron','smart')]
    if n==5:
        vary_n(W_5)
    elif n==4:
        vary_n(W_4)