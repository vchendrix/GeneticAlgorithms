"""
Created on Jan 6, 2011

Programs based on the Pascal programs (Simple3, Simple4,SGA) in
Goldberg, David. (1989). Genetic Algorithms in Search, 
Optimization and Machine Learning. Appendix B,C

@author: val
"""

import array
from random import Random

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
    import simple
    from simple import SimpleGeneticAlgorithm
    
    popsize, lchrom, maxgen, pcross, pmutation, rand = simple.initData()
    sga = SimpleGeneticAlgorithm(rand,popsize, lchrom, maxgen, pcross, pmutation);
    simple.initReport(sga)
    sga.run()
    

if __name__ == '__main__':
    while True:
        x=raw_input("Choose [C]oin Toss, [R]andom number [S]imple GA: ")
        if x == "C":
            coinToss()
        elif x == 'R':
            randomNumberCounter()
        elif x == 'S':
            simpleGeneticAlgorithm()
        else:
            break
