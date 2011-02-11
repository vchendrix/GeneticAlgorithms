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


    def testDecode(self):

        chrom=[18,17,15,8,6,5,0,9,12,19,7,11,17,13,16,17,18,12,7,1,31,32,23,31,37,24,25,26,31,29,30,37,29,38,39,36,39,21,13,32,54,59,50,57,43,47,30,42,52,22,53,41,45,44,50,57,22,57,57,20]
        x={'k': 7, 'kassign': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 3, 4, 4, 4, 4, 3, 4, 6, 4, 6, 6, 6, 6, 5, 6, 6, 4, 6, 4, 6, 6, 6, 6, 4, 6, 6, 4]}        
        xtest=decode(chrom)
        self.assertEqual(x,xtest,"the decoded chromome is incorrect.")

        
    def testClusterDeviation(self):
        V=self.V
        
        # number of clusters
        k=15
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 5, 5, 5, 5, 3, 3, 6, 6, 6, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 3, 6, 4, 3, 7, 7, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 7, 7, 7, 7, 7, 6, 6, 9, 9, 3, 3, 3, 3, 3, 11, 3, 3, 11, 6, 12, 3, 7, 6, 3, 12, 7, 3, 3, 6, 12, 12, 12, 6, 3, 12, 3, 3, 3, 3, 3, 3, 14, 3, 14, 14, 3, 3, 3, 3, 3]
        d=clusterDeviation(k,kassign,V)
        
        self.assertAlmostEqual(8905.271056, d, msg="Cluster Deviation is incorrect")
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterDeviation(k,kassign,V) 
        self.assertAlmostEqual(9124.1248813, d, msg= "Cluster Deviation is incorrect")
        

    def testClusterConnectivity(self):
        V=self.V
        
        # number of clusters
        k=15
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 5, 5, 5, 5, 3, 3, 6, 6, 6, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 3, 6, 4, 3, 7, 7, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 7, 7, 7, 7, 7, 6, 6, 9, 9, 3, 3, 3, 3, 3, 11, 3, 3, 11, 6, 12, 3, 7, 6, 3, 12, 7, 3, 3, 6, 12, 12, 12, 6, 3, 12, 3, 3, 3, 3, 3, 3, 14, 3, 14, 14, 3, 3, 3, 3, 3]
        d=clusterConnectivity(kassign,V)
        
        self.assertAlmostEqual(72, d, 8, "Cluster Deviation is incorrect")
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterConnectivity(kassign,V)
        self.assertAlmostEqual(75, d, 8, "Cluster Deviation is incorrect")
        

    def testCreateIrisGraph(self):
        V=self.V
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")
             

    def testCreateNxGraph(self):
        V=self.V
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")

        kassign=[1, 1, 1, 1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 2, 1, 5, 5, 1, 1, 1, 1, 1, 5, 5, 3, 1, 5, 5, 5, 1, 1, 5, 5, 1, 1, 6, 6, 4, 1, 1, 1, 6, 7, 7, 7, 7, 9, 9, 9, 7, 9, 7, 7, 11, 11, 11, 11, 11, 11, 11, 7, 7, 12, 12, 11, 7, 7, 13, 7, 7, 13, 13, 13, 7, 11, 14, 14, 14, 14, 14, 7, 7, 7, 7, 7, 7, 14, 7, 14, 1, 7, 14, 11, 7, 7, 16, 14, 14, 18, 18, 7, 19, 7, 7, 19, 19, 7, 7, 19, 7, 7, 7, 11, 7, 7, 7, 22, 7, 7, 14, 22, 18, 23, 14, 11, 7, 24, 7, 7, 7, 7, 25, 25, 25, 7, 25, 7, 7, 7, 7, 7]
        
        g=[39,34,47,47,0,10,47,39,8,34,48,7,1,38,33,33,10,0,5,48,27,19,22,26,11,34,7,48,39,11,29,20,46,32,30,49,10,4,42,28,17,8,47,26,46,1,44,3,19,7,52,75,86,89,58,90,51,57,75,89,93,96,92,91,64,75,55,92,72,80,138,82,133,63,75,74,58,52,61,81,81,81,92,142,84,56,52,68,95,89,94,78,92,57,99,96,99,71,98,82,136,149,120,116,132,107,84,125,108,143,147,147,139,101,121,110,147,117,122,119,120,101,105,146,120,125,123,126,103,125,107,117,128,83,134,135,148,116,127,145,112,145,113,143,140,147,111,77,115,127]
             
        
    def testPrims(self):
        V=self.V
        
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")
        
        Enew = primsAlgorithm(V,self.random)
        self.assertEqual(len(Enew), len(V)-1, "Incorrect Number of edges")
        
    def testMock(self):
        V=createIrisGraph("./bezdekIris.short")
        
        mock = Mock(V,self.random)
        #self.assertEqual(max(50,int(len(V)/20)), len(mock.internalPop), "Mock internal pop is not 50 or 1/N")
        
        mock.run()
        

if __name__ == "__main__":
    import sys
    sys.argv = ['','Test.testMock']
    unittest.main()
