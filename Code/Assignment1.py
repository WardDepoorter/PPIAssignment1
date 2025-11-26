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
# options: constant density: 'ct' or layered density: 'ct_layers_vpremoon' or  ADD other model, 'full_vpremoon',  
def rho_(r):
    if rho == 'ct':
        return 3345.56  # kg/m^3, from garcia 2019 +- 0.4 kg /m^3
    if rho == 'ct_layers_vpremoon':
        if r < 380e3:
            return 5171
        if 380e3 <= r < 1709e3:
            return 3308
        if 1709e3 <= r < 1736e3:
            return 2762
        if r >= 1736e3:
            return 2600

#mass gradient function
def dM_dr(r):
    return 4.0 * np.pi * r**2 * rho_(r)

# pressure gradient function
def dp_dr(r):
    return rho_(r) * g_r_array[np.searchsorted(r_array, r)]  #calculate dpdr at radius r, by taking the values of rho and g at given r.




# dM = 4pi r^2 rho(r) dr
# g(r) = -G M(r) / r^2 
# dp = -rho(r) g(r) dr  
#upward euler method; y_n+1 = y_n + (df/dr)(t_n, y_n) 

G = const.G.to('m3 / (kg s2)').value
R_moon = 1737.4 * 1e3  # meters TODO: check value from literature
dr = 1000 #m 


rho = 'ct_layers_vpremoon' # choose density model: 'ct' for constant density, 'layers' for ct layered approach M1 and M2 for variable density

#=========================================== M1: ct average density = 3345.56 kg/m3 ==========================================
if rho == 'ct':
    # integrate constant density model to find mass profile
    r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
    #Calculate gravity profile from mass profile:
    
    g_r_array = -G * M_r_array / r_array**2
    g_r_array[0] = 0  # avoid division by zero at center
    print (len(g_r_array))
    
    r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
    print (len(p_r_array))
    #add respective columns in df:
    results_df = add_to_df(r_array, 'Radius (m)', results_df)
    results_df = add_to_df(M_r_array, 'Mass (kg)', results_df)
    results_df = add_to_df(g_r_array, 'Gravity (m/s^2)', results_df)
    results_df = add_to_df(p_r_array/(1e9), 'Pressure (GPa)', results_df) 
    results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density (kg/m^3)', results_df)
    #print(M_r_array[-1])  # Total mass of the moon
    print('The numerically computed solution, assuming constant density is:', M_r_array[-1], 'kg')

    #compare with analytical solution: 
    M_analytical = (4/3) * np.pi * R_moon**3 * 3345.56
    print('The analytical solution,assuming constant density layers , is:', M_analytical, "kg")  # Analytical mass of the moon

    #find numerical error:
    error = abs(M_analytical - M_r_array[-1])
    print('The error is:', error, 'kg') 



#=========================================== M1: ct density layers ==========================================

if rho =='ct_layers_vpremoon':
    # integrate constant density model to find mass profile
    r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
    #Calculate gravity profile from mass profile:
    
    g_r_array = -G * M_r_array / r_array**2
    g_r_array[0] = 0  # avoid division by zero at center
    print (len(g_r_array))
    
    r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
    print (len(p_r_array))
    #add respective columns in df:
    results_df = add_to_df(r_array, 'Radius (m)', results_df)
    results_df = add_to_df(M_r_array, 'Mass (kg)', results_df)
    results_df = add_to_df(g_r_array, 'Gravity (m/s^2)', results_df)
    results_df = add_to_df(p_r_array/(1e9), 'Pressure (GPa)', results_df)
    results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density (kg/m^3)', results_df)

    #print(M_r_array[-1])  # Total mass of the moon
    print('The numerically computed solution, assuming constant density layers, is:', M_r_array[-1], 'kg')

    #compare with analytical solution: 
    #TODO: compute analytical solution for layered density
    #find numerical error:
    #error = abs(M_analytical - M_r_array[-1])
    #print('The error is:', error, 'kg') 






#store results in csv
results_df.to_csv('code/integration_output.csv')






