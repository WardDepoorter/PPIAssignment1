from typing import Union, Optional, Tuple
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

def reverse_data(file):
    """
    Reads a CSV file, reverses the order of its rows, and saves it back.
    """
    df = pd.read_csv(file)
    df_reversed = df.iloc[::-1].reset_index(drop=True)
    df_reversed.to_csv(file+'_reversed.csv', index=False)
    return df_reversed

reverse_data('vpremoon.csv')
r = np.array([0, 245, 340, 480, 1709, 1736, 1737.4]) * 1e3  # m
rho = np.array([6435, 5100, 3400, 3360, 2746, 2600])  # kg/m^3


def MMI(rho, r_o, r_i):
    """
    Calculate the moment of inertia factor for a spherical shell.
    """
    I_shell = (8/15) * np.pi * rho * (r_o**5 - r_i**5)
    return I_shell

def calc_I_factor(M_moon, R_moon, density):
    i = 1
    I_total = 0
    while i < 7 :
        r_o = r[i]  # outer radius of the layer
        r_i = r[i-1]  # inner radius of the layer
        rho_layer = density[i-1]  # density of the layer
        I_layer = MMI(rho_layer, r_o, r_i)
        I_total += I_layer
        i += 1
        I_factor = I_total / (M_moon * R_moon**2)
    return I_factor
#I_f =calc_I_factor(7.34948e22, 1737.4e3, rho)
#print("Calculated Moment of Inertia Factor:", I_f)
#reverse_data('w11.csv')
df = pd.read_csv('w11_reversed.csv')
df['R'] = 1737.1 - df['R'] 
df.to_csv('w11_reversed_adjusted.csv', index=False)