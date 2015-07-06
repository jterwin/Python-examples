
from __future__ import print_function, division
from numpy import *
import matplotlib.pyplot as plt





def pdf_normal(r, r0, sigma):
    n = 1/(sigma*sqrt(2.*pi))*exp(-(r-r0)**2/(2.*sigma**2))
    return n

def cdf_normal(r, r0, sigma):
    from scipy.special import erf
    cdf = 0.5*(1. + erf((r-r0)/sigma/sqrt(2.)))
    return cdf
               

def pdf_lognormal(r,r0,sigma):
    n = where(r>0, 1/(sigma*sqrt(2.*pi)*r)*exp(-log(r/r0)**2/(2.*sigma**2)), 0)
    return n

def cdf_lognormal(r, r0, sigma):
    from scipy.special import erf
    cdf = where(r>0, 0.5*(1. + erf(log(r/r0)/sigma/sqrt(2.))), 0)
    return cdf

r = linspace(0.001,2)
r0 = 0.6
sigma = 0.1



n1 = pdf_normal(r,r0,sigma)
n2 = pdf_lognormal(r,r0,sigma)


fig,ax = plt.subplots()
ax.plot(r,n1,label='normal')
ax.plot(r,n2,label='log-normal')



leftedges = linspace(0,2,20,endpoint=False)
dr = leftedges[1]-leftedges[0]
rightedges = leftedges + dr
midpoints = leftedges+0.5*dr


print(leftedges)
pdf1 = pdf_normal(midpoints,r0,sigma)
cdf1 = cdf_normal(rightedges,r0,sigma)-cdf_normal(leftedges,r0,sigma)

fig, ax = plt.subplots()
ax.bar(leftedges,cdf1,width=dr)
ax.plot(midpoints,pdf1*dr,'--')
ax.set_title('normal distribution')
print(sum(pdf1)*dr, sum(cdf1))



pdf2 = pdf_lognormal(midpoints,r0,sigma)
cdf2 = cdf_lognormal(rightedges,r0,sigma)-cdf_lognormal(leftedges,r0,sigma)

fig, ax = plt.subplots()
ax.bar(leftedges,cdf2,width=dr)
ax.plot(midpoints,pdf2*dr,'--')
ax.set_title('log-normal distribution')
print(sum(pdf2)*dr, sum(cdf2))


plt.show()
