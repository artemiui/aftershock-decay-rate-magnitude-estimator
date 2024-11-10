from data_preprocessing import data_load, parameter_checker
from identifier_algorithm import identify_aftershocks
from omori_fit import omori
from bath_law import bath
import pandas as pd

file_path = 'data/query_1990-2024.csv' # placeholder, add PATH here.
data = data_load(file_path)

try:
    parameter_checker(data)
except ValueError as e:
    print(f"Data parameter check failed: {e}")
    exit(1)

mainshocks, aftershocks = identify_aftershocks(data)

for mainshock in mainshocks.itertuples():
    mainshock_time = mainshock.time
    aftershock_subset = aftershocks[aftershocks['time'] > mainshock_time]

    if not aftershock_subset.empty:
        k, c, p = omori(aftershock_subset, mainshock_time)
        print(f"Mainshock at {mainshock_time} - Omori parameters: k={k}, c={c}, p={p}")

bath_results = bath(mainshocks, aftershocks)
print("Bath's Law outcome: ", bath_results)

