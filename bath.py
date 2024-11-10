# src/bath.py
import matplotlib.pyplot as plt

def bath_law(mainshock, aftershocks):
    """
    Calculates and visualizes Bath's Law, showing largest aftershock magnitude difference.
    """
    largest_aftershock = aftershocks['mag'].max()
    magnitude_difference = mainshock.magnitude - largest_aftershock
    print(f"Bath's Law Difference for Mainshock {mainshock.id}: {magnitude_difference:.2f}")
    return magnitude_difference

def plot_bath_law(mainshock, aftershocks):
    plt.scatter(mainshock.magnitude, aftershocks['mag'].max(), color='blue', label="Largest aftershock")
    plt.axhline(y=mainshock.magnitude - 1.2, color='red', linestyle='--', label="Bath's Law estimate")
    plt.xlabel("Mainshock Magnitude")
    plt.ylabel("Aftershock Magnitude")
    plt.legend()
    plt.show()
