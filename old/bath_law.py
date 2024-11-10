import pandas as pd

""" 
    bath's law is the average difference between the 
    magnitude of a main shock and the magnitude 
    of its largest aftershock is independent of 
    the magnitude of the main shock (Bath (1965)

    in this case, we will use it for magnitude
    estimations.
    """

def bath(mainshock_data, aftershock_data):
    ma_difference = []

    for mainshock in mainshock_data.intertuples():
        aftershock_subset = aftershock_data[aftershock_data['time']>mainshock.time]
        if not aftershock_subset.empty:
            max_aftershock_mag = aftershock_subset['mag'].max()
            diff = mainshock.mag - max_aftershock_mag
            ma_difference.append(diff) 

    return pd.Series(ma_difference, name='Magnitude Difference')