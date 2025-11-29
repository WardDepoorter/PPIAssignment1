import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 

from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import plot, add_to_df
from Densitymodels import M1, W11, vpremoon, ct

#================================================== constants =====================================================
G = const.G.to('m3 / (kg s2)').value # m^3 / (kg s^2)
R_moon = 1737.4 * 1e3  # me
dr = 1 #m 

#create empty dataframe to store results
results_df = pd.DataFrame()


# density function,
# options: constant density: 'ct' or layered density: 'ct_layers_vpremoon' or  ADD other model, 'full_vpremoon',  
def rho_(r):
    if model == ct:
        return ct[0]['rho']
    if model == M1:
        for layer in M1:
            if layer['r_in'] <= r < layer['r_out']:
                return layer['rho']
    if model == W11:
        for layer in W11:
            if layer['r_in'] <= r < layer['r_out']:
                return layer['rho']
    if model == vpremoon:
        for layer in vpremoon:
            if layer['r_in'] <= r < layer['r_out']:
                return layer['rho']

#mass gradient function
def dM_dr(r):
    return 4.0 * np.pi * r**2 * rho_(r)

# pressure gradient function
def dp_dr(r):
    return rho_(r) * g_r_array[np.searchsorted(r_array, r)] 

 
def integrate(model, h, output_df):
        
        '''
        This function integrates the mass and pressure profiles of the moon given a density model.
        Params:
        model: list of dictionaries, 1 for each density layer, containing  'r_out', 'r_in', 'rho'
        h = float , step size for euler integration
        output_df:  dataframe to store results
        '''
        global g_r_array, r_array
        r_max = model[-1]['r_out']
        r_array = np.arange(0, r_max, h)

        rho_array = np.array([rho_(r) for r in r_array])

        r_array, M_r_array = euler_upward(0, h, r_max, dM_dr)
        
        g_r_array = -G * M_r_array / r_array**2
        g_r_array[0] = 0  
        
        r_array, p_r_array = euler_downward(0, h, r_max, dp_dr)
        
        output_df = add_to_df(r_array, 'Radius', output_df)
        output_df = add_to_df(g_r_array, 'Gravity', output_df)
        output_df = add_to_df(p_r_array/(1e9), 'Pressure', output_df)
        output_df = add_to_df(M_r_array, 'Mass', output_df)
        output_df = add_to_df(rho_array, 'Density', output_df)

        return output_df
    

model = ct
results_df = integrate(model, 1, results_df)
results_df.to_csv('Code/output/integration_output.csv', index=False)


# #=========================================== M1: ct average density = 3345.56 kg/m3 ==========================================
# if model == 'ct':
#     # integrate constant density model to find mass profile
#     r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
#     #Calculate gravity profile from mass profile:
    
#     g_r_array = -G * M_r_array / r_array**2
#     g_r_array[0] = 0  # avoid division by zero at center
#     print (len(g_r_array))
    
#     r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
#     print (len(p_r_array))
#     #add respective columns in df:
#     results_df = add_to_df(r_array, 'Radius', results_df)
#     results_df = add_to_df(M_r_array, 'Mass', results_df)
#     results_df = add_to_df(g_r_array, 'Gravity', results_df)
#     results_df = add_to_df(p_r_array/(1e9), 'Pressure', results_df) 
#     results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density', results_df)
#     results_df.to_csv('Code/output/integration_output.csv')

#     #print(M_r_array[-1])  # Total mass of the moon
#     print('The numerically computed solution, assuming constant density is:', M_r_array[-1], 'kg')

#     #compare with analytical solution: 
#     M_analytical = (4/3) * np.pi * R_moon**3 * 3345.56
#     print('The analytical solution,assuming constant density layers , is:', M_analytical, "kg")  # Analytical mass of the moon

#     #find numerical error:
#     error = abs(M_analytical - M_r_array[-1])
#     print('The error is:', error, 'kg')
#     print('The relative error is:', error / M_analytical * 100, '%') 

# #=========================================== to generate w11 csv for plotting ==========================================
# if model == 'W11':
#     # integrate constant density model to find mass profile
#     r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
#     #Calculate gravity profile from mass profile:
    
#     g_r_array = -G * M_r_array / r_array**2
#     g_r_array[0] = 0  # avoid division by zero at center
#     print (len(g_r_array))
    
#     r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
#     print (len(p_r_array))
#     #add respective columns in df:
#     results_df = add_to_df(r_array, 'Radius', results_df)
#     results_df = add_to_df(M_r_array, 'Mass', results_df)
#     results_df = add_to_df(g_r_array, 'Gravity', results_df)
#     results_df = add_to_df(p_r_array/(1e9), 'Pressure', results_df)
#     results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density', results_df)
#     results_df.to_csv('Code/w11_moon.csv')
#     #print(M_r_array[-1])  # Total mass of the moon
# #=========================================== to generate vpremoon csv for plotting ==========================================
# if model == 'vpremoon':
#     # integrate constant density model to find mass profile
#     r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
#     #Calculate gravity profile from mass profile:
    
#     g_r_array = -G * M_r_array / r_array**2
#     g_r_array[0] = 0  # avoid division by zero at center
#     print (len(g_r_array))
    
#     r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
#     print (len(p_r_array))
#     #add respective columns in df:
#     results_df = add_to_df(r_array, 'Radius', results_df)
#     results_df = add_to_df(M_r_array, 'Mass', results_df)
#     results_df = add_to_df(g_r_array, 'Gravity', results_df)
#     results_df = add_to_df(p_r_array/(1e9), 'Pressure', results_df)
#     results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density', results_df)
#     results_df.to_csv('Code/vpre_moon.csv')
#     #print(M_r_array[-1])  # Total mass of the moon
# #=========================================== M1: ct density layers ==========================================

# if model =='M1':
#     # integrate constant density model to find mass profile
#     r_array, M_r_array = euler_upward(0, dr, R_moon, dM_dr)
#     #Calculate gravity profile from mass profile:
    
#     g_r_array = -G * M_r_array / r_array**2
#     g_r_array[0] = 0  # avoid division by zero at center
#     print (len(g_r_array))
    
#     r_array, p_r_array = euler_downward(0, dr, R_moon, dp_dr)
#     print (len(p_r_array))
#     #add respective columns in df:
#     results_df = add_to_df(r_array, 'Radius', results_df)
#     results_df = add_to_df(M_r_array, 'Mass', results_df)
#     results_df = add_to_df(g_r_array, 'Gravity', results_df)
#     results_df = add_to_df(p_r_array/(1e9), 'Pressure', results_df)
#     results_df = add_to_df(np.array([rho_(r) for r in r_array]), 'Density', results_df)
#     results_df.to_csv('Code/output/integration_output.csv')
#     #print(M_r_array[-1])  # Total mass of the moon
#     print('The numerically computed solution, assuming constant density layers, is:', M_r_array[-1], 'kg')

#     #compare with analytical solution: 
#     #TODO: compute analytical solution for layered density
#     #find numerical error:
#     #error = abs(M_analytical - M_r_array[-1])
#     #print('The error is:', error, 'kg') 
#     #plot own results vs vpre and w11 models





# #store results in csv
    






