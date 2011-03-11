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
from ga.common import *

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
    def testGraphMockResults(self):
        x={'k': 2, 'minksize': 5, 'kassign': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}  
        bestS=Individual(None,0,x,0,niche=0,normalized=False, attainmentScore=0.380778277697)        
        bestS.fitness={'deviation': 0.19753234153458674, 'connectivity': 0.22941573387056177}
        x={'k': 18, 'minksize': 1, 'kassign': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 3, 1, 4, 5, 1, 1, 1, 6, 7, 8, 9, 1, 1, 1, 9, 1, 1, 10, 1, 1, 1, 11, 10, 1, 9, 1, 1, 4, 5, 2, 1, 8, 6, 1, 4, 1, 1, 1, 1, 1, 1, 12, 1, 1, 1, 9, 13, 1, 1, 1, 1, 14, 1, 4, 1, 1, 15, 2, 1, 1, 16, 1, 13, 10, 1, 1, 5, 1, 1, 1, 1, 3, 6, 10, 1, 1, 1, 1, 1, 12, 6, 1, 1, 1, 1, 1, 6, 1, 1, 1, 8, 16, 1, 1, 14, 1, 1, 1, 10, 1, 2, 10, 1, 12, 1, 10, 16, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 16, 1, 1, 1, 1, 15, 12, 1, 17, 1, 1, 17, 6, 1, 1, 1, 10, 1, 8]}
        controlS=Individual(None,0,x,0,niche=0,normalized=False, attainmentScore=None)        
        controlS.fitness={'deviation': 0.49316438938781604, 'connectivity': 0.46940279403817725}

        graphMockResults('./data/mock',dataType='nf',solution=dict(best=bestS,control=controlS))

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
