'''
Created on Jan 18, 2011

@author: val
'''
import os
import sys
sys.path.insert(0, './src')
sys.path.insert(0, '../src')
import mock
import unittest
from datetime import datetime
from ga.utilities import *
from ga.mock import *


class Test(unittest.TestCase):


    def setUp(self):
        self.random = Random()
        from datetime import datetime
        self.random.warmupRandom(datetime.today().microsecond/1000001)       
        self.V=createIrisGraph("./data/iris.data")
        
        pass


    def tearDown(self):
        pass

    @profile
    def testDecode(self):

        chrom=[18,17,15,8,6,5,0,9,12,19,7,11,17,13,16,17,18,12,7,1,31,32,23,31,37,24,25,26,31,29,30,37,29,38,39,36,39,21,13,32,54,59,50,57,43,47,30,42,52,22,53,41,45,44,50,57,22,57,57,20]
        x={'k': 7,'kassign': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 3, 4, 4, 4, 4, 3, 4, 6, 4, 6, 6, 6, 6, 5, 6, 6, 4, 6, 4, 6, 6, 6, 6, 4, 6, 6, 4]}        
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
        
        self.assertAlmostEqual(0.366351048105, d,8, msg="Cluster Deviation was %s should be %s" % (d,0.366351048105))
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterDeviation(k,kassign,V) 
        self.assertAlmostEqual(1.12646532849, d, msg= "Cluster Deviation is incorrect %s should be %s" % (d,1.12646532849))
        

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
        
        self.assertAlmostEqual(62, d, 8, "Cluster Connectivity is incorrect %s expected %s" % (d,62))
        
        kassign=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 2, 2, 2, 6, 2, 2, 6, 5, 7, 2, 5, 5, 2, 7, 5, 2, 2, 5, 7, 7, 7, 5, 2, 7, 7, 2, 2, 2, 2, 2, 8, 2, 2, 8, 2, 2, 2, 2, 2]
        k=9
        d=clusterConnectivity(kassign,V,20)
        self.assertAlmostEqual(57, d, 8, "Cluster Deviation was %s expected %s"
                % (d,57))

    @profile
    def testCreateIrisGraph(self):
        V=self.V
        self.assertEqual(len(V), 150, "Graph is the incorrect length")
        self.assertEqual(len(V[0].edges), 149, "Graph is the incorrect length")

             
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
        V=createIrisGraph("./data/iris.data")
        
        m = Mock(V,self.random)
        todayStr=datetime.today().isoformat()
        resultsDir=createResultsDir('mock')
        solution=m.run(outputDir=resultsDir)
        graphMockResults(resultsDir,m.nicheUnit)        
        graphMockResults(resultsDir,m.nicheUnit,solution,dataType='nf')        


if __name__ == "__main__":
    import sys
    #sys.argv = ['','Test.testMockSolutionFront']
    unittest.main()
