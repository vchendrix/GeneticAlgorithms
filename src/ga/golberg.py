"""
Created on Jan 6, 2011

Programs based on the Pascal programs (Simple3, Simple4,SGA) in
Goldberg, David. (1989). Genetic Algorithms in Search, 
Optimization and Machine Learning. Appendix B,C

@author: val
"""

__version__ = '0.1'
__author__ = "Val Hendrix (val.hendrix@me.com)"
__date__ = 'Jan 7, 2011'
__url__ = 'https://github.com/valreee/GeneticAlgorithms'
__copyright__ = "(C) 2011 Val Hendrix."

import array
import ga
from utilities import Random

ncoins = 1000   # number of coin flips
prob = .5     # probability of heads turning up

def randomNumberCounter():
    ranges = ['0.00-25','0.25-0.50','0.50-0.75','0.75-1.00']
    randomNumbers = array.array('l',range(4))
    rand=Random()
    rand.randomize()
    for i in range(1000):
        r=rand.random()
        if r < 0.25:
            randomNumbers[0]+=1
        elif r < 0.5:
            randomNumbers[1]+=1
        elif r < 0.75:
            randomNumbers[2]+=1
        elif r < 1.0:
            randomNumbers[3]+=1
            
    for i in range(4):
        print "Range %s count: %d\n" % (ranges[i],randomNumbers[i])
        


def coinToss():
    headOrTails = array.array('l', [0, 0]) # head or tails count
    rand = Random()
    rand.randomize()    # Seed and warm up random number generator
    for i in range(ncoins):
        toss = rand.flip(prob)
        if toss:
            headOrTails[0] += 1
        else:
            headOrTails[1] += 1
    print "In %d coin tosses there were %d heads and %d tails." % (ncoins, headOrTails[0], headOrTails[1])
    

def simpleGeneticAlgorithm():
    """
        This is the simple genetic algorithm as seen in 
        Goldberg,David. (1989). Genetic Algoritms in Search, Optimization and 
        Machine Learning. Appendix C.
    """
    from simple import SimpleGeneticAlgorithm
    
    popsize, lchrom, maxgen, pcross, pmutation, rand = ga.common.initData()
    sga = SimpleGeneticAlgorithm(rand,popsize, lchrom, maxgen, pcross, pmutation);
    ga.common.initReport(sga)
    sga.run()
    
def tspGeneticAlgorithm():
    from tsp import  TSPGeneticAlgorithm
    
    popsize, lchrom, maxgen, pcross, pmutation, rand = ga.common.initData()
    graph = [
             [0, 1, 10, 2, 17, 13, 19, 11, 6, 5, 17, 1, 12, 7, 10],
             [1, 0, 12, 9,  4, 2, 7, 19, 12, 4, 14, 3, 17, 18, 16],
             [10,12, 0, 4, 18, 20, 1, 4, 16, 13, 20, 2, 6, 15, 18],
             [2, 9, 4, 0, 5, 3, 11, 14, 19, 1, 11, 7, 16, 5, 2],
             [17, 4, 18, 5, 0, 11, 5, 8, 2, 6, 15, 12, 8, 8, 17],
             [13, 2, 20, 3, 11, 0, 18, 6, 4, 3, 15, 7, 10, 16, 9],
             [19, 7, 1, 11, 5, 18, 0, 20, 9, 10, 5, 13, 3, 18, 19],
             [11, 19, 4, 14, 8, 6, 20, 0, 12, 7, 20, 2, 6, 3, 9],
             [6, 12, 16, 19, 2, 4, 9, 12, 0, 11, 8, 13, 16, 15, 3],
             [5, 4, 13, 1, 6, 3, 10, 7, 11, 0,14, 14, 10, 20, 19],
             [17, 14, 20, 11, 15, 15, 5, 20, 8, 14, 0, 14, 15, 8, 1],
             [1, 3, 2, 7, 12, 7, 13, 2, 13, 14, 14, 0, 1, 13, 4],
             [12, 17, 6, 16, 8, 10, 3, 6, 16, 10, 15, 1, 0, 9, 17],
             [7, 18, 15, 5, 8, 16, 18, 3, 15, 20, 8, 13, 9, 0, 1],
             [10, 16, 18, 2, 17, 9, 19, 9, 3, 19, 1, 4, 17, 1, 0]
             ]
    tspga = TSPGeneticAlgorithm(rand, graph, popsize, maxgen, pcross, pmutation);
    ga.common.initReport(tspga)
    tspga.run(silent=False)

if __name__ == '__main__':
    while True:
        x=raw_input("Choose [C]oin Toss, [R]andom number [S]imple GA [T]SP: ")
        if x == "C":
            coinToss()
        elif x == 'R':
            randomNumberCounter()
        elif x == 'S':
            simpleGeneticAlgorithm()
        elif x == 'T':
            tspGeneticAlgorithm()
        else:
            break
