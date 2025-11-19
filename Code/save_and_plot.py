from typing import Union, Optional, Tuple
import pandas as pd
import argparse
import matplotlib.pyplot as plt

#!/usr/bin/env python3
"""
PlotFromCsv.py

Small utility to plot two columns from a CSV file.

Usage example:
    plot_csv_columns("data.csv", x_col=0, y_col=1, delimiter=",", save_path="out.png")
"""



def plot_csv_columns(
    csv_path: str,
    x_col: Union[int, str] = 0,
    y_col: Union[int, str] = 1,
    delimiter: str = ",",
    header: Optional[int] = "infer",
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (8, 5),
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Read csv_path and plot two columns.

    Parameters:
    - csv_path: path to CSV file.
    - x_col, y_col: column index (int) or column name (str). Default 0 and 1.
    - delimiter: field delimiter (default ',').
    - header: row number to use as column names, None if no header, or 'infer' (default).
    - xlabel, ylabel, title: optional labels.
    - figsize: figure size.
    - save_path: if provided, save figure to this path.
    - show: if True, call plt.show().

    Returns:
    - (fig, ax) matplotlib figure and axes.
    """
    df = pd.read_csv(csv_path, sep=delimiter, header=header)

    def _col(series_or_index):
        if isinstance(series_or_index, int):
            return df.iloc[:, series_or_index]
        return df[series_or_index]

    x = _col(x_col)
    y = _col(y_col)

    # infer axis labels if not provided
    xlabel = xlabel or (x.name if hasattr(x, "name") and x.name is not None else str(x_col))
    ylabel = ylabel or (y.name if hasattr(y, "name") and y.name is not None else str(y_col))

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, y, marker="o", linestyle="-")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300)

    if show:
        plt.show()

    return fig, ax


if __name__ == "__main__":
    # simple CLI for quick testing

    parser = argparse.ArgumentParser(description="Plot two columns from a CSV file.")
    parser.add_argument("csv", help="CSV file path")
    parser.add_argument("--x", default=0, help="x column (index or name). Default 0")
    parser.add_argument("--y", default=1, help="y column (index or name). Default 1")
    parser.add_argument("--sep", default=",", help="CSV delimiter")
    parser.add_argument("--no-show", action="store_true", help="Do not call plt.show()")
    parser.add_argument("--save", help="Save figure to file")
    args = parser.parse_args()

    # try to convert x/y to int when possible
    def _maybe_int(s):
        try:
            return int(s)
        except Exception:
            return s

    plot_csv_columns(
        args.csv,
        x_col=_maybe_int(args.x),
        y_col=_maybe_int(args.y),
        delimiter=args.sep,
        show=not args.no_show,
        save_path=args.save,
    )

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

    
    