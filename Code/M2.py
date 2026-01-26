import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 

#Euler integration for 1D interior model of the moon 
from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import add_to_df
#from M1 import *
from Interior_models import M2_min, M2_avg, M2_max, get_from_dict, get_from_profile
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
def thermal(model, M1_csv,df):
    columnname = 'T_' + [name for name in globals() if globals()[name] is model][0]
    print(columnname)
    
    T_array = np.zeros(len(df))
    df = add_to_df(T_array, columnname, df)
    
    for layer in model:
        # calculate Ra
        Ra = Rayleigh_number(layer)
        print(f"Layer: {layer['layer']}, Rayleigh number: {Ra:.2e}")
        # base don Ra, find out if convective or conductive

        if Ra > 1e6:#convective
            print(f"Layer {layer['layer']} is convective.")
            
            R_in = layer['r_in']
            R_out = layer['r_out']
            T_in = df.loc[(df['Radius'] >= R_in) & (df['Radius'] <= R_out), columnname].iloc[0]#T_out of previous layer
            alpha = layer['alpha']
            Cp = layer['Cp']
            for i in range(len(df)):
                r = df['Radius'][i]
                if R_in <= r <= R_out:
                    g =-1* df.loc[i-1, 'Gravity']
                    temp = df.loc[i-1, columnname]
                    dTdz = (g * alpha * (temp)) / Cp
                    T = temp - dTdz * 100
                    df.loc[i, columnname] = T
        else: 
            if layer['layer'] == 'inner core':#conductive
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
                        df.loc[i, columnname] = T
            else:
                print(f"Layer {layer['layer']} is conductive.")
                T_out = layer['T_out']
                R_in = layer['r_in']
                R_out = layer['r_out']
                T_in = df.loc[(df['Radius'] >= R_in) & (df['Radius'] <= R_out), columnname].iloc[0]
                #print(T_in)

                dz = R_out - R_in
                dT = T_out - T_in
                dTdz = dT / dz
                
                T_0 = T_out  # Temperature at the outer boundary
                for i in range(len(df)):
                    r = df['Radius'][i]
                    if R_in <= r <= R_out:
                        T = T_0 + dTdz * (r - R_out)
                        df.loc[i, columnname] = T
    return df

print("Integrating thermal profile for M2 models...")
csv = 'Code/output/integration_output_380km.csv'
df = pd.read_csv(csv)
df = thermal(M2_min, M1_csv=csv, df=df)
df = thermal(M2_avg, M1_csv=csv, df=df)
df = thermal(M2_max, M1_csv=csv, df=df)

df.to_csv('Code/output/thermal_profile_M2_380km.csv', index=False)
plot_thermal_profile  = False
#plot results for min, avg, max models:
if plot_thermal_profile:
    plt.figure(figsize=(8, 6))

    # Define layer boundaries and colors
    colors = {'inner core': 'red', 'outer core': 'orange', 'mantle': 'blue', 'crust': 'green'}

    # Plot min, avg, and max models
    for model, linestyle in zip([M2_min, M2_avg, M2_max], [':', '-', '--']):
        model_name = 'min' if linestyle == ':' else 'avg' if linestyle == '-' else 'max'
        
        for i, layer in enumerate(model):
            layer_name = layer['layer']
            
            # Filter data for this layer
            layer_data = df[(df['Radius'] >= layer['r_in']) & (df['Radius'] <= layer['r_out'])]
            
            temp_col = f'T_M2_{model_name}'
            
            # Only add label for the first model to avoid duplicate legends
            label = layer_name if model_name == 'avg' else None
            
            plt.plot(layer_data[temp_col], layer_data['Radius'] / 1e3, label=label, color=colors.get(layer_name, 'gray'), linewidth=2, linestyle=linestyle)

    plt.xlabel('Temperature (K)')
    plt.ylabel('Radius (km)')
    plt.title('Thermal Profile for M2 Models')
    plt.legend()
    plt.grid(True)
    plt.show()


# iterate M2 mass, P and G profiles for min, avg, max models
#based on linear local density profile rho(dT, dp) 
#start from M1 w thermal profile csv, 380 km core radius

csv = 'Code/output/thermal_profile_M2_380km.csv'
df_M1 = pd.read_csv(csv)

def get_ref_T(model, layer_name):
    T_in = get_from_dict('T_in', layer_name , model) 
    T_out = get_from_dict('T_out', layer_name , model)
    return (T_in + T_out) / 2

def get_ref_P(model,layer_name, df = df_M1):
    r_in = get_from_dict('r_in', layer_name , model)
    r_out = get_from_dict('r_out', layer_name , model)
    
    P_in = get_from_profile('Pressure', df, r_in)
    P_out = get_from_profile('Pressure', df, r_out)
    
    return (P_in + P_out) / 2

# def density(R, model, df):
#     """
#     Calculate density at radius R based on linearized equation of state.
#     Params:
#     R : float
#         Radius at which to calculate density (m).
#     model : list of dicts
#         Interior model defining layers and their properties.
#     df : pandas DataFrame
#         DataFrame containing temperature and pressure profiles.
#     Returns:
#     float
#         Density at radius R (kg/m³).
#     """
#     #find which layer R is in
#     for layer in model:
#         r_in = layer['r_in']
#         r_out = layer['r_out']
#         layer_name = layer['layer']
#         if r_in <= R <= r_out:
#             #take Tref and Pref at layer(independent of iteration):
#             Tref = get_ref_T(model, layer_name)
#             Pref = get_ref_P(model, layer_name)
#             rho0 = layer['rho']
#             #get local T and P from df:
#             T = 
            
            
            
#             return rho
#     raise ValueError(f"Radius {R} not found in any layer of the model.")
