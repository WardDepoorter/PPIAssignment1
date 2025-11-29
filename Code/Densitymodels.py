M1 = [
        {"r_in": 0,       "r_out": 240e3,   "rho": 8000},  # inner core
        {"r_in": 240e3,   "r_out": 330e3,   "rho": 5100},  # outer core
        {"r_in": 330e3,   "r_out": 480e3,   "rho": 3400},  # partial melt
        {"r_in": 480e3,   "r_out": 1709e3,  "rho": 3360},  # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2746},  # crust
        {"r_in": 1736e3,  "r_out": 1737.4e3,  "rho": 2600},  # regolith
    ]



vpremoon = [
        {"r_in": 0,       "r_out": 380e3,   "rho": 5171},  #  core
        {"r_in": 380e3,   "r_out": 1709e3,  "rho": 3374},  # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2762},  # crust
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
