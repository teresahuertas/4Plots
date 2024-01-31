import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def read_gildas_fits(source, path):
    """
    Read the GILDAS-CLASS fits data files and return the data as a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the directory containing the GILDAS-CLASS fits data files.
    source : str
        Name of the source.

    Returns
    -------
    gildas_fit_data : dict
        Dictionary containing the GILDAS-CLASS fits data stored as pandas DataFrames for each source.
    """
    # Read the GILDAS-CLASS fits data files
    fit_files = {f'{source}_fit': f'{source}_rrls_fit.csv'}
    gildas_fit_data = {}

    for file_name in fit_files:
        full_path = f'{path}{fit_files[file_name]}'
        try:
            gildas_fit_data[file_name] = pd.read_csv(full_path, sep=',', header=0, usecols=range(0, 14))
        except FileNotFoundError:
            print(f"File '{fit_files[file_name]}' not found in path '{path}'")

    if f'{source}_fit' in gildas_fit_data:
        gildas_fit_data[f'{source}_fit']['Delta_n'] = (
            gildas_fit_data[f'{source}_fit']['Upper'] - gildas_fit_data[f'{source}_fit']['Lower']
        )
        gildas_fit_data[f'{source}_fit'] = gildas_fit_data[f'{source}_fit'].reset_index(drop=True)

    return gildas_fit_data