import numpy as np
import matplotlib.pyplot as plt
import astropy 
import pandas as pd 
#Euler integration for 1D constant density model of the moon 
#General euler integration function


def euler_upward(y0, h , x_max, dydx):
    """
    Upward Euler method for solving ODEs:
    y_i = y_i-1 + h * y'(x_i-1) 
    
    Parameters:
    y0 : float
        Initial value of the dependent variable.
    h : float
        Step size.
    x_max : float
        max value of the domain.
    dxdy : callable
        Function that computes the derivative at x_i-1.
    """
    #set initial conditions, starting at r=0 (center of body)
    # eg in case of moon mass integration, y = M, h = dr, x_max = R_moon, derivs = dMdr
    #initialize arrays to store results

    x_values = np.arange(0, x_max, h)
    y_values = np.zeros(len(x_values))
    y_values[0] = y0


    #perform Euler integration
    for i in range(1, len(x_values)):
        dydx_val = dydx(x_values[i-1])
        y_values[i] = y_values[i-1] + dydx_val * h
    return x_values, y_values


# density function, can be as funtion of r TODO: replace with realistic density profile
def rho_(r):
    if rho == 'ct':
        return 3340.0  # kg/m^3, example value
    if rho == 'layers':
        #add desired density profile here
        return None

def dM_dr(r):
    return 4.0 * np.pi * r**2 * rho_(r)




# dM = 4pi r^2 rho(r) dr
# g(r) = -G M(r) / r^2 
# dp = -rho(r) g(r) dr  
#upward euler method; y_n+1 = y_n + (df/dr)(t_n, y_n) 


R_moon = 1737.4 * 1e3  # meters TODO: check value from literature
dr = 1 #m 
rho = 'layers'

#================ TRY1: ct density = 3340 kg/m3 ==================
if rho == 'ct':
      # constant density model
    r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
    print(M_r_array[-1])  # Total mass of the moon
    print('The numerically computed solution, assuming constant density is:', M_r_array[-1], 'kg')

    #compare with analytical solution: 
    M_analytical = (4/3) * np.pi * R_moon**3 * rho_(0)
    print('The analytical solution,assuming constant density, is:', M_analytical, "kg")  # Analytical mass of the moon

    #find numerical error:
    error = abs(M_analytical - M_r_array[-1])
    print('The error is:', error, 'kg')



# ================== TRY2: density layers ============

if rho =='layers':
    None







#print(r_array)  # Radius array
# # put data in dataframe 
# data = pd.DataFrame({'Radius_m': r_array, 'Mass_kg': M_r_array})
# data.to_csv('moon_mass_profile.csv')

