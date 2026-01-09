import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 


#Euler integration for 1D interior model of the moon 
from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import plot, add_to_df
#from M1 import *
from Interior_models import M2_min, M2_avg, M2_max

#calculate rayleigh number for each shell
#see if layers are convective or conductive
#calculate thermal gradient accordingly
# def kappa_calc(k, rho, c_p):
#     """
#     Calculate thermal diffusivity.
#     Params:
#     k : float
#         Thermal conductivity (W/m·K)
#     rho : float
#         Density (kg/m³)
#     c_p : float
#         Specific heat capacity (J/kg·K)

#     Returns:
#     float
#         Thermal diffusivity (m²/s)
#     """
#     kappa = k / (rho * c_p)
#     return kappa

def Rayleigh_number(layer):
    """
    Calculate the Rayleigh number for a spherical shell.
    Params:
    alpha : float
        Thermal expansivity (1/K)
    g : float
        Gravitational acceleration (m/s²)
    rho : float
        Density (kg/m³)
    deltaT : float
        Temperature difference across the shell (K)
    r_in : float
        Inner radius of the shell (m)
    r_out : float( d = r_out - r_in)
        Outer radius of the shell (m)
    eta : float
        Dynamic viscosity (Pa·s)
    k : float
        Thermal conductivity (W/m·K)
    c_p : float
        Specific heat capacity (J/kg·K)
    Returns:
    float
        The Rayleigh number.
   
    """
    name = layer['layer']
    df = pd.read_csv('Code/output/integration_output_380km.csv')
    # Average gravity only within the layer's radial bounds
    r_in = layer['r_in']
    r_out = layer['r_out']
    g = -1* df.loc[(df['Radius'] >= r_in) & (df['Radius'] <= r_out), 'Gravity'].mean()
    alpha = layer['alpha']
    c_p = layer['Cp']
    eta = layer['eta']
    k = layer['k']
    rho = layer['rho']
    r_in = layer['r_in']
    r_out = layer['r_out']
    deltaT = layer['T_in'] - layer['T_out']
   
    d = r_out - r_in
    kappa = k / (rho * c_p)
    Ra = (alpha * g * rho * deltaT * d**3) / (kappa * eta)
    return Ra

## Calculate and print initial Rayleigh numbers for M2 models
# print('M2_min model:')
# for layer in M2_min:
#     Ra = Rayleigh_number(layer)
#     print(f" {layer['layer']} from {layer['r_in']/1e3:.1f} km to {layer['r_out']/1e3:.1f} km: Rayleigh number = {Ra:.2e}")

# print('M2_avg model:')    
# for layer in M2_avg:
#     Ra = Rayleigh_number(layer)
#     print(f" {layer['layer']} from {layer['r_in']/1e3:.1f} km to {layer['r_out']/1e3:.1f} km: Rayleigh number = {Ra:.2e}")
# print('M2_max model:')
# for layer in M2_max:
#     Ra = Rayleigh_number(layer)
#     print(f" {layer['layer']} from {layer['r_in']/1e3:.1f} km to {layer['r_out']/1e3:.1f} km: Rayleigh number = {Ra:.2e}")

#integrate thermal profile:
def thermal(model, M1_csv):
    df = pd.read_csv(M1_csv)
    T_array = np.zeros(len(df))
    df = add_to_df(T_array, 'Temperature', df)
    
    for layer in reversed(model):
        Ra = Rayleigh_number(layer)
        
        print(f"Layer: {layer['layer']}, Rayleigh number: {Ra:.2e}")
        if Ra > 1e3:
            print(f"Layer {layer['layer']} is convective.")
            T_out = layer['T_out']
            R_in = layer['r_in']
            R_out = layer['r_out']
            T_in = layer['T_in']
            alpha = layer['alpha']
            Cp = layer['Cp']

            T_avg = (T_in + T_out) / 2
            for i in range(len(df)):
                r = df['Radius'][i]
                if R_in <= r <= R_out:
                    g =-1* df.loc[i, 'Gravity']
                    dTdz = (g * alpha * (T_avg)) / Cp
                    T = T_in + dTdz * (r - R_out)
                    df.loc[i, 'Temperature'] = T
        else:
            print(f"Layer {layer['layer']} is conductive.")
            T_out = layer['T_out']
            R_in = layer['r_in']
            R_out = layer['r_out']
            T_in = layer['T_in']
            
            dz = R_out - R_in
            dT = T_out - T_in
            dTdz = dT / dz
            
            T_0 = T_out  # Temperature at the outer boundary
            for i in range(len(df)):
                r = df['Radius'][i]
                if R_in <= r <= R_out:
                    T = T_0 + dTdz * (r - R_out)
                    df.loc[i, 'Temperature'] = T
    
    return df


model = M2_avg
csv = 'Code/output/integration_output_380km.csv'

df = thermal(model, M1_csv=csv)
df.to_csv('Code/output/thermal_profile_M2_avg_380km.csv', index=False)