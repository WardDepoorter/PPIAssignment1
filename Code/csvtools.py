from typing import Union, Optional, Tuple
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def reverse_data(file):
    """
    Reads a CSV file, reverses the order of its rows, and saves it back.
    """
    df = pd.read_csv(file)
    df_reversed = df.iloc[::-1].reset_index(drop=True)
    df_reversed.to_csv(file+'_reversed.csv', index=False)
    return df_reversed
reverse_data('vpremoon.csv')

