import pandas as pd

def parameter_checker(chunk):
    required_columns = {
        'id':'object',
        'mag':'float64',
        'time':'datatime64[ns]',
        'latitude':'float64',
        'longitude':'float64'
    }

    for column, expected_type in required_columns.items():
        if column not in chunk.columns:
            raise ValueError(f"Missing required column: {column}")
        # Convert if not already correct type for time
        if column == 'time' and chunk[column].dtype != expected_type:
            chunk['time'] = pd.to_datetime(chunk['time'], errors='coerce')
        elif chunk[column].dtype != expected_type:
            chunk[column] = chunk[column].astype(expected_type)

def data_load(file_path): # insert csv file here
    chunk_size=1000  
    processed_data = []

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk['time'] = pd.to_datetime(chunk['time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        parameter_checker(chunk)
        chunk = chunk.dropna(subset=['time', 'latitude', 'longitude', 'mag'])
        processed_data.append(chunk['time','latitude','longitude','mag'])

    data = pd.concat(processed_data, ignore_index=True)
    return data