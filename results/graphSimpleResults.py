#!/usr/bin/env python

import sys
from pylab import *

def main(args):
    x=[]
    y=[]
    files=[open("%s/objectiveFunctionReport.txt" % args[0]),
       open("%s/fitnessReport.txt" % args[0])]
    for f in files:
        x.append([])
        y.append([])
        i=len(x)-1
        for line in f:
            line=line.split(',')
            if line[0] != "gen":
                x[i].append(int(line[0]))
                y[i].append(float(line[1]))
            
    print y[1]
    print "*********"
    print y[0]

    subplot(2,1,1)
    plot(x[0],y[0],'bo')
    ylabel('x**2')
    title('Maximizing x**2 with SGA')

    subplot(2,1,2)
    plot(x[1],y[1],'go')
    xlabel('Generation')
    ylabel('Fitness')
    savefig("%s/simple_result.png" % args[0])

if __name__ == '__main__':
    args=sys.argv[1:]
    if len(args)!=1:
        print "Usage: %s <resultsDir>" % __file__
        sys.exit(-1)

    main(args)

