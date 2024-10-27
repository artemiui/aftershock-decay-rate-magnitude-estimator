import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def omori(t,k,c,p):
    return k / (t + c) ** p # formula of omori's law in python format

    """ 
    wherein k is the productivity constant of initial aftershock rate
    c is a time offset parameter to avoid singularities when t = 0
    p is the decay rate of aftershock frequency
    """

def omori_fit(aftershocks_dataframe, mainshocks):

    """
    the following fits omori's Law to aftershock data for each mainshock.
    
    required parameters:
    - aftershocks_df (pd.DataFrame): Aftershock data with mainshock IDs
    - mainshocks (pd.DataFrame): Mainshock data
    
    returns:
    - pd.DataFrame: Omori parameters (k, c, p) for each mainshock
    """

    aftershocks_dataframe['TimeSinceMainshock'] = aftershocks_dataframe.apply(
        lambda row: (row['Time'] - mainshocks.loc[mainshocks['EventID'] == row['MainshockID'], 'Time'].values[0]).days,
        axis = 1
    )

    omori_parameters = []
    for mainshock_id, group in aftershocks_dataframe.groupby('MainshockID'):
        time_since_mainshock = group['TimeSinceMainshock'].values
        aftershock_counts, bins = np.histogram(time_since_mainshock, bins=np.arange(1,8+1))
        bin_centers = (bins[:-1] + bins[1:]) / 2

        try:
            popt, _ = curve_fit(omori, bin_centers, aftershock_counts, bounds=(0. [np.inf, np.inf, 2]))
            omori_parameters.append({'MainshockID': mainshock_id, 'k': popt[0], 'c': popt[1], 'p': popt[2]})
        except RuntimeError:
            print(f"Curve fit failed for '{mainshock_id}'")
            omori_parameters.append({'MainshockID': mainshock_id, 'k': np.nan, 'c': np.nan, 'p': np.nan})

    return pd.Dataframe(omori_parameters)
