# src/preprocessing.py
import pandas as pd

def load_data(file_path):
    """
    Load and preprocess earthquake data from a CSV file.
    """
    chunks = pd.read_csv(file_path, chunksize=1000)
    processed_data = []
    for chunk in chunks:
        # Convert time to datetime format
        chunk['time'] = pd.to_datetime(chunk['time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        processed_data.append(chunk[['id', 'latitude', 'longitude', 'mag', 'time']])
    return pd.concat(processed_data)

def check_columns(data):
    """
    Ensure required columns are present in data.
    """
    required_columns = {'id', 'latitude', 'longitude', 'mag', 'time'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Data must contain columns: {required_columns}")
