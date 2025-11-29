import numpy as np

def mass_and_inertia(layers):
    """
    Compute total mass and moment of inertia of a layered spherical body.

    Parameters
    ----------
    layers : list of dicts
        Each layer must be of form:
        {
            "r_in": inner radius (m),
            "r_out": outer radius (m),
            "rho": density (kg/m^3)
        }

    Returns
    -------
    M_total : float
        Total mass (kg)
    I_total : float
        Total moment of inertia (kg·m²)
    """

    M_total = 0.0
    I_total = 0.0

    for layer in layers:
        r_in  = layer["r_in"]
        r_out = layer["r_out"]
        rho   = layer["rho"]

        # mass contribution
        M_total += (4.0*np.pi/3.0) * rho * (r_out**3 - r_in**3)

        # moment of inertia contribution
        I_total += (8.0*np.pi/15.0) * rho * (r_out**5 - r_in**5)
    I_factor = I_total / (M_total * (layers[-1]["r_out"])**2)
    return M_total, I_total, I_factor



if __name__ == "__main__":
    # Example Moon-like layering
    Layers = [
        {"r_in": 0,       "r_out": 240e3,   "rho": 8000},  # inner core
        {"r_in": 240e3,   "r_out": 330e3,   "rho": 5100},  # outer core
        {"r_in": 330e3,   "r_out": 480e3,   "rho": 3400},  # partial melt
        {"r_in": 480e3,   "r_out": 1709e3,  "rho": 3360},  # mantle
        {"r_in": 1709e3,  "r_out": 1736e3,  "rho": 2746},  # crust
        {"r_in": 1736e3,  "r_out": 1737e3,  "rho": 2600},  # regolith
    ]

    M, I , I_factor = mass_and_inertia(layers)

    print(f"Total Mass:           {M} kg")
    print(f"Total Moment of Inertia: {I} kg·m²")
    print(f"Inertia Factor:       {I_factor}")