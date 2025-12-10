import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 


#Euler integration for 1D interior model of the moon 
from Euler_intergrators import euler_upward, euler_downward 
from save_and_plot import plot, add_to_df
from M1 import *

#create empty dataframe to store results
results_df = pd.DataFrame()

T_core = [T_core_lower,T_core_avg, T_core_upper] = [1600, 1900, 2200]  # K, core temperature options from Garcia et al. 2019

#calculate rayleigh number for each shell
#see if layers are convective or conductive
#calculate thermal gradient accordingly
def kappa_calc(k, rho, c_p):
    """
    Calculate thermal diffusivity.
    Params:
    k : float
        Thermal conductivity (W/m·K)
    rho : float
        Density (kg/m³)
    c_p : float
        Specific heat capacity (J/kg·K)

    Returns:
    float
        Thermal diffusivity (m²/s)
    """
    kappa = k / (rho * c_p)
    return kappa

def Rayleigh_number(alpha, g, rho, deltaT, r_in, r_out, eta, k, c_p):
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
    d = r_out - r_in
    kappa = k / (rho * c_p)
    Ra = (alpha * g * rho * deltaT * d**3) / (kappa * eta)
    return Ra
