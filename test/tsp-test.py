'''
Created on Jan 13, 2011

@author: val
'''
import copy
import math
import unittest
import sys
import time
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import itertools
import ga
from ga import tsp
from ga.utilities import Random
from ga.tsp import TSPGeneticAlgorithm


        
        
class TestTSPGeneticAlgorithm(unittest.TestCase):
    
    
    def createGraph(self,n,rand):
        
        
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
    
    def maxmin(self,graph):
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
            
        
    
    def testDefault(self):

        """
        graph = [[0, 2 , 3 , 4 , 6 , 8 , 2],
                 [2, 0 , 7 , 10, 5 , 1 , 22],
                 [3, 7 , 0 , 5 , 10, 30, 3],
                 [4, 10, 5 , 0 , 55, 1 , 7],
                 [6, 5 , 10, 55, 0 , 1 , 15],
                 [8, 1 , 30, 1 , 1 , 0 , 19],
                 [2, 22, 3 , 7 , 15, 19, 0]]
        """
        win=0
        rand = Random()
        rand.warmupRandom(.2342987345987345)
        rounds=10
        for i in range(rounds):
            rand.warmupRandom(rand.random())
            graph = self.createGraph(9,rand)
            tspga = TSPGeneticAlgorithm(rand, graph, 500, 30, 0.6, 0.033);
            ga.common.initReport(tspga)
            tspga.run()
            max,min = self.maxmin(graph)
            print "algorithm: %d, actual: %d" % (tspga.minx,min)
        
            win+=1 if min==tspga.minx else 0
            
        print "wins:%d/%d" % (win,rounds)
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
