import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import pandas as pd 
import scipy.optimize as optimize




#  # 
# r = np.array([245, 340, 480, 1709, 1736, 1737]) * 1e3  # m
# r = r[::-1]  # reverse to start from center
# rho = np.array([2600, 2746, 3360 ,3400, 5100])  # kg/m^3
#   # reverse to match radius order

# M = np.array([])  # initial mass at center is 0
# for i in range(5):
#     M = np.append(M, 4/3 * np.pi * ((r[i]**3 - r[i+1]**3) * rho[i]))
# M_total = np.sum(M)
# M_remaining = M_moon - M_total
# rho_core = M_remaining / (4/3 * np.pi * (245e3**3))
# print("core density:", rho_core)



# def core_constraint():
#     #calculats inner core density given outer core radius
#     rho_core = 
#     M = np.array([])  # initial mass at center is 0
#     for i in range(5):
#         M = np.append(M, 4/3 * np.pi * ((r[i]**3 - r[i+1]**3) * rho[i]))
#     M_total = np.sum(M)
#     M_remaining = M_moon - M_total
#     return M_remaining
def r_three(r_o, r_i):
    V = 4/3 * np.pi * (r_o**3 - r_i**3)
    return V

def r_five(r_o, r_i):
    return ((r_o**5) - (r_i**5))   


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
    