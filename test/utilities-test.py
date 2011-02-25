'''
Created on Feb 23, 2011

@author: val
'''
import unittest
import sys
import time
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import ga
from ga.utilities import *

class TestUtilities(unittest.TestCase):


    def testCreateNormalizedGraph(self):
        rand = Random()
        rand.warmupRandom(.8934769875683387234)
        
        V=createGraph(40,rand,1)

        values=(len(V),40)
        self.assertEqual(values[0],values[1],"Had %s vertices should have been %s" %values)

    def testCreateNormalizedDataset(self):
        rand=Random()
        rand.warmupRandom(.23634743589053445308)
        D=createNormalizedDataset(40,2,rand)
  
        values=(len(D),40)
        self.assertEqual(values[0],values[1],"Had %s rows should have been %s" %values)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestUtilities.testName']
    unittest.main()
