import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.family'] = 'Times New Roman'

# Define Omori's Law function
def omori_law(t, k, c, p):
    """Omori's Law: number of aftershocks per day"""
    return k / (t + c) ** p

# Define Exponential Decay function
def exponential_decay(t, k, p):
    """Exponential decay function"""
    return k * np.exp(-p * t)

# MLE Fitting for Omori's Law with bounds, using custom initial guesses
def fit_omori_mle(aftershocks_per_day, days_since_mainshock, initial_k=50, initial_c=0.5, initial_p=1.1):
    """Fit Omori's Law using MLE with parameter bounds, allowing manual initial guesses."""
    if len(aftershocks_per_day) == 1:
        # If only one data point, return default values or fixed values
        return initial_k, initial_c, initial_p  # or set them to some known values

    initial_guesses = [initial_k, initial_c, initial_p]
    bounds = ([1, 0.1, 0.5], [1000, 2, 2])  # Tighter bounds for k, c, and p

    try:
        params, _ = curve_fit(omori_law, days_since_mainshock, aftershocks_per_day,
                              p0=initial_guesses, bounds=bounds, maxfev=10000)
        k, c, p = params
        return k, c, p
    except RuntimeError:
        print("Curve fitting failed for Omori's Law.")
        return np.nan, np.nan, np.nan

# Fit Exponential Decay with custom initial guesses
def fit_exponential(aftershocks_per_day, days_since_mainshock, initial_k=50, initial_p=0.1):
    """Fit exponential decay to the data, allowing manual initial guesses."""
    if len(aftershocks_per_day) == 1:
        # If only one data point, return default values or fixed values
        return initial_k, initial_p  # or set them to some known values

    initial_guesses = [initial_k, initial_p]  # Initial guesses for k and p
    try:
        params, _ = curve_fit(exponential_decay, days_since_mainshock, aftershocks_per_day, p0=initial_guesses, maxfev=10000)
        k, p = params
        return k, p
    except RuntimeError:
        print("Curve fitting failed for Exponential Decay.")
        return np.nan, np.nan

# Plot the raw data and fits
def plot_fits(days_since_mainshock, raw_data, k_omori, c_omori, p_omori, k_exp, p_exp):
    """Plot the observed aftershocks per day and fitted curves."""
    plt.figure(figsize=(12, 7))
    
    # Plot only non-zero aftershocks
    non_zero_days = days_since_mainshock[raw_data > 0]
    non_zero_aftershocks = raw_data[raw_data > 0]
    
    # If there is only one aftershock, plot it directly
    if len(non_zero_aftershocks) == 1:
        plt.scatter(non_zero_days, non_zero_aftershocks, label="Raw Aftershocks per Day", color="blue", alpha=0.6)
        plt.text(non_zero_days[0], non_zero_aftershocks[0], f'({non_zero_days[0]}, {non_zero_aftershocks[0]})', fontsize=12, ha='right')
    else:
        plt.scatter(non_zero_days, non_zero_aftershocks, label="Raw Aftershocks per Day", color="blue", alpha=0.6)

    # Plot Omori fit if valid
    if not np.isnan(k_omori):
        t = np.linspace(1, 200, 1000)  # Extend to 200 days or more
        omori_curve = omori_law(t, k_omori, c_omori, p_omori)
        plt.plot(t, omori_curve, label=f"Omori's Law Fit (k={k_omori:.2f}, c={c_omori:.2f}, p={p_omori:.2f})", color="red")

    # Plot Exponential fit if valid
    if not np.isnan(k_exp):
        t = np.linspace(1, 200, 1000)  # Extend to 200 days or more
        exp_curve = exponential_decay(t, k_exp, p_exp)
        plt.plot(t, exp_curve, label=f"Exponential Fit (k={k_exp:.2f}, p={p_exp:.2f})", color="green", linestyle='--')

    # Set the x-axis to logarithmic scale
    plt.xscale('log')

    # Set labels with larger font size
    plt.xlabel("Days Since Mainshock (Including Days with No Aftershocks)", fontsize=16)  # Set x-axis label font size to 16
    plt.ylabel("Number of Aftershocks per Day", fontsize=16)  # Set y-axis label font size to 16
    plt.legend(fontsize=14)  # Set legend font size to 14

    # Customize the grid lines
    plt.grid(visible=True, which='major', linestyle='--', linewidth=0.5, color='gray')  # Major grid lines
    plt.minorticks_on()  # Enable minor ticks
    plt.grid(visible=True, which='minor', linestyle=':', linewidth=0.5, color='lightgray')  # Minor grid lines

    plt.show()

# Load the aftershock data from "E:\quakequest_code\data\output_mainshocks"
file_path = r"E:\quakequest_code\data\output_mainshocks\mag6.4_Sarangani_Island,_Davao_Occidental_aftershocks.csv" #enter csv file path
aftershocks = pd.read_csv(file_path)

# Ensure the 'aftershock_time' column is in datetime format
aftershocks['aftershock_time'] = pd.to_datetime(aftershocks['aftershock_time'])
mainshock_time = aftershocks['aftershock_time'].min()
end_time = aftershocks['aftershock_time'].max()

# Create a complete date range from mainshock to end time
date_range = pd.date_range(start=mainshock_time, end=end_time, freq='D')

# Count aftershocks per day and reindex to fill gaps with zeros
aftershocks_per_day = aftershocks.groupby(aftershocks['aftershock_time'].dt.date).size()
aftershocks_per_day = aftershocks_per_day.reindex(date_range.date, fill_value=0)

#  Generate an array of days since the mainshock
days_since_mainshock = np.arange(len(aftershocks_per_day))

# Fit Omori's Law to the raw data, excluding zeros
non_zero_days = days_since_mainshock[aftershocks_per_day > 0]
non_zero_aftershocks = aftershocks_per_day[aftershocks_per_day > 0]

# Specify custom initial guesses for Omori's Law
initial_k_omori = 1
initial_c_omori = 0.5
initial_p_omori = 1.2

# Check if there are enough non-zero aftershocks for fitting
if len(non_zero_aftershocks) < 1:  # Need at least 2 points for fitting
    print("Not enough non-zero aftershocks found. Skipping Omori's Law fitting.")
    k_omori, c_omori, p_omori = np.nan, np.nan, np.nan
else:
    k_omori, c_omori, p_omori = fit_omori_mle(non_zero_aftershocks, non_zero_days, initial_k_omori, initial_c_omori, initial_p_omori)

# Fit Exponential Decay to the raw data, excluding zeros
initial_k_exp = 1
initial_p_exp = 0.15

# Check for non-zero aftershocks for Exponential fitting
if len(non_zero_aftershocks) < 1:  # Need at least 2 points for fitting
    print("Not enough non-zero aftershocks found. Skipping Exponential fitting.")
    k_exp, p_exp = np.nan, np.nan
else:
    k_exp, p_exp = fit_exponential(non_zero_aftershocks, non_zero_days, initial_k_exp, initial_p_exp)

# Plot the results
plot_fits(days_since_mainshock, aftershocks_per_day, k_omori, c_omori, p_omori, k_exp, p_exp)