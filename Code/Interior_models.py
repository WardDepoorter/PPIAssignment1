#          inner radius     outer radius     density        inner T   Outer Temp alpha          Specific heat Viscosity         k 
#          r_in : m         r_out : m        rho : kg/m^3   T_in : K  T_out : K  alpha : 1/K    Cp : J/kg·K   eta : Pa·s      k : W/m·K
M2 = [
        {"layer": "inner core", "r_in": 0,       "r_out": 128.088e3,  "rho": 7000, 'T_in': 1900, 'T_out': 1800, 'alpha':  8e-5, 'Cp': 700 , 'eta': 10**30, 'k': 80},    #  inner core:rigid!
        {"layer": "outer core", "r_in": 128.088e3,   "r_out": 380e3,  "rho": 5980.78, 'T_in': 1800, 'T_out': 1650, 'alpha': 9e-5, 'Cp': 698, 'eta': 2*10**16, 'k': 45},  #  outer core
        {"layer": "mantle", "r_in": 380e3,   "r_out": 1709e3,  "rho": 3400, 'T_in': 1650, 'T_out': 650, 'alpha': 2.75e-5, 'Cp': 1200, 'eta': 10**21, 'k': 3.06},  # mantle
        {"layer": "crust", "r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762, 'T_in': 650, 'T_out': 300, 'alpha': 2.75e-5, 'Cp': 1100, 'eta': 10**24, 'k': 3.06},  # crust
        {"layer": "regolith", "r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600, 'T_in': 300, 'T_out': 273.15, 'alpha': 2.75e-5, 'Cp': 800, 'eta': 10**24, 'k': 0.7},  # regolith
    ]
M1 = [
        {"layer": "inner core", "r_in": 0,       "r_out": 128.088e3,  "rho": 7000},    #  inner core:rigid!
        {"layer": "outer core", "r_in": 128.088e3,   "r_out": 380e3,  "rho": 5980.78},  #  outer core
        {"layer": "mantle", "r_in": 380e3,   "r_out": 1709e3,  "rho": 3400},  # mantle
        {"layer": "crust", "r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},  # crust
        {"layer": "regolith", "r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]
M1_340 = [
        {"r_in": 0,       "r_out": 124602.79,  "rho": 7000},    #  inner core
        {"r_in": 124602.79 ,   "r_out": 340e3,  "rho": 5955.73},#  outer core
        {"r_in": 340e3,   "r_out": 1709e3,  "rho": 3400},    # mantle   
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},    # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]
M1_420 = [
        {"r_in": 0,       "r_out": 134491.36,  "rho": 7000},    #  inner core
        {"r_in": 134491.36,   "r_out": 420e3,  "rho": 5991.49},#  outer core
        {"r_in": 420e3,   "r_out": 1709e3,  "rho": 3400},    # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},    # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]



vpremoon = [
        {"r_in": 0,       "r_out": 380e3,   "rho": 5171},  #  core
        {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3400},  # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},  # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]


test = [
        {"r_in": 0,       "r_out": 380e3,   "rho": 8000},  #  core
        {"r_in": 380e3,   "r_out": 1124113.94733169,  "rho": 4343.64},  # mantle
        {"r_in": 1124113.94733169,  "r_out": 1736e3,  "rho": 2762},  # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]



W11 = [
        {"r_in": 0,    "r_out": 240e3,   "rho": 8000},  # inner core
        {"r_in": 240e3,"r_out": 330e3,   "rho": 5100},  # outer core
        {"r_in": 330e3,"r_out": 480e3,   "rho": 3400},  # partial melt                
        {"r_in": 480e3,"r_out": 1499.1e3,  "rho": 3400},  # lower mantle
        {"r_in": 1499.1e3,"r_out": 1697.1e3,  "rho": 3300},  # upper mantle
        {"r_in": 1697.1e3,"r_out": 1722.1e3, "rho": 2800},  # lower crust
        {"r_in": 1722.1e3,"r_out": 1736.1e3, "rho": 2700},  # upper crust
        {"r_in": 1736.1e3,"r_out": 1737.1e3, "rho": 2600},  # regolith
        ]
ct = [{"r_in": 0, "r_out": 1737.4e3, "rho": 3345.56}]  
