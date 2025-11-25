import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set font style and size globally for the entire plot
plt.rcParams['font.family'] = 'Times New Roman'  
plt.rcParams['font.size'] = 16  
plt.rcParams['legend.fontsize'] = 14  

# Load the aftershock data from "E:\quakequest_code\data\output_mainshocks"
file_path = r"E:\quakequest_code\data\output_mainshocks\compiled_mainshocks_aftershocks.csv"  
data = pd.read_csv(file_path)

# Group data by each mainshock name and find the largest aftershock magnitude for each mainshock
largest_aftershocks = data.groupby('mainshock_name').apply(
    lambda group: group.loc[group['aftershock_magnitude'].idxmax()]
)

# Extract mainshock magnitudes and corresponding largest aftershock magnitudes
mainshocks = largest_aftershocks['mainshock_magnitude'].values
largest_aftershock_magnitudes = largest_aftershocks['aftershock_magnitude'].values

# Print the list of largest aftershock magnitudes per mainshock
print("Largest Aftershock Magnitudes per Mainshock:")
for mainshock_name, aftershock_magnitude in zip(largest_aftershocks.index, largest_aftershock_magnitudes):
    print(f"{mainshock_name}: {aftershock_magnitude}")

# Calculate the magnitude differences
magnitude_differences = mainshocks - largest_aftershock_magnitudes

# Calculate the observed mean magnitude difference
observed_mean_difference = np.mean(magnitude_differences)

# Set the fixed magnitude difference for Bath's Law
fixed_difference = 1.1

# Plotting the Bath's Law scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(mainshocks, largest_aftershock_magnitudes, color="blue", label="Mainshock-Aftershock Pairs")

# Plot Bath's Law reference line with the fixed magnitude difference of 1.1
plt.plot(mainshocks, mainshocks - fixed_difference, color="red", linestyle="--", label=f"Bath's Law (Fixed difference = {fixed_difference})")

# Plot a reference line with the observed mean magnitude difference
plt.plot(mainshocks, mainshocks - observed_mean_difference, color="green", linestyle="--", label=f"Observed Mean difference = {observed_mean_difference:.2f}")

# Set labels, title, legend, and grid
plt.xlabel("Mainshock Magnitude", fontsize=16)  # Set x-axis font size to 16
plt.ylabel("Largest Aftershock Magnitude", fontsize=16)  # Set y-axis font size to 16
plt.title("Bath's Law: Mainshock vs. Largest Aftershock Magnitude")
plt.legend()
plt.grid(True)
plt.show()

# Plotting the histogram of magnitude differences
plt.figure(figsize=(8, 5))
plt.hist(magnitude_differences, bins=10, color='purple', alpha=0.7, label="Magnitude Differences")
plt.axvline(fixed_difference, color='red', linestyle='--', label=f"Fixed Difference = {fixed_difference}")
plt.axvline(observed_mean_difference, color='green', linestyle='--', label=f"Observed Mean Difference = {observed_mean_difference:.2f}")

# Set labels, title, legend, and grid for histogram
plt.xlabel("Magnitude Difference (Mainshock - Aftershock)", fontsize=16)  # Set x-axis font size to 16
plt.ylabel("Frequency", fontsize=16)  # Set y-axis font size to 16
plt.title("Distribution of Mainshock vs. Largest Aftershock Magnitude Differences")
plt.legend()
plt.grid(True)
plt.show()