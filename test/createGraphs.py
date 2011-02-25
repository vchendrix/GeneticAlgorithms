from pylab import *


f=open('paretofront.txt')
x=[[]]*6
y=[[]]*6
k=[[]]*6
for line in f:
    line=line.split(':')
    x[0].append(line[1])
    y[0].append(line[2])
    k[0].append(line[0])

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
legend(('Solution Front', 'Control Front' ),'upper center', shadow=True)
show()


