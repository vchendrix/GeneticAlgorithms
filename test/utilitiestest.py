'''
Created on Feb 23, 2011

@author: val
'''
from StringIO import StringIO
import unittest
import sys
import time
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import ga
from ga.utilities import *

class TestUtilities(unittest.TestCase):


    @profile
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

    @profile
    def testProfile(self):
        
        oldstdout=sys.stdout
        sys.stdout=myout=StringIO()

        @profile
        def double(x):
            return 2*x

        d= double(155)
        sys.stdout= sys.__stdout__

        value=(myout.getvalue(),'double.start\ndouble.end\n')
        self.assertEqual(value[0],value[1],"Got %s should have been %s" % value)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestUtilities.testProfile']
    unittest.main()
