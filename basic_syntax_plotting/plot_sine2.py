""" plot_sine2 - the object oriented way to plot
this script will emphasis the object oriented way to plot in Python. While this
may seem like extra work, it is a safer way to program in Python (it doesn't
add everything to the namespace), and it will allow more control in future
examples. 
"""

from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,2*np.pi)
y = np.sin(x)


fig, ax = plt.subplots()
ax.plot(x,y)

ax.set_xlim((0,2*np.pi))

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Plot of $\sin(x)$')


plt.show()
