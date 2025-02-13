# The idea is to obtain the error of our numeric solution at any time
# using the Richardson's extrapolation: 
#
#           E(t_n) = ( U1_n - U2_n ) / ( 1 - 2^(-q) ),              [1]
#
# where U1 is the solution for dt (coarse mesh) and U2 is the one 
# obtained for dt/2 (fine mesh). 
# 
# Every temporal scheme has an order "q" (DATA). 
# The convergence rate, AKA how great a temporal scheme is, is
# determined by:  
#
#               log( |E(_tn)| ) = C - q·log(N),                     [2]
#
# Notice that, as we can see from [1], the position occupied by the dt/2 
# grid is twice the positivon of the dt grid. 
# 
# Example: ---------------------------------------------------------------
# 
#  t1 = [0    1    2    3    4 ]
#  t2 = [0   1/2   1   3/2   2   5/2   4   7/2   8] 
#
#   -> t = 1s: t1[1] or t2[2]
#   -> t = 2s: t1[2] or t2[4]
#   -> t = 3s: t1[3] or t2[6]


###########################################################
#                       LIBRARIES                         #
########################################################### 
from numpy import array, zeros, linspace, log10
import matplotlib.pyplot as plt
from ODES.Temporal_schemes import Euler, RK2, RK4, AB2, Inv_Euler, CN
from Cauchy_Error.Richardson import Cauchy_Error
from Cauchy_Error.Convergence import Conv
from Physics.Kepler import Kepler
from Physics.Linear_Oscilator import Lin_Osc


###########################################################
#                         DATA                            #
###########################################################
# Select the problem you want to solve
problem = Lin_Osc

# Select the temporal scheme with wHich you want to calculate
# the numerical solution
scheme1 = Euler
scheme2 = Inv_Euler
scheme3 = CN
scheme4 = RK4

# Select the initial conditions
if problem == Lin_Osc: 
    # Linear Oscillator
    x0  = 1
    vx0 = 0
    U0 = array( [x0,vx0] )
elif problem == Kepler: 
    # Kepler's orbit
    x0  = 1
    y0  = 0
    vx0 = 0
    vy0 = 1
    U0 = array( [x0,y0,vx0,vy0] )

# Initial and final instants
t0 = 0
tf = 10

# Number of intervals for the coarse  mesh
N = 1000 # give a larger value for Inverse Euler scheme ( dt < 0.033 )

# DATA FOR CONVERGENCE RATIO
ptsgraf = 7 # Number of points to be plotted. IMPORTANT: Higher than 8 begins the V-form of the convergence ratio plot
Nf = 15000  # Maximum N-value to be plotted in convergence ratio figure

###########################################################
#  CODE FOR CAUCHY ERROR WITH RICHARDSON'S EXTRAPOLATION  #
###########################################################

# Initialize the temporal instants vectors
t  = zeros(N+1)
t  = linspace(t0,tf,N+1)
dt = (t[-1]-t[0])/N

# Compute the error with Richardson's extrapolation
error1 = Cauchy_Error(problem, scheme1, U0, t)
error2 = Cauchy_Error(problem, scheme2, U0, t)
error3 = Cauchy_Error(problem, scheme3, U0, t)
error4 = Cauchy_Error(problem, scheme4, U0, t)

###########################################################
#       CODE FOR CONVERGENCE OF TEMPORAL SCHEMES          #
###########################################################

# Obtain the vector of values to be represented in each axis of the convergence ratio plot
print("------------ SCHEME 1 ---------------")
logN1, logE1 = Conv(problem, scheme1, U0, t, ptsgraf, Nf)
q1 = - round( ( logE1[-1,0]-logE1[0,0] ) / (logN1[-1]-logN1[0]) , 2 )
print("------------ SCHEME 2 ---------------")
logN2, logE2 = Conv(problem, scheme2, U0, t, ptsgraf, Nf)
q2 = - round( ( logE2[-1,0]-logE2[0,0] ) / (logN2[-1]-logN2[0]) , 2 )
print("------------ SCHEME 3 ---------------")
logN3, logE3 = Conv(problem, scheme3, U0, t, ptsgraf, Nf)
q3 = - round( ( logE3[-1,0]-logE3[0,0] ) / (logN3[-1]-logN3[0]) , 2 )
print("------------ SCHEME 4 ---------------")
logN4, logE4 = Conv(problem, scheme4, U0, t, ptsgraf, Nf)
q4 = - round( ( logE4[-1,0]-logE4[0,0] ) / (logN4[-1]-logN4[0]) , 2 )

###########################################################
#                          PLOTS                          #
###########################################################
# Plots the solution with "scheme1" temporal scheme
# plt.figure(figsize=(13, 7))
# plt.axis("equal")

# plt.plot( U1[:,0], U1[:,1] , '-b' , lw = 1.0)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title( r'{} problem solved with {} scheme (coarse mesh with $\Delta$t={})'.format( problem.__name__, scheme1.__name__, round(dt, 2) ) )
# plt.grid()
# plt.show()

# Plots the error for componets 0 and 1 of the of the solution vector for 
# the "scheme1" temporal scheme.
plt.figure(figsize=(13, 7))

plt.plot( t[:], error1[:,0] , '-b' , lw = 1.0, label ="Comp. 1 of state vector" )
plt.plot( t[:], error1[:,1] , '-r' , lw = 1.0, label ="Comp. 2 of state vector" )
plt.xlabel('t')
plt.ylabel('Error')
plt.legend()
plt.title( r'Error of {} problem solved with {} scheme (coarse mesh with $\Delta$t={})'.format( problem.__name__, scheme1.__name__, round(dt, 5) ) )
plt.grid()
plt.show()

# Compares the component 0 of the solution vector given by different temporal schemes
plt.figure(figsize=(13, 7))

plt.plot( t[:], error1[:,0] , '-b' , lw = 1.0, label =r"{}".format(scheme1.__name__) )
plt.plot( t[:], error2[:,0] , '-r' , lw = 1.0, label =r"{}".format(scheme2.__name__) )
plt.plot( t[:], error3[:,0] , '-g' , lw = 1.0, label =r"{}".format(scheme3.__name__) )
plt.plot( t[:], error4[:,0] , '-m' , lw = 1.0, label =r"{}".format(scheme4.__name__) )
plt.xlabel('t')
plt.ylabel('Error')
plt.legend()
plt.title( r'Error in x component of {} problem (coarse mesh with $\Delta$t={})'.format( problem.__name__, round(dt, 2) ) )
plt.grid()
plt.show()


# Plots the convergence for every temporal scheme 
plt.figure(figsize=(13, 7))
# plt.axis("equal")

plt.plot( logN1[:], logE1[:,0] , '-b'  , lw = 1.0, label = r"{} (q={})".format(scheme1.__name__, q1) )
plt.plot( logN2[:], logE2[:,0] , '-r'  , lw = 1.0, label = r"{} (q={})".format(scheme2.__name__, q2) )
plt.plot( logN3[:], logE3[:,0] , '--m' , lw = 1.0, label = r'{} (q={})'.format(scheme3.__name__, q3) )
plt.plot( logN4[:], logE4[:,0] , '--c' , lw = 1.0, label = r'{} (q={})'.format(scheme4.__name__, q4) )

plt.xlabel(r'$log_{10}(N)$')
plt.ylabel(r'$log_{10}(U_2 - U_1)$')
plt.legend(loc='lower left')
plt.title( r'Convergence ratio of different temporal schemes for {} problem'.format( problem.__name__) )
plt.grid()
plt.show()