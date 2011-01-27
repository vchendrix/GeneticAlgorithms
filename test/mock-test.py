'''
Created on Jan 18, 2011

@author: val
'''
import sys
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import unittest
from ga.utilities import Random
from ga.mock import *



class Test(unittest.TestCase):


    def setUp(self):
        self.random = Random()
        self.random.warmupRandom(.87465982498734)
        
        self.V=createIrisGraph("./bezdekIris.data")
        
        pass


    def tearDown(self):
        pass

    def testClusterDeviation(self):
        V=self.V
        
        # number of clusters
        k=4
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3]
        d=clusterDeviation(k,kassign,V)
        
        self.assertAlmostEqual(1511.63809567, d, 8, "Cluster Deviation is incorrect")
        
        kassign=[0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 3, 1, 3, 3, 4, 1, 4, 1, 1, 4, 3, 3, 1]
        k=5
        d=clusterDeviation(k,kassign,V)
        self.assertAlmostEqual(430.477089135, d, 8, "Cluster Deviation is incorrect")
        

    def testClusterConnectivity(self):
        V=self.V
        
        # number of clusters
        k=4
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3]
        d=clusterConnectivity(kassign,V)
        print d
        
        self.assertAlmostEqual(8, d, 8, "Cluster Deviation is incorrect")
        
        kassign=[0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 3, 1, 3, 3, 4, 1, 4, 1, 1, 4, 3, 3, 1]
        k=5
        d=clusterConnectivity(kassign,V)
        print d
        self.assertAlmostEqual(9, d, 8, "Cluster Deviation is incorrect")
        

    def testCreateIrisGraph(self):
        V=self.V
        self.assertEqual(len(V), 23, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 22, "Graph is the incorrect length")
             

        
    def testPrims(self):
        V=self.V
        self.assertEqual(len(V), 23, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 22, "Graph is the incorrect length")
        
        
        Enew = primsAlgorithm(V,self.random)
        self.assertEqual(len(Enew), len(V)-1, "Incorrect Number of edges")
        
    def testMockInitialization(self):
        V=self.V
        self.assertEqual(len(V), 23, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 22, "Graph is the incorrect length")
        
        mock = Mock(V,self.random)
        self.assertEqual(max(50,int(1/len(V))), len(mock.internalPop), "Mock internal pop is not 50 or 1/N")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateIrisGraph']
    unittest.main()