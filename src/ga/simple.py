'''
Created on Jan 7, 2011

This module defines the data structures for a simple genetic algorithm
    Goldberg, David. (1989). Genetic Algorithms in Search, 
    Optimization and Machine Learning. Appendix Chapter 3 

Classes:

Individual - an individual in a population
SimpleGeneticAlgorithm  - a simple tripartite algorithm

Functions:

initData -  Gets user input for the initalization of the GA
initReport - Report header for SGA's output

Exceptions:


@author: Val Hendrix (val.hendrix@me.com)
'''

from __future__ import division
import copy
import ga
from ga.common import Individual

__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 7, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'

    

class Chromosome(ga.common.Chromosome):
    ''' An artificial chromosomve '''
    
    
    
    def __init__(self):
        ''' Constructor 
            
            Populations the chromosomes alleles to the length
        '''
        super(Chromosome, self).__init__()
        self.uint = 0
            
    def __getitem__(self, key): 
        """
            Return boolean representing the allele for the given key
            >>> Chromosome(length=20)[1]
        """
        return self.alleles[key]
    
    def __setitem__(self, key, item): 
        """
           Set the allele representing the key with the item
            >>> chrom=Chromosome(length=20)
            >>> chrom[1]=True
        """
        
        if(key >= len(self.alleles) or item != self.alleles[key]):
            if item:
                self.uint += pow(2, key)
            elif key < len(self.alleles):
                self.uint -= pow(2, key)
        self.__setattr__(key,item)
       
    def __str__(self):
        s = ""
        for i in range(len(self.alleles)-1,-1,-1):
            s += '1' if self.alleles[i] else '0' 
        return s
   
        


    
class SimpleGeneticAlgorithm(object):
    ''' 
        A simple genetic algorithm (SGA) as defined
        in Goldberg, David. (1989). Genetic Algorithms in Search
        Optimization & Machine Learning.
    '''
    
    def __init__(self, random, popsize=100, lchrom=30, maxgen=100, pcross=.5, pmutation=.000000001):
        ''' Constructor 
            Initializes the population with random individuals
        '''
        self.oldpop = []         # Two non-overlapping populations
        self.newpop = []   
        for i in range(popsize):
            self.oldpop.append(None) 
        for i in range(popsize):
            self.newpop.append(None)         
        self.gen = 0
        self.sumfitness = 0.0    # sum of population fitness (Sigma f)
        self.nmutation = 0
        self.ncross = 0               # Integer Statistics
        self.avg = 0.0
        self.max = 0.0
        self.min = 0.0             # Float Statistics
        self.random = random
        self.popsize = popsize
        self.lchrom = lchrom
        self.maxgen = maxgen
        self.pcross = pcross
        self.pmutation = pmutation
        self.coef = pow(2,self.lchrom)-1   # coefficient to normalize the domain 2^30-1  where 30 is the string size
       
        for j in range(self.popsize):
            ''' initial population generation '''
            chrom = Chromosome(length=self.lchrom)
            for j1 in range(self.lchrom):
                chrom[j1] = self.random.flip(0.5)
            x = self.decode(chrom)
            fitness = (self.objfunc(x))
            parent1 = 0
            parent2 = 0
            xsite = 0
            self.oldpop[j]=Individual(chrom, lchrom, x, fitness, parent1, parent2, xsite)
            
        self.statistics(self.oldpop)
                
                    
    
    def crossover(self, parent1, parent2, child1, child2):
        '''Cross two parent strings, place in two child strings '''
        j = 0
        if self.random.flip(self.pcross):                   # Do flip with p(cross)
            jcross = self.random.rnd(1, self.lchrom - 1)    # Cross between 1 and l-1
            self.ncross += 1                                # Increment crossover counter
        else:
            jcross = self.lchrom
        
        # First exchange, 1 to 1 and 2 to 2
        for j in range(jcross):
            child1[j] = self.mutation(parent1[j])
            child2[j] = self.mutation(parent2[j])
            
        # Second Exchange, 1 to 2 and 2 to 1
        if jcross != self.lchrom:
            for j in range(jcross + 1, self.lchrom):
                child1[j] = self.mutation(parent2[j])
                child2[j] = self.mutation(parent1[j])   
        return jcross,child1,child2
            
    def mutation(self, allele):
        ''' 
            Mutate and allele with pmutation, count number
            of mutations
        '''
        mutate = self.random.flip(self.pmutation)   #Flip biased coin
        mutation = allele
        if mutate:
            self.nmutation += 1
            mutation = False if allele else True                  #Change bit value
        return mutation
            
    def select(self):
        ''' Select a single individual via roulette wheel selection '''
        
        partsum = 0.0 # parial sum
        rand = self.random.random() * self.sumfitness
        for j in range(self.popsize):
            ''' Find wheel slot '''
            partsum += self.oldpop[j].fitness
            if partsum >= rand or j == self.popsize: break
            
        return j
    
    def decode(self, chrom):
        '''
        Decode string as unsigned binary integer
        '''
        return chrom.uint
    
    def objfunc(self, x):
        ''' Fitness function - f(x) = x**n '''
        n = 10
        return pow(float(x) / self.coef, n)
    
    def generation(self):
        '''
        Create a new generation through select,crossover, and mutation.
        Generation assumes the population is even numbered
        '''
        for j in range(0, self.popsize, 2):
            # select crossover, and mutation until newpop is filled
            mate1 = self.select() # pick a pair of mates
            mate2 = self.select() # what if it mates with itself
            
            child1=Individual(chrom=Chromosome(length=self.lchrom))
            child2=Individual(chrom=Chromosome(length=self.lchrom))
            
            #Crossover and mutation - mutation embedded w/in crossover
            jcross,child1.chrom,child2.chrom = self.crossover(self.oldpop[mate1].chrom, self.oldpop[mate2].chrom,
                      child1.chrom, child2.chrom)
            
            #Decode string, evaluate fitness and record parentage data on both children
            child1.x = self.decode(child1.chrom)
            child1.fitness = self.objfunc(child1.x)
            child1.parent1 = mate1
            child1.parent2 = mate2
            child1.xsite = jcross
            child2.x = self.decode(child2.chrom)
            child2.fitness = self.objfunc(child2.x)
            child2.parent1 = mate1
            child2.parent2 = mate2
            child2.xsite = jcross 
            
            self.newpop[j]=child1
            self.newpop[j+1]=child2
            
            
    def statistics(self, pop):
        ''' Calculate population statistics '''
        s = self
        s.sumfitness = pop[0].fitness
        s.min = pop[0].fitness
        s.max = pop[0].fitness
            
        for j in range(1, s.popsize):
            p = pop[j]
            s.sumfitness += p.fitness
            s.max = p.fitness if p.fitness > s.max else s.max
            s.min = p.fitness if p.fitness < s.min else s.min
        s.avg = s.sumfitness / s.popsize
            
    def report(self):
        print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        print " Population Report"
        print " Generation %d\t\t\t\t\t\t\t\t\t\t\t\tGeneration %d" % (self.gen, self.gen+1)
        print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        print "%s\t%s\t\t\t\t%s\t\t%s\t\t\t|\t%s\t%s\t%s\t%s\t\t\t\t%s\t\t%s" % ('#','string','x','fitness','#','parents','xsite','string','x','fitness')
        for i in range(self.popsize):
            op = self.oldpop[i]
            np = self.newpop[i]
            print "%d)\t%s\t%d\t%.15f\t|\t%d)\t%s" % (i, op.chrom, op.x, op.fitness, i, np)
        print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        print " Generation %d & Accumulation Statistics:\t max:%.15f\t min:%.15f\tsumfitness:%.15f\tavg:%.15f\tnmutation:%d\tncross:%d" % (self.gen, self.max, self.min, self.sumfitness,self.avg, self.nmutation, self.ncross)
        print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        
    def run(self):
        ''' run the algorithm '''
        s = self
        s.gen = 0
        for s.gen in range(s.maxgen):
            s.generation()
            s.statistics(s.newpop)
            s.report()
            s.oldpop = copy.copy(s.newpop)
                
    
        
        
    
        
    
        
