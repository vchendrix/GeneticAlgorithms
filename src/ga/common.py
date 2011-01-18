'''
Created on Jan 17, 2011

Classes:

Individual - an individual in a population


Functions:


Exceptions:


@author: Val Hendrix (val.hendrix@me.com)
'''
__version__ = '0.1'
__author__  = "Val Hendrix (val.hendrix@me.com)"
__date__    = 'Jan 17, 2011'
__url__     = 'https://github.com/valreee/GeneticAlgorithms'

import copy
from ga.utilities import Random


def initData():
    ''' Get user input for the initalization of the
        GA
        
        Returns popsize, lchrom, maxgen, pcross, pmutation, random
    '''
    
    popsize = input("Enter population size      : ")
    lchrom = input("Enter chromosome length    : ")
    maxgen = input("Enter max generations      : ")
    pcross = input("Enter crossover probability: ")
    pmutation = input("Enter mutation probability : ")
    random = Random()
    random.randomize()
    return popsize, lchrom, maxgen, pcross, pmutation, random

def initReport(sga):
    print "------------------------------------------------------------------------------------------------------------------------------------\n"
    print "      A Simple Genetic Algorithm in Python - SGAP - v %s" % __version__
    print "                    Val Hendrix 2011"
    print "------------------------------------------------------------------------------------------------------------------------------------\n"
    print "     SGAP Paramters"
    print "     --------------"
    print "  Population Size (popsize)          : %d" % sga.popsize
    print "  Chromosome length (lchrom)         : %d" % sga.lchrom
    print "  Max # of generations (maxgen)      : %d" % sga.maxgen
    print "  Crossover probability (pcross)     : %.3f" % sga.pcross
    print "  Mutation probability (pmutation)   : %.3f" % sga.pmutation
    print "     Intial Generation Statistics"
    print "     --------------"
    print "  Initial Population maximum fitness : %.3f" % sga.max
    print "  Initial Population average fitness : %.3f" % sga.avg
    print "  Initial Population minimum fitness : %.3f" % sga.min
    print "  Initial Population sum of fitness  : %.3f" % sga.sumfitness
    print "  Initial Population maximum x : %.3f" % sga.maxx
    print "  Initial Population average x : %.3f" % sga.avgx
    print "  Initial Population minimum x : %.3f" % sga.minx
    print "  Initial Population sum of x  : %.3f" % sga.sumx
    print "------------------------------------------------------------------------------------------------------------------------------------\n"
    
def selectRoulette(random,sumfitness,pop):
        ''' Select a single individual via roulette wheel selection '''
        popsize=len(pop)
        partsum = 0.0 # parial sum
        rand = random.random() * sumfitness
        for j in range(popsize):
            ''' Find wheel slot '''
            partsum += pop[j].fitness
            if partsum >= rand or j == popsize: break
            
        return j 

class Chromosome(object):
    '''
    An artificial chromosome 
    '''


    def __init__(self):
        ''' Constructor 
            
            Populations the chromosomes alleles to the length
        '''
        self.alleles = []  
        
    def __len__(self):
        return len(self.alleles)    
            
    def __getitem__(self, key): 
        """
            Return value representing the allele for the given key
            >>> print Chromosome()[1]
        """
        return self.alleles[key]
    
    def __setitem__(self, key, item): 
        """
           Set the allele representing the key with the item
        """
        if(key == len(self.alleles)):
            self.alleles.append(item)
        else:
                    
            self.alleles[key] = item
            
    def __str__(self):
        s = ""
        length=len(self.alleles)
        if length==0: return "<empty>"
        for i in range(length):
            s+="%d:" % self.alleles[i]
        return s

class Individual(object):
    '''
    An individual in a population
    Methods:
    
    none
    
    
    Special methods:

    Also available are the operators []
    
    Properties:
    
    chrom -- An artificial chromosome or bit string
    fitness -- Objective function value
    max -- the maximun length of a chromosome
    parent1 -- parent of individual
    parent2 -- parent of individual
    x -- Phenotype - unsigned integer
    xsite -- Crossover site

    bin -- The bitstring as a binary string.
    bool -- For single bit bitstrings, interpret as True or False.
    
    '''
    
    def __init__(self, chrom, max=0, x=0, fitness=0, parent1=0, parent2=0, xsite=(0,0)):
        ''' Constructor '''
        self.max = max    
        self.chrom = chrom  # Genotype - bitstring
        self.x = x                                # Phenotype - unsigned integer
        self.fitness = fitness                    # Objective function value
        self.parent1 = parent1                    # Parents and crossover point
        self.parent2 = parent2
        self.xsite = xsite
        
        
    
    def __str__(self):
        return "(%d,%d)\t%s\t%s\t%d\t%.15f" % (self.parent1, self.parent2, self.xsite, self.chrom, self.x, self.fitness)
 
class GeneticAlgorithm(object):
    ''' 
        A simple genetic algorithm (SGA) as defined
        in Goldberg, David. (1989). Genetic Algorithms in Search
        Optimization & Machine Learning.
    '''
    
    def __init__(self, random, popsize=100, maxgen=100, pcross=.5, pmutation=.000000001,verbose=False,):
        ''' Constructor 
            Initializes the population with random individuals
        '''
        self.verbose=verbose
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
        self.min = 0.0           # Float Statistics
        self.random = random
        self.popsize = popsize
        self.maxgen = maxgen
        self.pcross = pcross
        self.pmutation = pmutation 
        self.sumx=0
        self.maxx=0
        self.minx=0
        self.avgx=0

        self.initializePop()
            
        self.statistics(self.oldpop)
                
    def initializePop(self):
        pass          
    
    def crossover(self, parent1, parent2, child1, child2):
        '''Cross two parent strings, place in two child strings '''
        pass
    
    def mutation(self,chrom):
        for i in range(len(chrom)):
            self.mutate(i,chrom)
        return chrom
            
    def mutate(self, i,chrom):
        pass
      
    def select(self):
        return selectRoulette(self.random,self.sumfitness,self.oldpop)
    
    def decode(self, chrom):
        pass
    
    
    def generation(self):
        '''
        Create a new generation through select,crossover, and mutation.
        Generation assumes the population is even numbered
        '''
        maxx=0
        minx=9999999999
        for j in range(0, self.popsize, 2):
            # select crossover, and mutation until newpop is filled
            mate1 = self.select() # pick a pair of mates
            mate2 = self.select() # what if it mates with itself
            
            child1=Individual(chrom=Chromosome())
            child2=Individual(chrom=Chromosome())
            
            #Crossover and mutation - mutation embedded w/in crossover
            jcross,child1.chrom,child2.chrom = self.crossover(self.oldpop[mate1].chrom, self.oldpop[mate2].chrom,
                      child1.chrom, child2.chrom)
            child1.chrom=self.mutation(child1.chrom)
            child2.chrom=self.mutation(child2.chrom)
            
            
            #Decode string, evaluate fitness and record parentage data on both children
            child1.x = self.decode(child1.chrom)
            child1.parent1 = mate1
            child1.parent2 = mate2
            child1.xsite = jcross
            child2.x=self.decode(child2.chrom)
            child2.parent1 = mate1
            child2.parent2 = mate2
            child2.xsite = jcross 
            
            self.newpop[j]=child1
            self.newpop[j+1]=child2
            
            minx= min(min(child1.x,child2.x),minx)
            maxx = max(max(child1.x,child2.x),maxx)
        self.maxx= maxx
        self.minx=minx
        
    def objfunction(self,individual):
        pass
        
    def statistics(self,pop):
        """ Calculates the GA stats for the latest population """
        pop[0].fitness=self.objfunction(pop[0])
        self.max=pop[0].fitness
        self.min=pop[0].fitness
        self.sumfitness=pop[0].fitness
        self.sumx=pop[0].x
        
        # statistics
        for i in range(1,len(pop)): 
            p=pop[i]
            p.fitness=self.objfunction(p)
            self.sumfitness+=p.fitness
            self.max=max(self.max,p.fitness)
            self.min=min(self.min,p.fitness)
            self.sumx+=p.x
            
        self.avg=self.sumfitness/self.popsize
        self.avgx=self.sumx/self.popsize
        
            
    def report(self):
        if(self.verbose):
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
        print " Generation %d & Accumulation Statistics:\t max:%.3f\t min:%.3f\tsumfitness:%.15f\tavg:%.3f\tnmutation:%d\tncross:%d" % (self.gen, self.max, self.min, self.sumfitness,self.avg, self.nmutation, self.ncross)
        print " Generation %d & Accumulation Statistics:\t max:%.2f\t min:%.2f\tsumx:%.2f\tavg:%.2f\tnmutation:%d\tncross:%d" % (self.gen, self.maxx, self.minx, self.sumx,self.avgx, self.nmutation, self.ncross)
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
                
      
        