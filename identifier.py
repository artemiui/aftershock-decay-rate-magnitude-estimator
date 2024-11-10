# src/identifier.py
import pandas as pd
from utils import calculate_distance

class Mainshock:
    def __init__(self, id, latitude, longitude, magnitude, time):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.magnitude = magnitude
        self.time = pd.to_datetime(time)

def identify_aftershocks(mainshock, dataset, time_window=30, distance_threshold=100):
    """
    Identifies aftershocks based on time and distance criteria.
    """
    aftershock_df = dataset.copy()
    aftershock_df['time_diff'] = (aftershock_df['time'] - mainshock.time).dt.total_seconds() / (60 * 60 * 24)
    aftershock_df = aftershock_df[(aftershock_df['time_diff'] > 0) & (aftershock_df['time_diff'] <= time_window)]
    aftershock_df['distance'] = aftershock_df.apply(
        lambda row: calculate_distance(mainshock.latitude, mainshock.longitude, row['latitude'], row['longitude']),
        axis=1
    )
    return aftershock_df[aftershock_df['distance'] <= distance_threshold]
