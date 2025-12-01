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



