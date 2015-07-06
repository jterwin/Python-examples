
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from scipy import constants
from scipy.optimize import minimize_scalar
from scipy.integrate import cumtrapz


# set up some constants
h = constants.value('Planck constant')*1e-7
c = constants.value('speed of light in vacuum')*1e2
kb = constants.value('Boltzmann constant')*1e-7
sigma = constants.value('Stefan-Boltzmann constant')*1e-11
pi = np.pi


Tref = 140.
nu_max = 4000
#Tref = 5700.
#nu_max = 100000

# set up planck functions
def B_nu(nu, T=296.):
    return 2*h*c**2*nu**3/(np.exp((h*c/kb/T)*nu)-1)

def B_lam(lam, T=296.):
    return (2*h*c**2/lam**5)/(np.exp((h*c/kb/T)/lam)-1)

# remember cgs, so nu is cm^-1 and lambda is cm
#nu = np.logspace(np.log10(1.),np.log10(15000.), num=10000)
nu = np.linspace(1.,nu_max, num=int(nu_max))
lam_nu = 1./nu


# find max of planck functions
res_nu = minimize_scalar(lambda x: -B_nu(x,T=Tref), bounds=(10,10000), method='bounded')
#print(res_nu)
B_nu_max = -res_nu.fun
nu_max = res_nu.x

res_lam = minimize_scalar(lambda x: -B_lam(x,T=Tref), bounds=(1e-6,1e-2), method='bounded')
#print(res_lam)
B_lam_max = -res_lam.fun
lam_max = res_lam.x


# Calculate F_nu and F_lam, the normalized integral of B_nu and B_lam
F_nu = cumtrapz(B_nu(nu, T=Tref), nu, initial=0.0)
F_lam = cumtrapz(B_lam(lam_nu[::-1], T=Tref), lam_nu[::-1], initial=0.0)[::-1]  # do in reverse, starting at lambda=0
F_nu = F_nu*pi/(sigma*Tref**4)
F_lam = F_lam*pi/(sigma*Tref**4)


# Find nu_half and lam_half, where F_nu and F_lam are 0.5
n = np.searchsorted(F_nu, 0.5)
nu_half = nu[n-1]+(nu[n]-nu[n-1])**2*(0.5-F_nu[n-1])/(F_nu[n]-F_nu[n-1])
#print("")
#print(n, F_nu[n], F_nu[n-1])
#print(nu_half, nu[n-1], nu[n])

n = len(F_lam)-np.searchsorted(F_lam[::-1], 0.5)
lam_half = lam_nu[n-1]+(lam_nu[n]-lam_nu[n-1])**2*(0.5-F_lam[n-1])/(F_lam[n]-F_lam[n-1])
#print("")
#print(n, F_lam[n], F_lam[n-1])
#print(lam_half, lam_nu[n-1], lam_nu[n])


# the three nu
print("")
print("Max of B_nu, nu = %.1f, lam = %.2f" % (nu_max, 1e4/nu_max) )
print("Half of F_nu, nu = %.1f, lam = %.2f" % (nu_half, 1e4/nu_half) )
#print("Half of F_lam, nu = %.1f, lam = %.2f" % (1/lam_half, lam_half*1e4) )
print("Max of B_lam, nu = %.1f, lam = %.2f" % (1/lam_max, lam_max*1e4) )



# do some plotting


"""
fig, ax = plt.subplots()
ax.plot(nu, B_nu(nu, T=1500.))
ax2 = ax.twinx()
ax2.plot(nu, B_lam(lam_nu, T=1500.), 'g')
ax.set_xlabel(r'$\nu$ (cm$^{-1}$)')
"""

fig, ax = plt.subplots()
n = int(len(nu)/2)
ax.plot(nu[1:n], B_nu(nu[1:n], T=Tref)/B_nu_max, label=r'$B_\nu$/max($B_\nu$)')
ax.plot(nu[1:n], B_lam(lam_nu[1:n], T=Tref)/B_lam_max, 'g', label=r'$B_\lambda$/max($B_\lambda$)')

ax.plot(nu[1:n], F_nu[1:n], 'b--', label=r'$F_\nu$')
ax.plot(nu[1:n], F_lam[1:n], 'g--', label=r'$F_\lambda$')


# color lower axis blue
ax.set_xlabel(r'$\nu$ (cm$^{-1}$)', color='b')
for tl in ax.get_xticklabels():
    tl.set_color('b')

# make upper axis in microns, and color green
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
lam_ticks = [1.0,1.5,2.0,3.0,5.0,10.0]
ax2.set_xticks([1e4/lam for lam in lam_ticks])
ax2.set_xticklabels([str(lam) for lam in lam_ticks])
ax2.set_xlabel(r'$\lambda$ (micron)', color='g')
for tl in ax2.get_xticklabels():
    tl.set_color('g')


ax.set_ylim((0.,1.))
fig.suptitle('T = '+str(Tref), x=0.95, horizontalalignment='right')
ax.legend()


plt.tight_layout()

plt.show()
