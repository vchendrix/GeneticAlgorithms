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
from ga.utilities import Random
from ga.simple import SimpleGeneticAlgorithm


        
        
class TestSimpleGeneticAlgorithm(unittest.TestCase):
    
            
        
    
    def testDefault(self):

        rand = Random()
        rand.warmupRandom(.2342987345987345)
        
        sga = SimpleGeneticAlgorithm(rand);
        ga.common.initReport(sga)
        sga.run(verbose=True)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
