'''
Created on Jan 7, 2011

This module defines the data structures for a traveling salesman genetic algorithm

Classes:

TSPGeneticAlgorithm  - a TSP genetic algorithm

Functions:

population - creates the initial population for the TSP genetic algoirthm

Exceptions:


@author: Val Hendrix (val.hendrix@me.com)
'''
   
import ga
from ga.common import Individual

__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 7, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'
__copyright__ = "(C) 2011 Val Hendrix."

 
def population(self):
    """
       Creates the initial population for the TSP genetic algoirthm.
       This functione expects a TSPGeneticAlgorithm instance or at 
       least an object with the following attributes
       
       popsize - size of the population
       lchrom - size of the chromosime
       random - a PRNG
       decode(chrom) - a function for decoding the chromosime
       oldpop - the old population array to create
       maxx - the max x value of all individuals in the population
       minx - the min x value of all individuals in the population
       
    """
    for j in range(self.popsize):
        ''' initial population generation '''
        chrom = ga.common.Chromosome()
        alleles=range(self.lchrom)
        for j1 in range(self.lchrom):
            index=self.random.rnd(0,len(alleles)-1)
            chrom[j1] = alleles[index]
            alleles.pop(index)
        x = self.decode(chrom)
            
        self.oldpop[j]=Individual(chrom, self.lchrom, x, 0)
        self.maxx=max(x,self.maxx)  
        self.minx=max(x,self.minx)             

    
class TSPGeneticAlgorithm(ga.common.GeneticAlgorithm):
    ''' 
        A traveling salesman problem solver.
    '''
    
    def __init__(self, random, graph, popsize=100, maxgen=100, pcross=.5, pmutation=.000000001,verbose=False):
        ''' Constructor 
            Initializes the population with random individuals
        '''
        
        # set the TSP specific data
        self.graph=graph
        self.lchrom = len(graph)
        
        # set the anonymous population function
        self.initializePop= lambda: population(self)
        
        super(TSPGeneticAlgorithm,self).__init__(random, popsize, maxgen, pcross, pmutation,verbose)
           
                    
    
    def crossover(self, indiv1, indiv2):
        '''Cross two parent strings, place in two child strings '''
        indivc1=Individual(chrom=ga.common.Chromosome())
        indivc2=Individual(chrom=ga.common.Chromosome())
        child1=indivc1.chrom
        child2=indivc2.chrom
        parent1=indiv1.chrom
        parent2=indiv2.chrom
        
        j = 0
        
        if self.random.flip(self.pcross):                   # Do flip with p(cross)
            one = self.random.rnd(1, self.lchrom - 1)
            two =  self.random.rnd(1, self.lchrom - 1) 
            jcross1=min(one,two)
            jcross2=max(one,two)  # Cross between 1 and l-1
            self.ncross += 1                                # Increment crossover counter
        else:
            jcross1 = self.lchrom
            jcross2 = self.lchrom
        
        if jcross2-jcross1>0:
            # First exchange, 1 to 1 and 2 to 2
            crossoverRange=range(jcross1,jcross2+1)
            parent1Part=[]  #hold partial parents
            parent2Part=[]
            i=0
            for j in range(self.lchrom):
                ''' separate the alleles inside the crossover from
                    those that are outside
                '''
                if(j in crossoverRange):
                    child1[i] = parent1[j]
                    child2[i] = parent2[j]
                    i+=1
                else:
                    parent1Part.append(parent1[j])
                    parent2Part.append(parent2[j])
                    
            
            # Now add the rest of the alleles to the children in order
            # get remaining alleles from parent 1
            j=len(child2)
            if(len(child1)< self.lchrom):
                for p in parent2Part:
                    if p not in child1:
                        child1[i]=p
                        i+=1
                    elif p not in child2:
                        child2[len(child2)]=p
                # not get the others from parent two
                for p in parent1Part:
                    if p not in child1:
                        child1[i]=p
                        i+=1
                    elif p not in child2:
                        child2.alleles.insert(j,p)
                        j+=1
                
        else:
            for j in range(self.lchrom):
                child1[j] = parent1[j]
                child2[j] = parent2[j]
            
        return (jcross1,jcross2),indivc1,indivc2
    
    def mutate(self, i,chrom):
        ''' 
            Mutate and allele with pmutation, count number
            of mutations
        '''
        mutate = self.random.flip(self.pmutation)   #Flip biased coin
        d=self.decode(chrom)
        mutation = chrom[i]
        if mutate:
            self.nmutation += 1
            j = self.random.rnd(0, self.lchrom - 1)
            chrom[i]=chrom[j]
            chrom[j]=mutation
            if d < self.decode(chrom):
                chrom[j]=chrom[i]
                chrom[i]=mutation
                
    
    def decode(self, chrom):
        '''
        Decode string as unsigned binary integer
        '''
        distance=0
        for j in range(1,len(chrom)):
            distance += self.graph[chrom[j]][chrom[j - 1]]
        return distance
    
    def objfunction(self,individual):
        return float(self.maxx)/float(individual.x)-1
    
      
     
          
    