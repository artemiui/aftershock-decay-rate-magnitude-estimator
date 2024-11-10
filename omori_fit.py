# src/omori.py
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def omori_law(t, k, c, p):
    return k / (t + c) ** p

def omori_fit(aftershocks):
    """
    Fits Omori's Law to aftershock data and returns k, c, and p.
    """
    aftershock_times = (aftershocks['time'] - aftershocks['time'].min()).dt.total_seconds() / (60 * 60 * 24)
    try:
        params, _ = curve_fit(omori_law, aftershock_times, np.arange(1, len(aftershock_times) + 1), maxfev=5000)
        k, c, p = params
    except RuntimeError:
        print("Curve fitting failed for Omori's Law.")
        k, c, p = np.nan, np.nan, np.nan
    return k, c, p

def plot_omori(aftershock_times, k, c, p):
    t = np.linspace(0, aftershock_times.max(), 100)
    plt.scatter(aftershock_times, np.arange(1, len(aftershock_times) + 1), label="Observed aftershocks")
    plt.plot(t, omori_law(t, k, c, p), label=f"Omori fit (k={k:.2f}, c={c:.2f}, p={p:.2f})", color="red")
    plt.xlabel("Time since mainshock (days)")
    plt.ylabel("Cumulative aftershocks")
    plt.legend()
    plt.show()
