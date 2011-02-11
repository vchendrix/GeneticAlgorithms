import matplotlib.pyplot as plt

"""
    Plot the representation of the niches


"""
x=[]
y=[]
for item in niches:
    key=item[0]
    value=item[1]
    x.append(key)
    y.append(value)

plt.plot(x,y,'ro')
plt.axis([0,50,0,7000])
plt.xlabel('Connectivity')
plt.ylabel('Deviation')

