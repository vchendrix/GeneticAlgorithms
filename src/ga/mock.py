'''
Created on Jan 18, 2011

This module defines the functions and classes that support
the MOCK (Multiobjective Clustering with K-Determination) 
algorithm.

Classes

Edge - defines an edge in a graph
Mock - the MOCK genetic algorithm
Vertex - define a vertex in a graph

Functions

clusterConnectivity - determines the cluster deviation of a solution (chromosome) based on
    its decoded value which is the number of clusters and the cluster assignments
clusterDeviation - determines the cluster deviation of a solution (chromosome) based on
    its decoded value which is the number of clusters and the cluster assignments
createIrisGraph - this is a specific function that creates a Graph (adjacency list) for the Iris dataset 
    from the UCI Machine Learning dataset
createLocusBasedAdjacencyList - takes a graph (adjacency list) and returnes it representation
    in locus based adjacency form
crossoverUniform - performes uniform crossover between two mates
decode - decodes the Mock algorithms Chromosome which is a graph  using
    a locus based adjacency representation and stored as a python list
euclideanDistance - returns the euclidean distance between two n-tuples
mutationNearsetNeighbor -
objectiveFunction - the multi-objective function returns a dictionary containing the
    deviation and connectivity objectives
primsAlgorithm - returns the minimum spanning tree of the given graph (adjacency list)

@author: val
'''
__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 18, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'

import copy
import heapq
import math
import sets

from ga.common import Chromosome, Individual

#############
# Functions
#############

def clusterConnectivity(kassign,graph):
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
        l = 20 if len(v.edges)>20 else len(v.edges)
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
        k=kassign[i]
        kN[k]+=1
        if kMeans[k]==[]: kMeans[k]=list(v.value)
        else:
            for j in range(len(v.value)):
                kMeans[k][j]+=v.value[j]
        
    # divided all the summed n-tuples from the vertices
    # by the number of data items in the cluster
    for i in range(k):
        for j in range(len(kMeans[i])):
            kMeans[k][j]=kMeans[k][j]/ kN[i]
            
    deviation=0
    for i in range(len(graph)):
        v=graph[i]
        k=kassign[i]
        deviation+=euclideanDistance(kMeans[k],v.value) 
    return deviation

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
            value = tuple(float(l) for l in line[0].split(","))
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

def crossoverUniform(parent1,parent2,random,pcross=.7):
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
                child1[i]=parent2[i]
                child2[i]=parent1[i]
            else:
                xsite+="0"
                child1[i]=parent1[i]
                child2[i]=parent2[i]
    else:
        xsite='0'*len(parent1)
        child1.alleles=copy.copy(parent1.alleles)
        child2.alleles=copy.copy(parent2.alleles)
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
    
    
    ctr=0
    previous=[None]*len(chrom)
    for i in range(len(chrom)):
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
    print "k:%d, kassgin:%s" %(cc+1,clusterAssignment)
    return dict(k=cc+1,kassign=clusterAssignment)                 

def euclideanDistance(x,y):
    """ Finds the euclidean distance between two n-tuples """
    d = 0
    for i in range(len(x)):
        d += (x[i] - y[i]) ** 2
    d = math.sqrt(d)
    return d 
            
def mutationNearestNeighbor():
    pass

def objectiveFunction(individual, graph):
    """
        The Mock objective function calculates the cluster
        Deviation and the Connectivity. The return value is a 
        dictionary with deviation and connectivity
    """  
    
    d = clusterDeviation(individual.x['k'],individual.x['kassign'], graph)
    c = clusterConnectivity(individual.x['kassign'],graph)
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
        
        V=createIrisGraph("./bezdekIris.data")
        random = ga.utilities.Random()
        random.warmupRandom(seed)
        mock = Mock(V,random)
        """
        
        self.random=random
        self.niches=[]
        self.graph=V
        self.ipsize=max(50,int(len(V)/20))
        self.internalPop,self.externalPop=self.initialize(V,random,self.ipsize)
        pass  
    
    def initialize(self,V,random,popsize):
        """
        Creates an initialized population using the fully connected
        graph represented by the adjacency list V.
        
        V=createIrisGraph("./bezdekIris.data")
        internalPop, externalPop = initialize(V,self.random,20)
        """
    
        internalPop=[]
        externalPop=[]
        lenV=len(V)
        for i in range(popsize):
            E = primsAlgorithm(V,random)
            chrom= Chromosome()
            chrom.alleles=createLocusBasedAdjacencyList(V,E)
            # remove i-1 longest links
            ilargest=heapq.nlargest(i%lenV, E)
            for edge in ilargest:
                chrom[edge.v1.id]=edge.v1.id
            x=decode(chrom) # This decodes the number of clusters
            individual = Individual(chrom,len(chrom),x,0)
            internalPop.append(individual) 
            individual.fitness=objectiveFunction(individual,self.graph) 
            self.updateExternalPopulation(individual,externalPop)
                
        return internalPop,externalPop  
      
    def isSolutionNondominated(self,s1,s2):
        """ return True if s1 is not dominated by s2 """
        if s1.fitness.deviation < s1.fitness.deviation or s2.fitness.deviation < s2.fitness.deviation:
            return True
    
    def updateExternalPopulation(self,solution,externalPop):
        """ Updates externalPop with the solution, if it dominates """
        nondominated=False
        for i in externalPop:
            s=externalPop[i]
            if(self.isSolutionNondominated(solution, s)):
                nondominated=True
                externalPop.remove(s)
        if nondominated and len(self.externalPop) < self.EPSIZE:
            externalPop.append(solution)
        else:
            pass # need to figure out how to manage niches
    
    def run(self):
        for i in range(self.GEN):
            for j in range(self.ipsize):
                #select a populated niche uniformly at random from externalPop
                #select a solution uniformly at random from niche
                #IP=IP U {si}
                pass
            for j in range(self.ipsize):
                if self.random.flip(self.Pc):
                    # crossover
                    pass
                #mutate
                j+=2
            for j in range(self.ipsize):
                self.internalPop[j].fitness=objectiveFunction(self.internalPop[j],self.graph) 
                self.updateExternalPopulation(self.internalPop[j])
            self.internalPop=[]
            
            
                
            
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
            returns the Euclidean distance between vertices
        """
        return euclideanDistance(self.v1.value,self.v2.value)
    
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
        
