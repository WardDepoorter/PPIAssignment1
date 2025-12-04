import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 

from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import plot, add_to_df
from Interior_models import M1, W11, vpremoon, ct,test, M1_340, M1_420

#================================================== constants =====================================================
G = const.G.to('m3 / (kg s2)').value # m^3 / (kg s^2)
R_moon = 1737.4 * 1e3  # me
M_moon = 7.346e22  # kg
I_factor_moon = 0.3932 # dimensionless

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
    if model == M1_340:
        for layer in M1_340:
            if layer['r_in'] <= r < layer['r_out']:
                return layer['rho']
    if model == M1_420:
        for layer in M1_420:
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



def MMI(rho, r_o, r_i):
    """
    Calculate the moment of inertia for a spherical shell,with ct density
    """
    if r_i >= r_o:
        raise TypeError("Inner radius must be less than outer radius.")
    
    I_shell = (8/15) * np.pi * rho * (r_o**5 - r_i**5)
    return I_shell



def Mass(rho, r_o, r_i):
    """
    Calculate the mass of a spherical shell, with ct density
    """
    if r_i >= r_o:
        raise TypeError("Inner radius must be less than outer radius.")
    M_shell = (4/3) * np.pi * rho * (r_o**3 - r_i**3)
    return M_shell


def mass_and_inertia(model):
    '''
    Calculate total mass and moment of inertia for a given density model.
    This is used to check if the model used fits the known mass and inertia of the moon.
    Params: model: list of dictionaries containing  'r_out', 'r_in'and 'rho' 
    returns: M_total, I_total, I_factor'''

    M_total = 0.0
    I_total = 0.0
    I_factor = 0.0
    for layer in model:
        r_in  = layer["r_in"]
        r_out = layer["r_out"]
        rho   = layer["rho"]

        # mass contribution
        M_total += Mass(rho, r_out, r_in)

        # moment of inertia contribution
        I_total += MMI(rho, r_out, r_in)
    I_factor = I_total / (M_total * (model[-1]["r_out"])**2)
    return M_total, I_total, I_factor
 
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
    

    



#model = M1
# # ==== uncomment to check mass and inertia of model: ====
# M, I , I_factor = mass_and_inertia(model)
# print(f"Total Mass:           {M} kg")
# print(f"Total Moment of Inertia: {I} kg·m²")
# print(f"Inertia Factor:       {I_factor}")
#dr = 100  # m step size 



#=================  generate csv for min/max vs avg =========================================

# dr = 100  # m step size
# model = M1
# results_df = integrate(model, dr, results_df)
# results_df.to_csv('Code/output/integration_output_380km.csv', index=False)


# results_df = pd.DataFrame()
# model  = M1_340
# results_df = integrate(model, dr, results_df)
# results_df.to_csv('Code/output/integration_output_340km.csv', index=False)



# results_df = pd.DataFrame()
# model  = M1_420
# results_df = integrate(model, dr, results_df)
# results_df.to_csv('Code/output/integration_output_420km.csv', index=False)
# #=================  plotting for min/max vs avg =========================================








#Old code:

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
    






