'''
Created on Jan 18, 2011

@author: val
'''
import os
import sys
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import graphMockResults as gmr
import mock
import unittest
from datetime import datetime
from ga.utilities import *
from ga.mock import *


class Test(unittest.TestCase):


    def setUp(self):
        self.random = Random()
        self.random.warmupRandom(.3849837507758344)
        
        self.V=createIrisGraph("./data/bezdekIris.data")
        
        pass


    def tearDown(self):
        pass

    @profile
    def testDecode(self):

        chrom=[18,17,15,8,6,5,0,9,12,19,7,11,17,13,16,17,18,12,7,1,31,32,23,31,37,24,25,26,31,29,30,37,29,38,39,36,39,21,13,32,54,59,50,57,43,47,30,42,52,22,53,41,45,44,50,57,22,57,57,20]
        x={'k': 7,'minksize':1, 'kassign': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 3, 4, 4, 4, 4, 3, 4, 6, 4, 6, 6, 6, 6, 5, 6, 6, 4, 6, 4, 6, 6, 6, 6, 4, 6, 6, 4]}        
        xtest=decode(chrom)
        print xtest
        self.assertEqual(x,xtest,"the decoded chromome is incorrect.")
        
    @profile
    def testClusterDeviation(self):
        V=self.V
        
        # number of clusters
        k=15
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 5, 5, 5, 5, 3, 3, 6, 6, 6, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 3, 6, 4, 3, 7, 7, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 7, 7, 7, 7, 7, 6, 6, 9, 9, 3, 3, 3, 3, 3, 11, 3, 3, 11, 6, 12, 3, 7, 6, 3, 12, 7, 3, 3, 6, 12, 12, 12, 6, 3, 12, 3, 3, 3, 3, 3, 3, 14, 3, 14, 14, 3, 3, 3, 3, 3]
        d=clusterDeviation(k,kassign,V)
        
        self.assertAlmostEqual(0.367179862891, d,8, msg="Cluster Deviation was %s should be %s" % (d,0.367179862891))
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterDeviation(k,kassign,V) 
        self.assertAlmostEqual(1.14113951812, d, msg= "Cluster Deviation is incorrect %s should be %s" % (d,1.14113951812))
        

    @profile
    def testClusterConnectivity(self):
        V=self.V
        
        # number of clusters
        k=15
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 5, 5, 5, 5, 3, 3, 6, 6, 6, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 6, 3, 3, 3, 3, 6, 4, 3, 7, 7, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 7, 7, 7, 7, 7, 6, 6, 9, 9, 3, 3, 3, 3, 3, 11, 3, 3, 11, 6, 12, 3, 7, 6, 3, 12, 7, 3, 3, 6, 12, 12, 12, 6, 3, 12, 3, 3, 3, 3, 3, 3, 14, 3, 14, 14, 3, 3, 3, 3, 3]
        d=clusterConnectivity(kassign,V,20)
        
        self.assertAlmostEqual(61, d, 8, "Cluster Deviation is incorrect %s expected %s" % (d,61))
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterConnectivity(kassign,V,20)
        self.assertAlmostEqual(55, d, 8, "Cluster Deviation was %s expected %s"
                % (d,55))

    @profile
    def testCreateIrisGraph(self):
        V=self.V
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")

    @profile
    def testCreateNxGraph(self):
        V=self.V
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")
        kassign=[1, 1, 1, 1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 2, 1, 5, 5, 1, 1, 1, 1, 1, 5, 5, 3, 1, 5, 5, 5, 1, 1, 5, 5, 1, 1, 6, 6, 4, 1, 1, 1, 6, 7, 7, 7, 7, 9, 9, 9, 7, 9, 7, 7, 11, 11, 11, 11, 11, 11, 11, 7, 7, 12, 12, 11, 7, 7, 13, 7, 7, 13, 13, 13, 7, 11, 14, 14, 14, 14, 14, 7, 7, 7, 7, 7, 7, 14, 7, 14, 1, 7, 14, 11, 7, 7, 16, 14, 14, 18, 18, 7, 19, 7, 7, 19, 19, 7, 7, 19, 7, 7, 7, 11, 7, 7, 7, 22, 7, 7, 14, 22, 18, 23, 14, 11, 7, 24, 7, 7, 7, 7, 25, 25, 25, 7, 25, 7, 7, 7, 7, 7]
        
        g=[39,34,47,47,0,10,47,39,8,34,48,7,1,38,33,33,10,0,5,48,27,19,22,26,11,34,7,48,39,11,29,20,46,32,30,49,10,4,42,28,17,8,47,26,46,1,44,3,19,7,52,75,86,89,58,90,51,57,75,89,93,96,92,91,64,75,55,92,72,80,138,82,133,63,75,74,58,52,61,81,81,81,92,142,84,56,52,68,95,89,94,78,92,57,99,96,99,71,98,82,136,149,120,116,132,107,84,125,108,143,147,147,139,101,121,110,147,117,122,119,120,101,105,146,120,125,123,126,103,125,107,117,128,83,134,135,148,116,127,145,112,145,113,143,140,147,111,77,115,127]
             
    @profile
    def testCosine(self):
        x=[1,1]
        y=[2,2]
        c=cosineSimilarity(x,y)
        self.assertAlmostEqual(c,0,0,"Cosine Similarity is incorrect was %s should be %s" %(c,1)) 
    
    @profile
    def testCreateNormalizedUniformlyRandomGraph(self):

        rand = Random()
        rand.warmupRandom(.679838975498345)
        V=createNormalizedUniformlyRandomGraph(40,2,rand)
        values=(len(V),40)
        self.assertEqual(values[0],values[1],"Had %s rows should have been %s" %values)
        
    
    @profile
    def testEuclidean(self):
        x=[1,2]
        y=[1,3]
        d=euclideanDistance(x,y)
        self.assertEqual(d,1,"Euclidean Distance is incorrect was %s should be %s" %(d,1)) 

    @profile
    def testNormalizeGraph(self):
        normalizeGraph(self.V)
        for v in self.V:
            for i in range(len(v.value)):
                self.assertLessEqual(v.value[i],1,"Value %s ! <= 1" % v.value[i])

    @profile
    def testPareto(self):
        indiv1 = mock.Mock()
        indiv1.fitness={'deviation':1,'connectivity':0} 
        indiv2 = mock.Mock()
        indiv2.fitness={'deviation':1,'connectivity':0} 

        p=getSolutionParetoRelationship(indiv1,indiv2)
        self.assertEqual(p,Pareto.NONDOMINATED,"Pareto was %s should be %s"%(p,Pareto.NONDOMINATED)) 
        
        indiv1.fitness={'deviation':1,'connectivity':1}
        indiv2.fitness={'deviation':0,'connectivity':0}

        p=getSolutionParetoRelationship(indiv1,indiv2)
        self.assertEqual(p,Pareto.DOMINATED,"Pareto was %s should be %s"%(p,Pareto.DOMINATED)) 
        
        indiv1.fitness={'deviation':0,'connectivity':0}
        indiv2.fitness={'deviation':0,'connectivity':1}

        p=getSolutionParetoRelationship(indiv1,indiv2)
        self.assertEqual(p,Pareto.NONDOMINATED,"Pareto was %s should be %s"%(p,Pareto.NONDOMINATED)) 
        
        indiv1.fitness={'deviation':0,'connectivity':0}
        indiv2.fitness={'deviation':1,'connectivity':1}

        p=getSolutionParetoRelationship(indiv1,indiv2)
        self.assertEqual(p,Pareto.DOMINATES,"Pareto was %s should be %s"%(p,Pareto.DOMINATES)) 
        
        indiv1.fitness={'deviation':0,'connectivity':0}
        indiv2.fitness={'deviation':0,'connectivity':0}

        p=getSolutionParetoRelationship(indiv1,indiv2)
        self.assertEqual(p,Pareto.NONDOMINATED,"Pareto was %s should be %s"%(p, Pareto.NONDOMINATED)) 


    @profile
    def testPrims(self):
        V=self.V
        
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")
        
        Enew = primsAlgorithm(V,self.random)
        self.assertEqual(len(Enew), len(V)-1, "Incorrect Number of edges")

        
    @profile
    def testMock(self):
        V=createIrisGraph("./data/bezdekIris.data")
        
        m = Mock(V,self.random)
        todayStr=datetime.today().isoformat()
        resultsDir=createResultsDir('mock')
        m.run(outputDir=resultsDir)
        gmr.main([resultsDir])


if __name__ == "__main__":
    import sys
    #sys.argv = ['','Test.testMockSolutionFront']
    unittest.main()
