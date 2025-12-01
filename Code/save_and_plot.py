#from turtle import save
from typing import Union, Optional, Tuple
import pandas as pd
import argparse
import matplotlib.pyplot as plt

#!/usr/bin/env python3

def plot(model1_csv, model2_csv, model3_csv, model4_csv=None):
    """
    model1 = your model (red solid)
    model2 = green dotted
    model3 = blue dotted
    """

    import pandas as pd
    import matplotlib.pyplot as plt

    label1 = "New Model"
    label2 = "VPREMOON Model"
    label3 = "W11 Model"

    
    # Load data
    m_own = pd.read_csv(model1_csv)
    m_vpre = pd.read_csv(model2_csv)
    m_w11 = pd.read_csv(model3_csv)

    # Extract columns
    r1, M1, g1, P1 = m_own["Radius"]/1000, m_own["Mass"], -m_own["Gravity"], m_own["Pressure"]
    r2, M2, g2, P2 = m_vpre["Radius"]/1000, m_vpre["Mass"], -m_vpre["Gravity"], m_vpre["Pressure"]
    r3, M3, g3, P3 = m_w11["Radius"]/1000, m_w11["Mass"], -m_w11["Gravity"], m_w11["Pressure"]

    if model4_csv:
        m_vpre_mass = pd.read_csv(model4_csv)
        r4, M4, g4, P4 = m_vpre_mass["Radius"], m_vpre_mass["Mass"], m_vpre_mass["Gravity"], m_vpre_mass["Pressure"]

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=True)

    # --- Mass ---
    axes[0].plot(M1, r1, 'r-', label=label1)
    axes[0].plot(M2, r2, 'g-.', label=label2)
    axes[0].plot(M3, r3, 'b-.', label=label3)
    axes[0].set_xlabel("Mass (kg)")
    axes[0].set_title("Mass Integration")
    axes[0].grid(True)

    # --- Gravity ---
    axes[1].plot(g1, r1, 'r-')
    axes[1].plot(g4, r4, 'g-.')
    axes[1].plot(g3, r3, 'b-.')
    axes[1].set_xlabel("Gravity (m/s²)")
    axes[1].set_title("Gravity Profile")
    axes[1].grid(True)

    # --- Pressure ---
    axes[2].plot(P1, r1, 'r-')
    axes[2].plot(P4, r4, 'g-.')
    axes[2].plot(P3, r3, 'b-.')
    axes[2].set_xlabel("Pressure (GPa)")
    axes[2].set_title("Pressure Integration")
    axes[2].grid(True)

    # Y-axis (shared)
    axes[0].set_ylabel("Radius (km)")

    # Reverse y-axis so centre is at bottom and surface at top
    

     # Shared legend (top of figure)
    axes[0].legend( labels=[label1, label2, label3], loc='upper left')

    plt.tight_layout()
    #plt.show()
    plt.savefig('Code/output/mass_gravity_pressure_profiles.png')

def add_to_df(array, column_name, df):
    """
    Add an array as a new column to the dataframe
    Params:
    array : 
        The data to add as a new column
    column_name : str
        The name of the new column.
    df : pandas.DataFrame
        The DataFrame to which the new column will be added.

    Returns:
    pandas.DataFrame
        The updated DataFrame with the new column added.
    """
    df[column_name] = array
    return df
def plot_array(x, y, x_label="x", y_label="y", legend_label="data"):
    plt.figure(figsize=(6,4))
    plt.plot(x, y, label=legend_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f'Code/output/{legend_label.replace(" ","_")}.png')

    
if __name__ == "__main__":
    plot('Code/output/integration_output.csv', 'Code/vpre_moon.csv', 'Code/w11_moon.csv', model4_csv='vpremoon_with_mass.csv')