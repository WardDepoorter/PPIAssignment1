import numpy as np
import pandas as pd
from Euler_intergrators import euler_upward, euler_downward


df = pd.read_csv('vpremoon.csv')
r = df['Radius'].to_numpy()
rho = df['Density'].to_numpy()

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
   
    dmdr = 4.0 * np.pi * r_array[i-1]**2 * rho_array[i-1]
    #print(dmdr)
    m = m_array[-1] + dmdr * (r_array[i] - r_array[i-1])
    m_array = np.append(m_array, m)

print(m_array)
V = 4/3 * np.pi *((1709*1e3)**3 - (380*1e3)**3)
rho_avg = m_array[-1] / V
print("Average density between 380 km and 1710 km:", rho_avg, "kg/m^3")

#simple sum average:
rho_simple_avg = np.mean(rho_array)
print("Simple average density between 380 km and 1710 km:", rho_simple_avg, "kg/m^3")
#integrate mass vpremoon:
df = pd.read_csv('vpremoon.csv')
r = df['Radius'].to_numpy()*1000  # convert to meters
rho = df['Density'].to_numpy()*1000  # convert to kg/m^3
dmdr_array = 4.0 * np.pi * r**2 * rho

M_r_array = np.array([0])  # initial mass at center is 0
# integrate starting from the bottom (core) by reversing arrays
r_rev = r[::-1]
dmdr_rev = dmdr_array[::-1]

for i in range(1, len(r_rev)):
    dmdr = dmdr_rev[i - 1]
    dr = r_rev[i] - r_rev[i - 1]
    m = M_r_array[-1] + dmdr * dr
    M_r_array = np.append(M_r_array, m)
print(M_r_array[-1])
#add m array to dataframe and save as csv for plotting:
df['Mass'] = M_r_array[::-1]
df.to_csv('vpremoon.csv', index=False)


