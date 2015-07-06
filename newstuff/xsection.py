#!/opt/local/bin/python

from pylab import *
from scipy.special import gamma
from numpy import polyfit


kb = 1.38065e-23
m = 28.*1.66054e-27
Na = 6.0221415e23


def sigma(k0,w,T):
    return  (15.*15.*sqrt(pi*kb*m)*kb)/(32*(3.5-w)*(2.5-w)*m*k0*T**(w-.5))

temp = linspace(40,140,200)



T = temp
p = 1.0e-6
rho = p/(1e3*Na*kb*100.)  # ??


Tc = 126.192          # K
rhoc = 11.1839        # mol/dm^3
pc = 3.3958           # Mpa
M = 28.03148          # g per mol
siglj = 0.3656        # K
epsklj = 98.94        # nm
xi0 = 0.17            # nm
Gamma = 0.055         # []
qD = 0.40             # 0.40
Tref = 252.384        # K 

tau = Tc/T
delta = (rho/rhoc)
Tstar = T/epsklj


bi = array([0.431,-.4623,0.08406,0.005341,-.00331])
omega = bi[0]*ones_like(Tstar)
omega = omega + bi[1]*log(Tstar) + bi[2]*log(Tstar)**2 + bi[3]*log(Tstar)**3 + bi[4]*log(Tstar)**4
omega = exp(omega)

eta0 = 0.0266958*sqrt(M*T)/siglj**2/omega


N3i = array([0,10.72,0.03989,0.001208,-7.402,4.62])
t3i = array([0,0.1,0.25,3.2,0.9,0.3])
d3i = array([0,2,10,12,2,1])
l3i = array([0,0,1,1,2,3])
g3i = array([0,0,1,1,1,1])

etar = zeros_like(T)
for i in range(1,6):
    etar = etar + N3i[i]*tau**t3i[i]*delta**d3i[i]*exp(-g3i[i]*delta**l3i[i])


eta = (eta0+etar)*1e-6
                                            
sigma_lemmon = 0.998*sqrt(kb*m*temp/pi)/eta

#print 0.998*sqrt(kb*m*100/pi)/6.9e-6

N4i = array([0,1.511,2.117,-3.332,8.862,31.11,-73.13,20.03,-0.7096,0.2672])
t4i = array([0,0,-1.0,-0.7,0.0,0.03,0.2,0.8,0.6,1.9])
d4i = array([0,0,0,0,1,2,3,4,8,10])
l4i = array([0,0,0,0,0,0,1,2,2,2])
g4i = array([0,0,0,0,0,0,1,1,1,1])

lam0 = N4i[1]*eta0+N4i[2]*tau**t4i[2]+N4i[3]*tau**t4i[3]

lamr = zeros_like(T)
for i in range(4,10):
    lamr = lamr + N4i[i]*tau**t4i[i]*delta**d4i[i]*exp(-g4i[i]*delta**l4i[i])


chi = pc*p/pc**2*(m/kb/T)**2
chiref = pc*p/pc**2*(m/kb/Tref)**2
xi = xi0*((chi-chiref*Tref/T)/Gamma)**(0.63/1.2415)
omegatilde = 2./pi*(2./7.*arctan(xi/qD) + 5./7.*(xi/qD))
omegatilde0 = 2./pi*(1.0-exp(-1.0/(qD/xi+((xi/qD)*(rhoc/rho))**2/3.))) 
lamc = rho*3.5*kb*kb*1.01*T/(6*pi*xi*eta)*(omegatilde-omegatilde0)

lam = (lam0+lamr)*1e-3
lamn = (lam0+lamr+lamc)*1e-3

p = polyfit(log(T),log(lamn),1)
print( "" )
print( "kappa0 = " + repr(exp(p[1])) )
print( "s = " + repr(p[0]) )
print( "sigma(100) = " + repr(sigma(exp(p[1]),p[0],100.)) )
print( (75./64.*(pi*m*kb*temp[10])**0.5*(kb/m))/(lamn[10]) )
print( sigma(lamn[10],0.0,temp[10]) )
print( "" )

print( "using 5.63e-5*T*1.12" )
print( "sigma(60) = " + repr(sigma(5.63e-5, 1.12, 60)) )
print( "sigma(70) = " + repr(sigma(5.63e-5, 1.12, 70)) )
print( "sigma(80) = " + repr(sigma(5.63e-5, 1.12, 80)) )
print( "sigma(90) = " + repr(sigma(5.63e-5, 1.12, 90)) )


sigma_bird = pi*(4.17e-10)**2*(273./temp)**(2.*0.74-1.)



figure(1)
plot(temp, sigma(9.37e-5, 1., temp)/1e-19  , 'b',label='Stevens (1992)')
plot(temp, sigma(5.63e-5, 1.12, temp)/1e-19, 'g',label = 'Hubbard et al. (1990)')
plot(temp, pi*(4.17e-10)**2*ones_like(temp)/1e-19, 'r--', label="Bird (1994), HS-273K")
plot(temp, sigma_bird/1e-19, 'r', label="Bird (1994), VHS")
plot(temp, 1.5*sigma_lemmon/1e-19, 'c', label = "Lemmon 2004") #, via viscocity")
#plot(temp, sigma(lamn,0.0,temp)/1e-19, 'c--', label = "Lemmon 2004, via conductivity")
#plot(temp, sigma(exp(p[1]),p[0],temp)/1e-19, 'k--', label = "Lemmon 2004, via conductivity")
#plot(temp, (75./64.*(pi*m*kb*temp)**0.5*(kb/m))/(lamn)/1e-19, 'k--', label = "Lemmon 2004, via conductivity")

ylabel('$\sigma$ ($10^-19$ m$^2$)')
xlabel('T (K)')
legend()


#write out data for darrel
savetxt('crosssection.txt',
        column_stack( (temp, 1.5*sigma_lemmon,
                       sigma(exp(p[1]),p[0],temp), (75./64.*(pi*m*kb*temp)**0.5*(kb/m))/(lamn)) ),
    fmt=('%5.2f','%15.5e','%15.5e', '%15.5e'))

savetxt('t_mu_kappa.txt', column_stack((temp,eta,lamn)) ,fmt=('%5.2f','%15.5e','%15.5e') )


figure(2)
plot(temp, 9.37e-5*temp, 'b', label='Stevens et al. (1992)')
plot(temp, 5.63e-5*temp**1.12, 'g', label='Hubbard et al. (1990)')
plot(temp, sigma( pi*(4.17e-10)**2, 0.74, 273)*temp**0.74,'r',label='Bird (1994), VHS')
plot(temp, lam, 'c', label='Lemmon et al. (2004)')
#plot(temp, exp(p[1])*temp**p[0], 'c', label='Lemmon 2004')
#plot(temp, lamn, 'k--', label='Lemmon 2004')

ylabel('$\kappa$ (W per m per K)')
xlabel('T (K)')
legend(loc='upper left')



#figure(3)
#plot(temp, (sigma(exp(p[1]),p[0],temp)/1e-19)/((75./64.*(pi*m*kb*temp)**0.5*(kb/m))/(lam)/1e-19), 'k--')
#plot(temp, (sigma(exp(p[1]),p[0],temp)/1e-19)/(sigma(lamn,0.0,temp)/1e-19), 'k--')
#plot(temp, (75./64.*(pi*m*kb*temp)**0.5*(kb/m))/(lam)/1e-19/(sigma(lamn,0.0,temp)/1e-19), 'k--')


#figure(4)
#plot(temp,15./4.*(kb/m)*eta/lamn)

show()


