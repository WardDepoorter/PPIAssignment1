import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 


#Euler integration for 1D interior model of the moon 
from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import plot_csv_columns, add_to_df
#create empty dataframe to store results
results_df = pd.DataFrame()


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

G = const.G.to('m3 / (kg s2)').value
R_moon = 1737.4 * 1e3  # meters TODO: check value from literature
dr = 1 #m 
rho = 'ct'

#================ TRY1: ct density = 3340 kg/m3 ==================
if rho == 'ct':
    # integrate constant density model to find mass profile
    r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
    #Calculate gravity profile from mass profile:
    
    g_r_array = -G * M_r_array / r_array**2
    g_r_array[0] = 0  # avoid division by zero at center
    #add respective columns in df:
    results_df = add_to_df(r_array, 'Radius (m)', results_df)
    results_df = add_to_df(M_r_array, 'Mass (kg)', results_df)
    results_df = add_to_df(g_r_array, 'Gravity (m/s^2)', results_df)
    
    #print(M_r_array[-1])  # Total mass of the moon
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

results_df.to_csv('code/integration_output.csv')






