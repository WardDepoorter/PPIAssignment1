#          inner radius     outer radius     density        inner T   Outer Temp alpha          Specific heat Viscosity         k 
#          r_in : m         r_out : m        rho : kg/m^3   T_in : K  T_out : K  alpha : 1/K    Cp : J/kg·K   eta : Pa·s      k : W/m·K
M1 = [
        {"r_in": 0,       "r_out": 110.188e3,  "rho": 7000, 'T_in': 1900, 'T_out': 1800, 'alpha':  72, 'Cp': 448 , 'eta': None, 'k': 20.4},    #  inner core
        {"r_in": 110.188e3,   "r_out": 380e3,  "rho": 5962.2, 'T_in': 1800, 'T_out': 1650, 'alpha': None, 'Cp': None, 'eta': 2*10**16, 'k': None},  #  outer core
        {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3400, 'T_in': 1650, 'T_out': 650, 'alpha': None, 'Cp': None, 'eta': 10**21, 'k': 4},  # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762, 'T_in': 650, 'T_out': 300, 'alpha': None, 'Cp': None, 'eta': None, 'k': None},  # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600, 'T_in': 300, 'T_out': 273.15, 'alpha': None, 'Cp': None, 'eta': None, 'k': None},  # regolith
    ]
M1_340 = [
        {"r_in": 0,       "r_out": 104515,  "rho": 7000},    #  inner core
        {"r_in": 104515,   "r_out": 380e3,  "rho": 5912.139},#  outer core
        {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3400},    # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},    # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]
M1_420 = [
        {"r_in": 0,       "r_out": 131089,  "rho": 7000},    #  inner core
        {"r_in": 131089,   "r_out": 380e3,  "rho": 5985.687},#  outer core
        {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3400},    # mantle
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
