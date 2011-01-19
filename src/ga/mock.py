'''
Created on Jan 18, 2011

This module defines the functions and classes that support
the MOCK (Multiobjective Clustering with K-Determination) 
algorithm.

@author: val
'''
__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 18, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'

import heapq
import ga
import math
import networkx as nx
import sets

from ga.common import Chromosome, Individual

#############
# Functions
#############

def createIrisGraph(filename):
    """ Create a fully connected graph using the data file """
    f = open(filename)
    V = [] # vertices
    
    i = 0
    for line in f:
        line = line.rstrip('\n ')
        if(len(line) > 0):
            line = line.rpartition(",")
            value = tuple(float(l) for l in line[0].split(","))
            group = line[2]
            V.append(Vertex(group, value, i))
            i += 1
            
    for i in range(len(V)):
        for j in range(len(V)):
            e = Edge(V[i], V[j])
            if(e.weight() > 0):
                V[i].edges.append(e)
    return V

def creatNxGraph(V):
    """ creates a graph using the networkx library """
    G=nx.Graph()
    for v in V:
        G.add_node(v.id)
        for e in v.edges:
            G.add_edge(e.v1.id, e.v2.id, weight=e.weight())
    return G

        

def primsAlgorithm(V):
    """
        Applies Prim's Algorithm to the specified adjacency list
        and returns the MST as a tuple (V,E)
    """
    pq = []
         
    allE = sets.Set()
    for j in range(len(V)):
        v = V[j]
        for k in range(len(v.edges)):
            e = v.edges[k]
            allE.add(e)
    
    for e in allE:
        heapq.heappush(pq, e)
      
    Et = []
    Vt = [None]*len(V)
    Vt[0]=V[0]
    e=heapq.heappop(pq)
    i=1
    Etmp=[]
    while (e != None or i!=len(V)):
        if Vt[e.v1.id]!=None and Vt[e.v2.id]==None:
            Et.append(e);
            e.v2.edges=[]           
            Vt[e.v2.id]=e.v2
            i+=1
            for t in Etmp: 
                heapq.heappush(pq,t)
            Etmp=[]
        elif Vt[e.v2.id]!=None and Vt[e.v1.id]==None:
            Et.append(e)  
            e.v1.edges=[]        
            Vt[e.v1.id]=e.v1
            i+=1
            for t in Etmp: 
                heapq.heappush(pq,t)
            Etmp=[]
        else: Etmp.append(e)
        e=heapq.heappop(pq) if len(pq)>0 else None
    
    for v in Vt:
        v.edges=[e for e in Et if e.mate(v)]
    return (Vt,Et)
    
            

class Edge(object):
    
    def __init__(self, v1, v2):
            
        self.v1 = v1
        self.v2 = v2
        self.w = None
        
    def mate(self, v):
        if self.v1 == v: return self.v2;
        if self.v2 == v: return self.v1;
        return None
   
    def weight(self):
        if(self.w == None):
            self.w = 0
            for i in range(len(self.v1.value)):
                self.w += (self.v1.value[i] - self.v2.value[i]) ** 2
            self.w = math.sqrt(self.w)
        return self.w
    
    def __eq__(self, other):
        if other==None: return False
        if(self.mate(other.v1)!=None and self.mate(other.v2)!=None): return True
    
    def __cmp__(self, other):
        if other==None: return 1
        if self.weight() < other.weight():return - 1
        if self.weight() == other.weight(): return 0
        return 1
    
    def __str__(self):
        s = "Edge<%s,%s,%f>" % (self.v1.__str__(), self.v2.__str__(), self.weight())
        return s
            


class Vertex(object):
    '''
    classdocs
    '''


    def __init__(self, group, value, id, edges=None):
        '''
        Constructor
        '''
        self.edges = [] if edges == None else edges
        self.value = value
        self.group = group
        self.id=id
        
    def __eq__(self, other):
        if other == None: return False
        return self.id == other.id

    def __str__(self):
        s = "Vertex%s" % (self.value.__str__())
        return s
        
