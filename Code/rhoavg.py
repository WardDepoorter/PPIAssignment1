import numpy as np
import pandas as pd
from Euler_intergrators import euler_upward, euler_downward

df = pd.read_csv('VPREMOON.csv')
r = df['r'].to_numpy()
rho = df['rho'].to_numpy()

r_array = np.array([])  
rho_array = np.array([])
m_array = np.array([0])  # initial mass at center is 0

for i in range(len(r)):
    if 380 < r[i] < 1710:
        r_array = np.append(r_array, r[i]*1e3)  # convert to meters
        rho_array = np.append(rho_array, rho[i]*1e3)  # convert to kg/m^3
        #print(r_array)
        #print(rho_array)

r_array = r_array[::-1]
rho_array = rho_array[::-1]
print(rho_array)
print(r_array)
for i in range(1, len(r_array)):
   
    dmdr = 4.0 * np.pi * r_array[i]**2 * rho_array[i]
    #print(dmdr)
    m = m_array[-1] + dmdr * (r_array[i] - r_array[i-1])
    m_array = np.append(m_array, m)

print(m_array)
V = 4/3 * np.pi *((1709*1e3)**3 - (380*1e3)**3)
rho_avg = m_array[-1] / V
print("Average density between 380 km and 1710 km:", rho_avg, "kg/m^3")

        