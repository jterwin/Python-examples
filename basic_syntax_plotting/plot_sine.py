""" plot_sine.py
this is a basic example of plotting. It uses the incorrect type of import
(ie from .. import *, or wildcards). But it will useful to compare this to
the 'correct' way in the next example. To run this code (assuming you have
your python environment set up correctly), enter from the command line:
>> python plot_sine.py &
"""

from numpy import *
from pylab import *



x = linspace(0,2*pi)
y = sin(x)

figure()
plot(x,y)

xlabel('x')
ylabel('y')
title('Plot of $\sin(x)$')


show()
