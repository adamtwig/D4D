from numpy import corrcoef, sum, log, arange
from numpy.random import rand
from pylab import pcolor, show, colorbar, xticks, yticks

# generating some uncorrelated data
data = rand(10,100) # each row of represents a variable

# creating correlation between the variables
# variable 2 is correlated with all the other variables
data[2,:] = sum(data,0)
# variable 4 is correlated with variable 8
data[4,:] = log(data[8,:])*0.5

# plotting the correlation matrix
R = corrcoef(data)
pcolor(R)
colorbar()
yticks(arange(0.5,10.5),range(0,10))
xticks(arange(0.5,10.5),range(0,10))
show()
