#!/usr/bin/env python

import sys
sys.path.insert(0,'../src')
from pylab import *

def main(args):
     
    f=open("%s/paretofront.txt" % args[0])
    x=[[]]*6
    y=[[]]*6
    k=[[]]*6
    for line in f:
        line=line.split(':')
        x[0].append(line[1])
        y[0].append(line[2])
        k[0].append(line[0])
        if line[0] == '3':
            kassign= [int(i) for i in list(line[3]) if i.isdigit()]
            print "c:%s d:%s" %(line[1],line[2])
            print kassign
            i=0
            failed=0
            for ka in kassign:
                i+=1
                if ka==0 and i<= 50: pass
                elif ka==1 and i >50 and i<=100: pass
                elif ka==2 and i>100:pass
                else:failed+=1 
            print failed

    for i in range(1,1):
        f=open('controlFront%s.txt' % i)
        for line in f:
            line=line.split(':')
            x[i].append(line[1])
            y[i].append(line[2])
            k[i].append(line[0])


    plot(x[0],y[0],'bo')
    xlabel('Deviation')
    ylabel('Connectivity')
    title('Pareto Front for UCI Iris Dataset')
    #legend(('Solution Front', 'Control Front' ),'upper center', shadow=True)
    savefig("%s/paretofront.png" % args[0])

if __name__ == '__main__':
    args=sys.argv[1:]
    if len(args)!=1:
        print "Usage: %s <resultsDir>" % __file__
        sys.exit(-1)

    main(args)

