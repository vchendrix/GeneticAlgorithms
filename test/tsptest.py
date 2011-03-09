'''
Created on Jan 13, 2011

@author: val
'''
import copy
import math
import unittest
import sys
import time
sys.path.insert(0, '../src')
import ga
from ga import tsp
from ga.utilities import *
from ga.tsp import TSPGeneticAlgorithm


        
        
class TestTSPGeneticAlgorithm(unittest.TestCase):
    
    
    @profile
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
        for j in range(5,11):
            win=0
            rand = Random()
            rand.warmupRandom(.2342987345987345)
            rounds=10
            print "Tour of %s Cities" % j
            for i in range(rounds):
                rand.warmupRandom(rand.random())
                graph = createGraph(j,rand)
                tspga = TSPGeneticAlgorithm(rand, graph, 500, 30, 0.6, 0.033);
                #ga.common.initReport(tspga)
                resultsDir=createResultsDir('tsp_%s' % j)
                tspga.run(outputDir=resultsDir)
                graphTSPResults(resultsDir,j)
                max,min = maxmin(graph)
                print "(%d)algorithm: %d, actual: %d" % (i,tspga.minx,min)
        
                win+=1 if min==tspga.minx else 0
            
            print "accuracy:%d/%d" % (win,rounds)
            self.assertGreater(float(win)/float(rounds), .89, "accuracy not good enough")
        
    @profile
    def testBigTours(self):
        for j in range(15,20):
            rand = Random()
            rand.warmupRandom(.2342987345987345)
            rounds=10
            print "Tour of %s Cities" % j
            for i in range(rounds):
                rand.warmupRandom(rand.random())
                graph = createGraph(j,rand)
                tspga = TSPGeneticAlgorithm(rand, graph, 100, 100, 0.6, 0.033);
                resultsDir=createResultsDir('tsp_%s' % j)
                tspga.run(outputDir=resultsDir)
                graphTSPResults(resultsDir,j)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestTSPGeneticAlgorithm.testBigTours']
    unittest.main()
