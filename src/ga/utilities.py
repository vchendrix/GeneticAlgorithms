'''
Created on Jan 6, 2011

This module defines the random functions defined in
    Goldberg, David. (1989). Genetic Algorithms in Search, 
    Optimization and Machine Learning. Appendix B 

Classes:

Random -- A Psuedorandom number generator (PRNG)

Functions:

createGraph - create an undirected graph with n vertices populated using the PRNG
maxmin - returns the maximun and minimum hamiltonian paths for the given graph
swap - swap data between two variables


Exceptions:


URL for Code here

'''
__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 7, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'

import array
import itertools
import math

def createGraph(n,rand):
    """ create an undirected graph 
        n is the number of vertices
        rand is the seeded random number generator
        
        rand = Random()
        rand.warmupRandom(.2342987345987345)
        graph = createGraph(5,rand)
    """    
        
    graph=[0]*n
    for i in range(n):
        graph[i]=[0]*n
            
    for i in range(n):
        for j in range(i,n):
            if i !=j:
                r=rand.rnd(0, 200)
                graph[i][j]=r
                graph[j][i]=r
                
        print graph[i]
         
    return graph
    
def maxmin(graph):
    """ find the maximun and minimum hamiltonian circuit for 
        a fully connected graph
    """
    perm = itertools.permutations(range(0, len(graph)))
    maxi = 0
    mini = 2000
    for p in perm:
        distance = 0
        for j in range(1,len(p)):
            distance += graph[p[j]][p[j - 1]]
                    
        maxi = max(distance, maxi)
        mini = min(distance,mini)
    print "max distance: %d" % maxi
    print "min distance: %d" % mini
    return maxi,mini

def swap(a,b):
    """ Swaps the values"""
    tmp=a
    a=b
    b=tmp

class Random(object):
    '''
    Programs based on the Pascal programs (random.apb) in
    Goldberg, David. (1989). Genetic Algorithms in Search, 
    Optimization and Machine Learning. Appendix B
    
    This code rewritten in python from the Pascal version
    with little modification to logic.
    '''
    oldrand = array.array('d',range(56)) # array of 55 random numbers
    jrand=0
    

    def __init__(self):
        '''
        Constructor
        '''
        
    def advanceRandom(self):
        '''
        Create  next batch of 55 random numbers
        '''
        
        for j1 in range(25):
            newrand=self.oldrand[j1]-self.oldrand[j1+31]
            newrand=newrand+1.0 if (newrand<0.0) else newrand
            self.oldrand[j1]=newrand
        for j1 in range(25,56):
            newrand=self.oldrand[j1]-self.oldrand[j1-24]
            newrand=newrand+1.0 if (newrand<0.0) else newrand
            self.oldrand[j1]=newrand
            
    def warmupRandom(self, seed):
        ''' Get random off and running '''
        ii=0
        self.oldrand[55] =seed
        newrand=.000000001
        prevrand=seed
        for j1 in range(1,55):
            ii=(21*j1) % 55
            self.oldrand[ii]=newrand
            newrand=prevrand-newrand
            newrand=newrand+1.0 if (newrand<0.0) else newrand
            prevrand=self.oldrand[ii]
        for i in range(1,3):
            self.advanceRandom()
        self.jrand=0
        
    def random(self):
        ''' Fetch a single random number between 0.0 and 0.1 - Subtractive Method
            See Knuth, D. (1969), v. 2 for details.
            
            Returns a floating point psuedorandom number between zero and one 
            (a uniform random variable on the real interval [0,1]).
        '''
        self.jrand=self.jrand+1
        if self.jrand > 55:
            self.jrand=1
            self.advanceRandom()
        return self.oldrand[self.jrand]
    
    def flip(self,prob):
        ''' Flip a biased coin, true if heads. 
            Returns a boolean True value with the specified probability
            (a Bernoulli random variable)'''
        return True if prob==1.0 else (self.random() <= prob)
    
    def rnd(self, low, high):
        ''' Pick a random integer between low and high.
        
            Returns an integer value between specified lower and upper limits
            (a uniform random variable over a subset of adjacent integers)
        '''
        i=0
        if(low>=high):
            i=low
        else:
            i=(self.random() * (high-low+1))+low
            i= high if i > high else i
        return math.trunc(i)
    
    def randomize(self):
        ''' Get seed number for random and start it up '''
        seed=0
        while True:
            seed= input('Enter seed random number (0.0..1.0): ')
            print "%s\n" % seed
            if seed > 0.0 and seed <1.0:
                break
        self.warmupRandom(seed)
        
            
        
        
            
            
        
            