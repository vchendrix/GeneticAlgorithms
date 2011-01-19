'''
Created on Jan 18, 2011

@author: val
'''
import sys
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import unittest
from ga.mock import createIrisGraph,primsAlgorithm



class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCreateIrisGraph(self):
        V=createIrisGraph("./bezdekIris.data")
        
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")

        
    def testPrims(self):
        V=createIrisGraph("./bezdekIris.data")
        
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")
        
        Vnew,Enew = primsAlgorithm(V)
        self.assertEqual(len(Vnew), len(V), "Incorrect Number of vertices")
        self.assertEqual(len(Enew), len(V)-1, "Incorrect Number of edges")
        
        chrom=[None]*len(V)
        i=0
        for e in Enew:
            print "%d-%d:%f" % (e.v1.id,e.v2.id,e.weight())
            if chrom[e.v1.id]==None:
                chrom[e.v1.id]=e.v2.id
            elif chrom[e.v2.id]==None:
                chrom[e.v2.id]=e.v1.id
        for i in range(len(chrom)):
            if chrom[i]==None:
                chrom[i]=V[i].edges[0].mate(V[i]).id
                
        print chrom




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateIrisGraph']
    unittest.main()