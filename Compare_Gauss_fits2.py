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

    Usage
    -----
    >>> gildas_fit_data = read_gildas_fits(source, path)
    """
    # Read the GILDAS-CLASS fits data files
    fit_files = {f'{source}_fit': f'{source}_rrls_fit.csv'}
    gildas_fit_data = {}

    for file_name in fit_files:
        full_path = f'{path}{fit_files[file_name]}'
        try:
            gildas_fit_data[file_name] = pd.read_csv(full_path, sep=',', header=0, usecols=range(0, 14))
            print(f"File '{fit_files[file_name]}' read successfully")
        except FileNotFoundError:
            print(f"File '{fit_files[file_name]}' not found in path '{path}'")

    if f'{source}_fit' in gildas_fit_data:
        gildas_fit_data[f'{source}_fit']['Delta_n'] = (
            gildas_fit_data[f'{source}_fit']['Upper'] - gildas_fit_data[f'{source}_fit']['Lower']
        )
        gildas_fit_data[f'{source}_fit'] = gildas_fit_data[f'{source}_fit'].reset_index(drop=True)

    return gildas_fit_data


def apply_temperature_correction(telescope_data, source, element):
    """
    Applies temperature correction to the telescope data based on frequency ranges.

    Parameters
    ----------
    telescope_data (DataFrame): DataFrame containing the telescope data.
    source (str): Source name.
    element (list): List of element names.

    Returns
    -------
    Dictionary containing the corrected data for each element.

    Usage
    -----
    source_name = 'your_source'
    element_names = ['H', 'He', 'C', 'O']
    telescope_data = iram[source_name]  # or yebes[source_name]

    corrected_data = apply_temperature_correction(telescope_data, source_name, element_names)
    """

    corrected_data = {}

    try:
        # Determine telescope type based on frequency ranges
        if telescope_data['Freq[MHz]'].max() > 70000:
            telescope_type = 'IRAM-30m'
        elif 30000 <= telescope_data['Freq[MHz]'].max() <= 50000:
            telescope_type = 'Yebes-40m'
        else:
            raise ValueError("Unable to determine telescope type based on frequency.")

        if telescope_type == 'IRAM-30m':
            # Convert Tpeak data from Tmb to Ta
            TatoTmb = (
                1000 * (94 * (telescope_data['Freq[MHz]'] / 1000 / 211.024589551445843 + 1) +
                       (-94 - 0.102592852137351087 * (telescope_data['Freq[MHz]'] / 1000 - 211.024589551445843)) *
                       telescope_data['Freq[MHz]'] / 1000 / 211.024589551445843)
            )
            TatoTmb = TatoTmb / (
                    -2.556567478886569763E-04 * (telescope_data['Freq[MHz]'] / 1000) ** 2 -
                    7.226368939203042796E-02 * (telescope_data['Freq[MHz]'] / 1000) +
                    89.2508073876328893
            )
            telescope_data['Tpeak'] = telescope_data['Tpeak'] / TatoTmb
            TatomJy = (
                1000 * (5.760273113762687692E-05 * (telescope_data['Freq[MHz]'] / 1000) ** 2 -
                       5.015712414552293830E-03 * (telescope_data['Freq[MHz]'] / 1000) +
                       5.91822560841985812)
            )
            telescope_data['Tpeak'] = telescope_data['Tpeak'] * TatomJy

        elif telescope_type == 'Yebes-40m':
            # Convert Tpeak data from Tmb to Ta
            TatoTmb = (
                    1.4913789244107469 - 1.2925792303656232E-002 * (telescope_data['Freq[MHz]'] / 1000) +
                    5.0941757966556876E-004 * (telescope_data['Freq[MHz]'] / 1000) ** 2
            )
            TatoTmb = TatoTmb * 1000
            telescope_data['Tpeak'] = telescope_data['Tpeak'] / TatoTmb
            TatomJy = (
                    4.0660553594502913 - 6.6879469816527315E-002 * (telescope_data['Freq[MHz]'] / 1000) +
                    1.6408850177347977E-003 * (telescope_data['Freq[MHz]'] / 1000) ** 2
            )
            TatomJy = TatomJy * 1000
            telescope_data['Tpeak'] = telescope_data['Tpeak'] * TatomJy

        else:
            raise ValueError("Invalid telescope type. Supported types: 'IRAM-30m', 'Yebes-40m")

        # Classify the lines by species
        for i, elem in enumerate(element):
            corrected_data[f'{source}_{elem}'] = telescope_data[
                telescope_data['Species'].str.contains(rf'{elem}(?!I)')].reset_index(drop=True)

    except ZeroDivisionError:
        print(f'Error in {source} data: dividing by zero')

    return corrected_data