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
import ga
from ga import simple
from ga.utilities import *
from ga.simple import SimpleGeneticAlgorithm


        
        
class TestSimpleGeneticAlgorithm(unittest.TestCase):
    
            
        
    @profile 
    def testDefault(self):

        rand = Random()
        rand.warmupRandom(.6598734598745938)
        resultsDir=createResultsDir('simple') 
        sga = SimpleGeneticAlgorithm(rand,popsize=30, lchrom=30);
        ga.common.initReport(sga)
        sga.run(silent=False,outputDir=resultsDir)
        graphSimpleResults(resultsDir)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
