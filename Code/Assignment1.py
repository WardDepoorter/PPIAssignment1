import numpy as np
import matplotlib.pyplot as plt
import astropy 
import pandas as pd 
#Euler integration for 1D interior model of the moon 
from Euler_intergrators import euler_upward, euler_downward 



# density function,
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



# ================== TRY2: density layers =======================

if rho =='layers':
    None







#print(r_array)  # Radius array
# # put data in dataframe 
# data = pd.DataFrame({'Radius_m': r_array, 'Mass_kg': M_r_array})
# data.to_csv('moon_mass_profile.csv')

