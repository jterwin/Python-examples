#Basic Syntax and Plotting

##Python scripts
To start we need to cover some basic good practices (that I learned through trial and error) that should be in every Python script that you make

####1. Do not use hashbang

To begin with, you shouldn't start your script with `#!/usr/bin/python` or similar. This is telling the computer which *interpreter* to use, in this case */usr/bin/python*. But this may be the incorrect version of python as you might have multiple versions of python installed, or when you move to a different machine python may move (for example if you move to the University's computers). Also this requires the script to have permission to run as an executable, which requires you to change the permissions with `chmod`. So instead, leave out this first line, and invoke your script with python from the command line:
```
python script.py &
```
So in this case, *python* will be the first instance of python in your *PATH* which can be set up and modified (on my Mac, I use Macports and *port select* to set which version of python I want to use, in my case `/opt/local/bin/python` that itself points to `/opt/local/bin/python2.7`; on University clusters this is commonly handled with *modules*). So this way your script are more easily adapted to different systems and even different versions of python.

After the script name I put a *&*, which means to run it in the background. I do this with plotting scripts so that I do not have to close the plot window to run another script. Otherwise I can not do anything at the command line until I close all the plots associated with that script.

####2. Import and Object Oriented Programming

Next let's talk about *Importing* modules and the *namespace*. Python is the languague, which is basically just the syntax and object types (ie numbers, arrays, lists, classes, etc.). So most of the great features are included in *modules* or *packages*. So person making a python server routine might use the `sys` and `urllib` modules, but we as scientist aren't too interesting in those ones. The most import module for us is `numpy`, which is then used my `scipy` and `matplotlib` and most (if not all) other scientific packages. Numpy main feature is the *ndarray* (or n-dimensional array) that is a very effiecient array (compared to python's built in array), and then there are a bunch of functions that work on this type of array in *numpy* and other packages (many of these efficient functions are written in *c*, and called through Python, so you get the speed of *c* with the readability of Python).

We gain access to the stuff in these packages by using the *import* statement. I would like to show the incorrect way of doing this first, because it is simpler, very similar to Matlab, and can be useful when you are just playing or testing your scripts. The incorrect way is to use the *wildcard*. If you look at **plot_sine.py** you will see
```
from numpy import *
from pylab import *

x = linspace(0,2*pi)
y = sin(x)
```
This type of import put everything in numpy in the current namespace, the namespace being the set of variables and functions you have current access to. So you can use the *sine* function by `y=sin(x)`. But this can be dangerous because it is not clear where the *sine* functions was declared, and you may have the case where you import two functions from two different packages with the same name, then you have no idea which one is being called. In fact, in the above example I did this. *pylab* is a convenient package that includes everythining from *numpy* and many plotting routines from *matplotlib*. So when I imported everything from *pylab*, I imported everything from *numpy* a second time.

This solution to this is import the package into the current namespace, and to access the elements of that package individually. So look at **plot_sine2.py** and you will see
```
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,2*np.pi)
y = np.sin(x)
```
So we import the package *numpy*, and use the convenient short name of *np*. And then it is clear that *linspace*, *pi*, and *sin* are elements of *numpy*. Like I said, this is a bit more typing (especially with the math functions like *sin* and *exp* and the like), but it is a lot safer in the end, and as you will see it will allow you a lot more control over what is happening in your scripts. There is a third type of import, where you import individual functions from a package, but I will introduce this later.


####3. A note on IPython and modules

IPython is an **interactive** interpreter for Python. This means that it is basically Python but has some additional interactive features that are very useful in learning python. One of the nicest features is tab suggestion (I forget the official name) which can show you all the contents of a package, or show you all the properties and functions available for a data type. Assuming you installed IPython, enter `ipython` at the command line. Now you can enter python commands to do simple things and test (you can do the same with python, but it lacks some of the nice features of IPython). Now import numpy:
```
import numpy as np
```
Now enter `np.` (np with a period) and press **TAB** a couple times. It will print out all the contents of numpy, include datatypes, function, and other stuff. Sometimes packages are composed of a heirarchical folder structure (SciPy is a good example), so you would have to enter that foldar and then **TAB** to see the contents of the folder (ex `import scipy as sp` and `sp.constants.` and **TAB**). This is a nice way to learn the contents of a package, to see whats available. But also we can look at a particular datatype, for example
```
x = np.linspace(0,10)
```
and now try `x.` and **TAB**. You will see all the properties and routines for an *ndarray*. So commonly I forget how to find the size and shape of an array, and this is a easy way to do it, as apposed to google, and keeps me learning.

####4. `__future__` package
Before we move on to plotting, notice the first import in **plot_sin2.py**
```
from __future__ import print_function, division
```
This is a line I include in every script now, and it keeps things forward and backward compatability. You may know that there are many versions of Python, in particular Python 2.x and Python 3.y. As Python evolved through Python 2.x, there was the condition that every old script should run with the current version, which required a lot of legacy compatability, which kept around a lot of old code and methods. This didn't allow for some major implementation changes that could improve Python. So with Python 3, they dropped the requirement for full backward compatability and could focus on cleaning up the language and improving the efficiency. For our purposes this isn't a major issue since most of the scientific packages work in both 2.x and 3.y, but I want to be sure that my scripts will run in Python 3.y in case I finally give up on 2.x (2.7 is the last Python 2 version that is in active developement, exclusively meant for backward compatbility, but this may not always be the case as 3.y has become mature and is becoming more efficient and widely used). So there is the **`__future__`** module to allow some compatability between the two.

So one change that impacts our scripts is the **print** statement. In Python 2.x it is
```
print "hello world"
```
and in Python 3.y
```
print("hello world")
```
So Python 3.y uses parentheses, and it is clear that it is a function. By importing **print_function** from the future package, we will only use the Python 3.y print statement, and our codes will work under both 2.x and 3.y. So it is a good idea to start including this in your scripts so they will be compatible in the future. There are many other


## Basic plotting

The script **plot_sine.py** show the simpler, Matlab-like way to plot. But it is unclear where the functions are coming from. The better, Object-Oriented, way is shown in **plot_sine2.py**. More explaination to come.
