import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 
import scipy.optimize as optimize
from Interior_models import M1, W11, vpremoon, ct, test
from M1 import MMI, Mass
from save_and_plot import plot_array
#params to constrain M1

M_moon = 7.346e22  # kg
I_factor_moon = 0.3932 # dimensionless
R_moon = 1737.4e3  # m
I_moon = I_factor_moon * M_moon * R_moon**2  # kg·m²
print(I_moon)
model = vpremoon
# vpremoon = [
#         {"r_in": 0,       "r_out": 380e3,   "rho": 8000},  #  core
#         {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3360},  # mantle
#         {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},  # crust
#         {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
#     ]


def core_mass(M_tot, model):
    r_core = model[1]['r_in']
    for layer in model:
        if layer['r_in'] >= r_core:
            M_tot -= Mass(layer['rho'], layer['r_out'], layer['r_in'])
    M_core = M_tot
    return M_core

def core_inertia(I_tot, model):
    r_core = model[1]['r_in']
    for layer in model:
        if layer['r_in'] >= r_core:
            
            mmi_layer = MMI(layer['rho'], layer['r_out'], layer['r_in'])
            print(mmi_layer)
            I_tot -= mmi_layer
    I_core = I_tot

    return I_core, 
def r_three(r_o, r_i):
    return r_o**3 - r_i**3
def r_five(r_o, r_i):   
    return r_o**5 - r_i**5

M_core = core_mass(M_moon, model)
I_core,  = core_inertia(I_moon, model)
print(f"Core Mass:              {M_core} kg")
print(f"Core Moment of Inertia: {I_core} kg·m²")

def eqns_to_solve(vars, r_core):
    r_c_inner, rho_c_outer = vars  # outer core radius and inner core density 
    r_crust  = 1709e3
    
    M = -((3*M_moon)/(4*np.pi))  + 2600 * r_three(1737.4e3,1736e3) + 2762 * r_three(1736e3,r_crust) + 3400 * r_three(r_crust,r_core) + rho_c_outer * r_three(r_core,r_c_inner) + 7000 * r_three(r_c_inner,0)
    I = -((15*I_moon)/(8*np.pi)) + 2600 * r_five(1737.4e3,1736e3) + 2762 * r_five(1736e3,r_crust) + 3400 * r_five(r_crust,r_core) + rho_c_outer * r_five(r_core,r_c_inner) + 7000 * r_five(r_c_inner,0)
    return [M, I]


r_core = np.linspace(340e3, 420e3, 200)
rho_core_outer =np.array([])  
r_core_inner = np.array([])


for i in r_core:
    Guess = [190e3, 6000]  # initial guess for mantle density and core
    solution = optimize.fsolve(eqns_to_solve, Guess, args=(i,))
    print(f"For core radius {i} m, optimal inner core radius and outer core density:", solution)
    r_core_inner = np.append(r_core_inner, solution[0])
    rho_core_outer = np.append(rho_core_outer, solution[1])


# Guess = [200e3, 6000]  # initial guess for mantle density and core
# solution = optimize.fsolve(eqns_to_solve, Guess, args=(r_core,))
# print(solution)
print(r_core_inner)
print(rho_core_outer)


# Plot both:
r_core_km = r_core / 1e3
r_core_inner_km = r_core_inner / 1e3

fig, ax1 = plt.subplots()

# Left axis: density (make this line red)
ln1 = ax1.plot(r_core_km, rho_core_outer, color='tab:red', label='Outer Core Density')
ax1.set_xlabel('Outer Core Radius (km)')
ax1.set_ylabel('Outer Core Density (kg/m^3)')
ax1.tick_params(axis='y')

# Right axis: inner core radius
ax2 = ax1.twinx()
ln2 = ax2.plot(r_core_km, r_core_inner_km, color='tab:blue', label='Inner Core Radius')
ax2.set_ylabel('Inner Core Radius (km)')
ax2.tick_params(axis='y')

# Vertical dotted red line at nominal core radius 380 km
vline = ax1.axvline(380, color='red', linestyle=':', linewidth=1.5)

# Combined legend
lines = ln1 + ln2 
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='best')

# Grid: both horizontal and vertical
ax1.grid(True, which='both', axis='both', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()















# Guess = [190e3, 6000]  # initial guess for outer core radius and inner core density
# k =380e3  
# solution = optimize.fsolve(eqns_to_solve, Guess, args=(k,))
# print(solution)

'''
def eqns_to_solve(vars, i):
    M_moon = 7.346e22
    I_factor = 0.3932 # m, fixed inner core radius
    r_o, rho_i = vars  # outer core radius and inner core density 
    MMI = I_factor * M_moon * (1737.4e3)**2  # m, fixed inner core radius
    vars = (r_o, rho_i)
      # use the outer-scope loop value during iteration
    mct = r_three(1737.4e3,1736e3) * 2600  + r_three(1736e3,1709e3) * 2746 + r_three(1709e3,480e3) * 3380    + r_three(480e3,340e3) * 3400 - ((3*M_moon)/(4*np.pi))
    Ict = 2600*r_five(1737.4e3,1736e3)    + 2746 * r_five(1736e3,1709e3) + 3380*r_five(1709e3,480e3)      + 3400*r_five(480e3,340e3) - ((15*MMI)/(8*np.pi))
    #print("Current guess:", vars, "Mass diff:", mct, "Inertia diff:", Ict)
    M = mct+ 5100* (r_o**3 - i**3) + (i**3)* rho_i 
    I = Ict+ 5100 * ((r_o**5) - (i**5)) + rho_i * (i**5)
    return [M , I]

Guess = [340e3, 6500]  # initial guess for outer core radius and inner core density
k =240e3  
solution = optimize.fsolve(eqns_to_solve, Guess, args=(k,))
print(solution)
#print("Optimal outer core radius (m) and inner core density (kg/m^3):", solution)

i_array = np.linspace(0, 340e3, 100)
for i in i_array: 
    Guess = [300e3, 6000]  # initial guess for outer core radius and inner core density
    solution = optimize.fsolve(eqns_to_solve, Guess, args=(i,))
    print("For inner core radius:", i, "Optimal outer core radius (m) and inner core density (kg/m^3):", solution)
    '''