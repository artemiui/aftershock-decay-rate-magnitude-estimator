import pandas as pd
from datetime import timedelta

# note: make an algorithm that converts all of your time to the same format as the ri researcher to make it more readable and for it to be easily manipulated

# since the data is not normalized in terms of magnitude, we first define a dictionary for conversion, and then a function that normalizes it

def identify_aftershocks(
    data,
    mainshock_magnitude_threshold = 5.0, # tentative value
    time_window = 3, # in days
    spatial_radius = 1.0 # circular radius in degrees latitude/longitude
    ):

    mainshocks = []
    aftershocks = []

    for i, event in data.iterows():
        if event['mag'] >= 5.0:
            mainshock = event
            mainshocks.append(mainshock)

            for j, potential_aftershock in data.iterrows():
                time_difference = (potential_aftershock['time'] - mainshock['time']).days
                if time_difference > 0 and time_difference <= time_window:
                    distance = ((event['latitude'] - potential_aftershock['latitude'])**2 +  # uses the traditional dist formula
                                (event['longitude'] - potential_aftershock['longitude'])**2)**0.5
                    if distance <= spatial_radius:
                        aftershocks.append(potential_aftershock)

    return pd.DataFrame(mainshocks), pd.DataFrame(aftershocks)