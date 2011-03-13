'''
Created on Jan 18, 2011

This module defines the functions and classes that support
the MOCK (Multiobjective Clustering with K-Determination) 
algorithm.

Classes

Edge - defines an edge in a graph
Hypergrid - define the hypergrid
Individual - inherited from ga.common.Individual
Mock - the MOCK genetic algorithm
Pareto - Enumeration for Pareto relationship of solutions
Vertex - define a vertex in a graph

Functions

clusterConnectivity - determines the cluster deviation of a solution 
    (chromosome) based on its decoded value which is the number of 
    clusters and the cluster assignments
clusterDeviation - determines the cluster deviation of a solution 
    (chromosome) based on its decoded value which is the number of 
    clusters and the cluster assignments
cosineSimilarity - returns the minimized cosine similarity for two vectors
createIrisGraph - this is a specific function that creates a Graph 
    (adjacency list) for the Iris dataset from the UCI Machine Learning dataset
createLocusBasedAdjacencyList - takes a graph (adjacency list) 
    and returnes it representation in locus based adjacency form
crossoverUniform - performes uniform crossover between two mates
decode - decodes the Mock algorithms Chromosome which is a graph  using
    a locus based adjacency representation and stored as a python list
euclideanDistance - returns the euclidean distance between two n-tuples
getNiche - returns the niche for a given individuals fitness
getSolutionParetoRelationship - return the first solutions relationship to the
    second solution. It is either DOMINATED, NONDOMINATED or DOMINATES
mutationNearsetNeighbor - mutates the alleles with a restriction on the 
    L nearest neighbors.
objectiveFunction - the multi-objective function returns a dictionary 
    containing the deviation and connectivity objectives
primsAlgorithm - returns the minimum spanning tree of the given graph 
    t(adjacency list)

@author: val
'''
__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 18, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'

import copy
import ga
import heapq
import math
import numpy as N
import sets
import sys

from numpy import linalg as LA

from ga.common import Chromosome
from ga.utilities import createNormalizedDataset

#############
# Functions
#############

def clusterConnectivity(kassign,graph,L):
    """ Calculates the cluster connectivity by evaluating
        the degree to which neighboring data-points have 
        been placed in the same cluster. The smaller the
        number the more connectivity the graph has.
        
        kassign: cluster assignment
        graph: a fully connected graph representing the data points with
             the edges sorted by ascending weights
             
             
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[1,2,3,4,5,1,1,1,2,1,4,2,5,2,3,,4,5,3]
        d=clusterConnectivity(kassign,graph)
        
    """
    connectivity=0
    for v in graph:
        l = L if len(v.edges)>20 else len(v.edges)
        for i in range(l):
            c1=kassign[v.id]
            c2=kassign[v.edges[i].mate(v).id]
            connectivity+= 0 if (c1==c2) else 1/(i+1)
    return connectivity
    

def clusterDeviation(k,kassign,graph):
    """ Calculate the centroids of all the clusters and then
        figures out the total deviation for the graph.
        
        k: number of clusters
        kassign: cluster assignment
        graph: a fully connected graph representing the data points with
             the edges sorted by ascending weights
        
        # number of clusters
        k=4
        
        # tells what clusters the edges in the 
        # locus based adjacency representation are
        # assigned to
        kassign=[0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3]
        d=clusterDeviation(k,kassign,graph)
        
        Centroids are found in the following manner.
        Example: The data set has three dimensions and the 
        cluster has two points: X = (x1,x2,x3) and Y = (y1,y2,y3). 
        Then the centroid Z becomes Z = (z1,z2,z3), where 
        z1= x1+y1/2, z2=x2+y2/2 and z3= x3+y3/2
    """
        
    # add up all the values in the n-tuples
    # associated with the vertices
    kMeans=[[]]*k
    kN=[0]*k
    for i in range(len(graph)):
        v=graph[i]
        l=kassign[i]
        kN[l]+=1
        if kMeans[l]==[]: kMeans[l]=list(v.value)
        else:
            for j in range(len(v.value)):
                kMeans[l][j]+=v.value[j]
    #print k
    #print kMeans
    #print kN
        
    # divided all the summed n-tuples from the vertices
    # by the number of data items in the cluster
    for i in range(k):
        for j in range(len(kMeans[i])):
            kMeans[i][j]=kMeans[i][j]/ kN[i]
    #print kMeans
    #print kN
            
    deviation=0
    #print kassign
    for i in range(len(graph)):
        v=graph[i]
        l=kassign[i]
        #print "[%d] %5f+=cosineSimilarity(%s,%s)" %(l,deviation,kMeans[l],v.value)
        deviation+=cosineSimilarity(kMeans[l],v.value) 
    #print "*******"
    return deviation

def cosineSimilarity(a,b):
    """ Determines the cosine similarity between two points.
        a and b are arrays 
    """
    return 1-(N.dot(a,b)/(LA.norm(a)*LA.norm(b)))
    

def createIrisGraph(filename):
    """ Create a fully connected graph using the data file 
        This returns a list of vertices of type Vertex with
        the edges in in nearest neighbor order (increasing 
        weight)
    """
    f = open(filename)
    V = [] # vertices
    
    i = 0
    for line in f:
        line = line.rstrip('\n ')
        if(len(line) > 0):
            line = line.rpartition(",")
            value = [float(l) for l in line[0].split(",")]
            group = line[2]
            V.append(Vertex(group, value, i))
            i += 1
            
    for i in range(len(V)):
        for j in range(len(V)):
            e = Edge(V[i], V[j])
            if(e.weight() > 0):
                V[i].edges.append(e)
        V[i].edges=heapq.nsmallest(len(V[i].edges),V[i].edges)
    
    return V

def createNormalizedUniformlyRandomGraph(rows,columns,rand):
    """ Create a graph with normalized data [0,1] uniformly
        at random.
    """
    V=[] # vertices
    dataSet=createNormalizedDataset(rows,columns,rand)     
    for i in range(len(dataSet)):
            V.append(Vertex(None,dataSet[i],i))

    for i in range(len(V)):
        for j in range(len(V)):
            e=Edge(V[i],V[j])
            if(e.weight() >0):
                V[i].edges.append(e)
        V[i].edges=heapq.nsmallest(len(V[i].edges),V[i].edges)
    return V


def createNxGraph(kassign,V):
    """ creates a nextwork x graph from the local adjacency based matrix """
    G=nx.Graph()
    rangeV=range(len(V))
    for i in rangeV:
        G.add_node(i,value=V[i].value,group=V[i].group)
        G.add_edge(i,kassign[i])            
    return G

def createLocusBasedAdjacencyList(V,E):
    """
        Creates a Locus-Based Adjacency representation 
        of the graph with vertices, V,  and edges, E.
        E should be a minimum spanning tree for V
        The list of edges should be equal to the number of vertices.
        
        Returns an ga.common.Chromosome instance
        
        
        random = ga.utilities.Random()
        random.warmupRandom(seedValue)
        V=createIrisGraph("afile") # returns a fully connected graph
        E=primsAlgorithm(V,random) # finds the minimun spanning tree for the givien graph
        
        chrom= Chromosome()
        alleles = createLocusBasedAdjacencyList(V,E)
        chrom.alleles=alleles
    """
    alleles=[None]*len(V)
    i=0
    for e in E:
        if alleles[e.v1.id]==None:
            alleles[e.v1.id]=e.v2.id
        elif alleles[e.v2.id]==None:
            alleles[e.v2.id]=e.v1.id
    for i in range(len(alleles)):
        if alleles[i]==None:
            alleles[i]=V[i].edges[0].mate(V[i]).id
    return alleles

def crossoverUniform(parent1,parent2,random,pcross,pmutation,G,L):
    """
        Uniform Crossover
        
        Returns three parameters (xsite,child1,child2)
        
        xsite = the mask used for the uniform crossover
        child1 = the first child
        child2 = the second child
    """
    child1=Chromosome()
    child2=Chromosome()
    xsite=""
    if(random.flip(pcross)):
        for i in range(len(parent1)):
            if(random.flip(.5)):
                xsite+="1"
                child1[i]=mutationNearestNeighbor(random,pmutation,i,parent2[i],G,L)
                child2[i]=mutationNearestNeighbor(random,pmutation,i,parent1[i],G,L )
            else:
                xsite+="0"
                child1[i]=mutationNearestNeighbor(random,pmutation,i,parent1[i],G,L)
                child2[i]=mutationNearestNeighbor(random,pmutation,i,parent2[i],G,L )
    else:
        xsite='0'*len(parent1)
        for i in range(len(parent1)):
                child1[i]=mutationNearestNeighbor(random,pmutation,i,parent1[i],G,L)
                child2[i]=mutationNearestNeighbor(random,pmutation,i,parent2[i],G,L )
    return xsite,child1,child2
            

def decode(chrom):
    """
    Returns a tuple (k,assignments)
    where 
    k is the number of clusters
    assignments is the list of cluster assignments 
    
    """
    cc=0
    clusterAssignment=[None]*len(chrom)
    previous=[None]*len(chrom)
    for i in range(len(chrom)):
        ctr=0
        if clusterAssignment[i]==None:
            clusterAssignment[i]=cc
            neighbor=chrom[i]
            previous[ctr]=i
            ctr+=1
            while clusterAssignment[neighbor]==None:
                previous[ctr]=neighbor
                clusterAssignment[neighbor]=cc
                neighbor=chrom[neighbor]
                ctr+=1
            if clusterAssignment[neighbor] != cc:
                ctr-=1
                while ctr >= 0:
                    clusterAssignment[previous[ctr]]=clusterAssignment[neighbor]
                    ctr-=1
            else:
                cc+=1
    # print "k:%d, kassgin:%s" %(cc+1,clusterAssignment)
    return dict(k=cc,kassign=clusterAssignment)                 

def euclideanDistance(x,y):
    """ Finds the euclidean distance between two n-tuples """
    z=range(len(x))
    for i in range(len(z)):
        z[i]=x[i]-y[i]
    return LA.norm(z) 
            
def getNiche(individual,dimension,nicheUnit):
    """ determines the current niche for the given individual 
        Returns a tuple (connectivity, deviation)
    """
    #print individual.fitness 
    d=dimension-1 if individual.fitness['deviation']==1 else (individual.fitness['deviation']/nicheUnit)
    c=dimension-1 if individual.fitness['connectivity']==1 else (individual.fitness['connectivity']/nicheUnit)
    return (int(c),int(d))
         
def getSolutionParetoRelationship(s1,s2):
    """ return s1's relatinship to s2 """
    if s1.fitness['deviation'] == float('inf'):
        return Pareto.DOMINATED

    dev=s1.fitness['deviation'] < s2.fitness['deviation']  
    conn=s1.fitness['connectivity'] < s2.fitness['connectivity']
    if dev and conn: return Pareto.DOMINATES

    dev=s1.fitness['deviation'] <= s2.fitness['deviation']  
    conn=s1.fitness['connectivity'] <= s2.fitness['connectivity']
    if dev or conn: return Pareto.NONDOMINATED
    else: return Pareto.DOMINATED

    
def mutationNearestNeighbor(random,pm,i,allele,G,L):
    """
        This is call mutation on the restricted nearest neighbors.
        It mutates a chromosome based on the L nearest neighbors
        supplied in the given graph G.
        
    """
    ledges=len(G[i].edges)
    Lnn=L if ledges > L else ledges 
    if random.flip(pm): # mutation with the probabilit pm
        j=random.rnd(0,Lnn-1)
        return G[i].edges[j].mate(G[i]).id
    return allele

def normalizeGraph(V):
    """
        Normalize the values of the vertices
    """
    # find the min and max values
    mx=copy.copy(V[0].value)
    mn=copy.copy(V[0].value)
    for j in range(1,len(V)):
        for i in range(len(V[j].value)):
            m = V[j].value[i]
            mx[i] =  max(m,mx[i])    
            mn[i] =  min(m,mn[i])    
    spread=N.subtract(mx,mn)

    # perform the normalization of the values
    for v in V:
        for i in range(len(v.value)):
            v.value[i]=(v.value[i]-mn[i])/spread[i]
     

def objectiveFunction(individual, graph,L,maxKCC=2):
    """
        The Mock objective function calculates the cluster
        Deviation and the Connectivity. The return value is a 
        dictionary with deviation and connectivity
    """  
    # get the cluster counts
    kcc=[0 for i in range(individual.x['k'])]
    for c in individual.x['kassign']:
        kcc[c]+=1
    kcc.sort()

    if individual.x['k'] >25 or kcc[0] < maxKCC:
        d=float('inf') 
        c=float('inf')
    else:
        d = clusterDeviation(individual.x['k'],individual.x['kassign'], graph)
        c = clusterConnectivity(individual.x['kassign'],graph,L)
    return dict(deviation=d,connectivity=c)

def primsAlgorithm(V,random=None):
    """
        Applies Prim's Algorithm to the specified adjacency list
        and returns the MST as a list of edges, E. If random is empty
        then the first vertex in the list is used as a starting point.
        
        random = ga.utilities.Random()
        random.warmupRandom(seedValue)
        V=createIrisGraph("afile") # returns a fully connected graph
        E=primsAlgorithm(V,random) # finds the minimun spanning tree for the givien graph
        
    """
    pq = []
         
    allE = sets.Set() # using a set so that we don't get duplicate edges
    for j in range(len(V)):
        v = V[j]
        for k in range(len(v.edges)):
            e = v.edges[k]
            allE.add(e)
    
    for e in allE:
        heapq.heappush(pq, e)
      
    Et = []
    Vt = [None]*len(V)
    
    v=0 if random==None else random.rnd(0,len(V)-1)
    Vt[v]=V[v]
    e=heapq.heappop(pq)
    i=1
    Etmp=[]
    while (e != None or i!=len(V)):
        if Vt[e.v1.id]!=None and Vt[e.v2.id]==None:
            Et.append(e);         
            Vt[e.v2.id]=e.v2
            i+=1
            for t in Etmp: 
                heapq.heappush(pq,t)
            Etmp=[]
        elif Vt[e.v2.id]!=None and Vt[e.v1.id]==None:
            Et.append(e)         
            Vt[e.v1.id]=e.v1
            i+=1
            for t in Etmp: 
                heapq.heappush(pq,t)
            Etmp=[]
        else: Etmp.append(e)
        e=heapq.heappop(pq) if len(pq)>0 else None
    
    for v in Vt:
        v.edges=[e for e in Et if e.mate(v)]
    return Et
    
#############
# Classes
#############

class Edge(object):
    """
        Class representing an edge in a graph
    """
    
    def __init__(self, v1, v2):
            
        self.v1 = v1
        self.v2 = v2
        self.w = None
        
    def mate(self, v):
        """
            Returns the mate if the given vertex exists in this edge
        """
        if self.v1 == v: return self.v2;
        if self.v2 == v: return self.v1;
        return None
   
    def weight(self):
        """
            returns the cosine similarity between vertices
        """
        if self.w==None:
            self.w=cosineSimilarity(self.v1.value,self.v2.value)
        return self.w
    
    def __eq__(self, other):
        if other==None: return False
        if(self.mate(other.v1)!=None and self.mate(other.v2)!=None): return True
    
    def __cmp__(self, other):
        if other==None: return 1
        if self.weight() < other.weight():return - 1
        if self.weight() == other.weight(): return 0
        return 1
    
    def __str__(self):
        s = "Edge<%s,%s,%f>" % (self.v1.__str__(), self.v2.__str__(), self.weight())
        return s
            
    
class HyperGrid(object):
    """ This represents a hypergrid used in region based niching"""        
    
    def __init__(self, dimension):
        """ Constructor """  
        self.dimension=dimension
        self.unit=1.0/dimension # float division
        self.grid = [[None for i in range(self.dimension)] for i in range(self.dimension)]
        self.max=None
        self.min=None
        
    def __getitem__(self,key):
        if isinstance(key,int):
            key=(int(key/self.dimension),key % self.dimension)
        return self.grid[key[0]][key[1]]
        
    def __setitem__(self, key, item): 
        """
          Set the niche.
          The key is a tuple (x,y)
          The item can be anything
            >>> key=tupe(5,2)
            >>> item=anObject
            >>> hypergrid[key]=item
        """
        if not isinstance(key,tuple):
            raise Exception('key must be a tuple')
        if self.grid[key[0]][key[1]]==None: self.grid[key[0]][key[1]]=[]
        self.grid[key[0]][key[1]].append(item)
        self.max =key if self.max==None or len(self.grid[key[0]][key[1]]) > len(self.grid[self.max[0]][self.max[1]]) else self.max
        self.min =key if self.min==None or len(self.grid[key[0]][key[1]]) < len(self.grid[self.min[0]][self.min[1]]) else self.min

    def getMaxNiche(self):
        return self.__getitem__(self.max)
         
    def clear(self):
        self.grid = [[None for i in range(self.dimension)] for i in range(self.dimension)]
        self.max=None
        self.min=None

class Individual(ga.common.Individual):

    def __cmp__ ( self, other ):
        """Define how to compare two Individual instances.
        """
        cmp=-1
        if self.fitness['connectivity']> other.fitness['connectivity']:
            cmp= 1 
        elif self.fitness['connectivity']== other.fitness['connectivity']:
            if self.fitness['deviation']< other.fitness['deviation']:
                cmp= 1
            elif self.fitness['deviation']== other.fitness['deviation']:
                cmp=0
        #print "%s %s %s" %(cmp,self,other)
        return cmp

class Mock(object):
    """ 
        Multiobjective Clustering with K-determiniation
    """   
    
    L=20
    GEN=200
    EPSIZE=1000
    Pc=.7
    
    def __init__(self,V,random):
        """
        Initializes the algorithm
        
        CONSTANT
        generations: 200
        L nearest neighbors is 20
        External Population Size: 1000
        Internal Population Size: N/20 where N is the number of vertices
        
        The algorithm requires a fully connected graph representing the dataset as 
        well as a seeded random number generator
        
        >>> import ga
        >>> from ga.mock import createIrisGraph,Mock
        >>> V=createIrisGraph("./bezdekIris.data")
        >>> random = ga.utilities.Random()
        >>> random.warmupRandom(seed)
        >>> mock = Mock(V,random)
        """
       
        self.Pm=1/len(V)
        self.hyperGridDepth=3
        self.niches=dict()
        self.random=random
        self.externalPop=[]
        self.internalPop=[]
        self.hyperboxDimension=(2**self.hyperGridDepth)
        self.hypergrid=HyperGrid(self.hyperboxDimension)
        self.nicheUnit=1.0/self.hyperboxDimension
        self.maxDeviation=None
        self.minDeviation=None
        self.maxConnectivity=None
        self.minConnectivity=None
        self.graph=V
        self.ipsize=max(50,int(len(V)/20))
        print "IP size:%s" % self.ipsize
        print "nicheUnit:%s" %self.nicheUnit 
    
    def initialize(self,V,random,popsize):
        """
        Creates an initialized population using the fully connected
        graph represented by the adjacency list V.
        
        V=createIrisGraph("./bezdekIris.data")
        internalPop, externalPop = initialize(V,self.random,20)
        """
    
        internalPop=[]
        lenV=len(V)
        for i in range(popsize):
            E = primsAlgorithm(V,random)
            chrom= Chromosome()
            chrom.alleles=createLocusBasedAdjacencyList(V,E)
            # remove i-1 longest links
            ilargest=heapq.nlargest(i%25, E)
            for edge in ilargest:
                chrom[edge.v1.id]=edge.v1.id
            x=decode(chrom) # This decodes the number of clusters
            individual = Individual(chrom,len(chrom),x,0,niche=0,normalized=False, attainmentScore=None)
            internalPop.append(individual) 
            individual.fitness=objectiveFunction(individual,self.graph,self.L,maxKCC=1) 
            self.updateMaxMin(individual)
             
        #print "maxD:%s minD:%s" %(self.maxDeviation,self.minDeviation)
        #print "maxC:%s minC:%s" %(self.maxConnectivity,self.minConnectivity)
        for individual in internalPop:
            self.normalizeObjectiveFunction(individual)
            #print "k[%s] %s," %(individual.x['k'],individual.fitness)
            self.updateExternalPopulation(individual)

        print "Gen[%s,%s] %s" % (-1,len(self.externalPop),self.niches)
        for e in self.externalPop:
            #print "k[%s] %s," %(e.x['k'],e.fitness)
            pass
        return internalPop  
     
    def updateMaxMin(self,individual):
        if individual.fitness['deviation']==float('inf'): return
        if(self.maxConnectivity==None):
            self.maxConnectivity=individual.fitness['connectivity']
            self.minConnectivity=individual.fitness['connectivity']
            self.maxDeviation=individual.fitness['deviation']
            self.minDeviation=individual.fitness['deviation']
        else:
            self.maxConnectivity=max(individual.fitness['connectivity'],self.maxConnectivity)
            self.minConnectivity=min(individual.fitness['connectivity'],self.minConnectivity)
            self.maxDeviation=max(individual.fitness['deviation'],self.maxDeviation)
            self.minDeviation=min(individual.fitness['deviation'],self.minDeviation)
        
        
         
    def normalizeObjectiveFunction(self,individual):
        if individual.fitness['deviation']==float('inf'): return
        if individual.normalized==False:
            if self.maxDeviation-self.minDeviation > 0:
                dDenom=(self.maxDeviation-self.minDeviation)
                cDenom=(self.maxConnectivity-self.minConnectivity)
                individual.fitness['deviation']=(individual.fitness['deviation']-self.minDeviation)/dDenom
                individual.fitness['connectivity']=float(individual.fitness['connectivity']-self.minConnectivity)/cDenom
            elif self.maxDeviation-self.minDeviation==0: 
                individual.fitness['deviation']=1
                individual.fitness['connectivity']=1
            individual.normalized=True 
      
    def updateExternalPopulation(self,individual):
        """ Updates externalPop with the solution, if it dominates """
        lEP=len(self.externalPop)
        dominatedIndiv=[]
        for i in range(lEP):
            pareto=getSolutionParetoRelationship(individual, self.externalPop[i]) 
            if(pareto >= Pareto.NONDOMINATED):
                if pareto == Pareto.DOMINATES:
                    dominatedIndiv.append(i)
            else: 
                return # solution is dominated 

        dominatedIndiv.sort(reverse=True)
        for i in dominatedIndiv:
            self.externalPop.pop(i)
        self.externalPop.append(individual)

        externalPopFull=len(self.externalPop) > self.EPSIZE
        if externalPopFull and self.hypergrid.getMaxNiche()!=None:
            maxNiche=self.hypergrid.getMaxNiche()
            i=self.random.rnd(0,len(maxNiche)-1)
            self.externalPop.pop(i)
        
        
        # update niche counts
        self.hypergrid.clear()
        self.niches.clear()
        for i in range(len(self.externalPop)):
            s=self.externalPop[i]
            s.niche= getNiche(s,self.hypergrid.dimension,self.hypergrid.unit)
            self.hypergrid[s.niche]=i
            try:
                self.niches[s.niche]+=1
            except:
                self.niches[s.niche]=1
                
    def run(self,outputDir='.'):
        """ Runs the mock algorithm on the data set and five control sets
        and then normalize to find the 'best' solution.

        Normalization of the original 'solution front' using the 
        'reference fronts'. Since there is a set of solutions for 
        every value of k and it is not clear how individual points 
        in the solution front should be normalized. The following 
        is a heuristic approach to this.
       
        1) Restrict analysis to solutions with clusters in the range 
           [1, kMax] where kMax is the highest number of clusters 
           shared by all fronts AND where solutions points are 
           not dominated by any reference point.

        2) After filtering, normalize deviation and connectivity 
           to be in region [0,1] x [0,1]

        3) Take the square root of each normalized point to give 
           higher degree of emphsis to small but distince changes in the objectives

        4) Compute attainment surfaces: 
           For each point in the solution front 
            1) compute the distance to the attainment surfaces for
               each reference front 
            2) for each solution point p compute the attainment 
               score as the Euclidean distance between p and the 
               closest point on the reference attainment surface.

        5) plot attainment scores as a function of the number of clusters
        """
        solutionFront=self.mock(self.graph)
        self.writeParetoFront('%s/paretofront.txt' % outputDir,solutionFront)
        controlFront=[]
        for i in range(5):
            V=createNormalizedUniformlyRandomGraph(len(self.graph),2,self.random)
            controlFront.append(self.mock(V))
            self.writeParetoFront('%s/controlFront%s.txt' % (outputDir,i),controlFront[i])

        # 1) 
        # Restrict analysis to solutions with clusters in the range 
        # [1, kMax] where kMax is the highest number of clusters 
        # shared by all fronts AND where solutions points are 
        # not dominated by any reference point.
        kSF=self.maxK(solutionFront)
        kCF=self.maxK(controlFront[0])
        for i in range(1,5):
            k=self.maxK(controlFront[i])
            kCF=min(k,kCF)
        kMax=min(kSF,kCF)
        solutionFront=self.filter(solutionFront,kMax,controlFront)
        for i in range(5):
            #cfi=[controlFront[j] for j in range(5) if i !=j]
            controlFront[i]=self.filter(controlFront[i],kMax)

        # 2) 
        # After filtering, normalize deviation and connectivity 
        # to be in region [0,1] x [0,1]
        solutionFront=self.normalize(solutionFront)
        for i in range(5):
            controlFront[i]=self.normalize(controlFront[i])

        # 3)
        # Take the square root of each normalized point to give 
        # higher degree of emphsis to small but distince changes in the objectives
        for i in range(5):
            for s in controlFront[i]:
                s.fitness['deviation']=math.sqrt(s.fitness['deviation'])
                s.fitness['connectivity']=math.sqrt(s.fitness['connectivity'])
        for s in solutionFront:
            s.fitness['deviation']=math.sqrt(s.fitness['deviation'])
            s.fitness['connectivity']=math.sqrt(s.fitness['connectivity'])

        # 4) 
        # Compute attainment surfaces
        bestSolution=-1
        bestScore=-1
        cfScore=None
        for s in solutionFront:
            minDistance=sys.float_info.max
            minCFPoint=None
            for cf in controlFront:
                for c in cf: 
                    score=euclideanDistance((s.fitness['deviation'],s.fitness['connectivity']),(c.fitness['deviation'],c.fitness['connectivity']))
                    minDistance=min(score,minDistance)
                    if minDistance==score: minCFPoint=c
            bestScore=max(bestScore,minDistance)
            s.attainmentScore=minDistance
            if bestScore==minDistance: 
                bestSolution=s
                cfScore=minCFPoint

        self.writeParetoFront('%s/paretofront_nf.txt' % outputDir,solutionFront)
        for i in range(5):
            self.writeParetoFront('%s/controlFront%s_nf.txt' % (outputDir,i),controlFront[i])
        print bestSolution
        print cfScore
        return dict(best=bestSolution, control=cfScore)

    def maxK(self,solutionSet):
        """ returns the largest k encountered in the solution set"""
        maxK=0
        for s in solutionSet:
            maxK=max(s.x['k'],maxK)

    def normalize(self,solutionSet):
        self.maxDeviation=None
        self.minDeviation=None
        self.maxConnectivity=None
        self.minConnectivity=None
        for s in solutionSet:
            self.updateMaxMin(s)
        
        for s in solutionSet:
            self.normalizeObjectiveFunction(s)
        return solutionSet

    def filter(self,solutionSet,maxK,controlFronts=None):
        """ Filters out all solutions outside of the range [1,maxK].
            If a list of control fronts are given then the the solutions
            dominated by reference points are removed. """
        for s in solutionSet:
            remove=True
            if s.x['k'] <= maxK:
                if controlFronts == None:
                   remove=False
                else:
                    for cf in controlFronts:
                        for c in cf:
                            if getSolutionParetoReslationship(s,cf)>Pareto.DOMINATED:
                               remove=False 
                
            if remove: solutionSet.remove(s)
        
        return solutionSet


    def mock(self,graph):
        self.externalPop=[]
        self.niches=dict()
        self.hypergrid=HyperGrid(self.hyperboxDimension)
        self.internalPop=self.initialize(graph,self.random,self.ipsize)
        for i in range(self.GEN):
            # Reset member variables
            self.internalPop=[] # reset the internal population
            self.maxDeviation=None
            self.minDeviation=None
            self.maxConnectivity=None
            self.minConnectivity=None

            for j in range(self.ipsize):
                #select a populated niche uniformly at random from externalPop
                listNiches=self.niches.items()
                n=self.random.rnd(0,len(listNiches)-1)

                #select a solution uniformly at random from niche
                niche=self.hypergrid[listNiches[n][0]]
                
                #IP=IP U {si}
                s=self.random.rnd(0,len(niche)-1)
                self.internalPop.append(self.externalPop[niche[s]])
                
            # mate the selected parents
            for j in range(0,self.ipsize,2):
                parent1=self.internalPop[j]
                parent2=self.internalPop[j+1]
                xsite,chrom1,chrom2=crossoverUniform(parent1.chrom,
                        parent2.chrom, self.random,
                        self.Pc,self.Pm,self.graph,self.L)
                x=decode(chrom1)
                child1 = Individual(chrom1,len(chrom1),x,0,niche=0,normalized=False,attainmentScore=None)
                child1.xsite=xsite
                child1.fitness=objectiveFunction(child1,self.graph,self.L) 
                self.updateMaxMin(child1)

                x=decode(chrom2)
                child2 = Individual(chrom2,len(chrom2),x,0,niche=0,normalized=False,attainmentScore=None)
                child2.xsite=xsite
                child2.fitness=objectiveFunction(child2,self.graph,self.L) 
                self.updateMaxMin(child2)

                self.internalPop[j]=child1
                self.internalPop[j+1]=child2
                
            for j in range(self.ipsize):
                indiv=self.internalPop[j]
                self.normalizeObjectiveFunction(indiv)
                self.updateExternalPopulation(indiv)

        print "Gen[%s,%s] %s" % (self.GEN,len(self.externalPop),self.niches)
        for e in self.externalPop:
            #print "k[%s] %s," %(e.x['k'],e.fitness)
            pass
        return copy.copy(self.externalPop)


    def writeParetoFront(self,filename,population):
        """ Write the current pareto front to a text file """
        f=open(filename,'w')
        population.sort()
        for e in population:
            f.write("%s:%s:%s:%s:%s\n" %(e.x['k'],e.fitness['deviation'],
                e.fitness['connectivity'],e.attainmentScore,e.x['kassign']))

class Pareto:
    """ Enumeration for Pareto Relationships """
    DOMINATED=0
    NONDOMINATED=1
    DOMINATES=2

class Vertex(object):
    '''
        Class representing a vertex in the graph. Attributes 
        are
        
        id = a unique identifier
        value = the value of the vertex usually an n-tuple
        group = this can be the classification of the vertex
                which is used for training purposes
        edges = a list of Edge objects
    '''


    def __init__(self, group, value, id, edges=None):
        '''
        Constructor
        '''
        self.edges = [] if edges == None else edges
        self.value = value
        self.group = group
        self.id=id
        
    def __eq__(self, other):
        if other == None: return False
        return self.id == other.id

    def __str__(self):
        s = "Vertex%s" % (self.value.__str__())
        return s
       
