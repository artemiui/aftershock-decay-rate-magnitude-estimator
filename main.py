import pandas as pd
from preprocessing import load_data, check_columns
from identifier import Mainshock, identify_aftershocks
from bath import bath_law, plot_bath_law
from omori_fit import omori_fit, plot_omori

def main():
    # Load and preprocess the data
    dataset = load_data("C:/Users/Art/Desktop/aftershocks_sja/data/2022-2024.csv") # place path of usgs here
    check_columns(dataset)

    ri_mainshocks = [
        Mainshock(name = "Lubang, Occidental Mindoro", 
              latitude = "14.05",
              longitude = "119.11",
              mag = "6.4",
              time = "2022-03-14T05:05:48"),

        Mainshock(name = "Itbayat, Batanes", 
              latitude = "23.43",
              longitude = "121.57",
              mag = "6.7",
              time = "2022-03-23T01:41:00"),

        Mainshock(name = "Tayum, Abra", 
              latitude = "17.63",
              longitude = "120.63",
              mag = "7.0",
              time = "2022-07-27T08:43:24"),

        Mainshock(name = "Lagayan, Abra", 
              latitude = "17.77",
              longitude = "120.72",
              mag = "6.4",
              time = "2022-10-25T22:59:02"),

        Mainshock(name = "Balut Island, Davao Occidental", 
              latitude = "2.86",
              longitude = "127.04",
              mag = "7.0",
              time = "2023-01-18T14:06:10"),

        Mainshock(name = "Sarangani Island, Davao Occidental", 
              latitude = "3.18",
              longitude = "128.13",
              mag = "6.4",
              time = "2023-02-24T04:02:47"),

        Mainshock(name = "Sarangani Island, Davao Occidental", 
              latitude = "5.38",
              longitude = "125.24",
              mag = "6.8",
              time = "2023-11-17T16:14:08"),

        Mainshock(name = "Hinatuan, Surigao Del Sur", 
              latitude = "8.44",
              longitude = "126.59",
              mag = "7.4",
              time = "2023-12-02T22:37:05"),

        Mainshock(name = "Hinatuan, Surigao Del Sur", 
              latitude = "8.49",
              longitude = "126.95",
              mag = "6.6",
              time = "2023-12-03T18:35:50"),

        Mainshock(name = "Cagwait, Surigao Del Sur", 
              latitude = "8.96",
              longitude = "126.91",
              mag = "6.8",
              time = "2023-12-04T03:49:33")]


    for mainshock in ri_mainshocks:
        # Identify aftershocks for each mainshock
        aftershocks = identify_aftershocks(mainshock, dataset)

        if not aftershocks.empty:
            # Fit Omori's Law to aftershock data
            k, c, p = omori_fit(aftershocks)
            aftershock_times = (aftershocks['time'] - aftershocks['time'].min()).dt.total_seconds() / (60 * 60 * 24)
            omori_fit(aftershock_times, k, c, p)

            # Apply and plot Bath's Law
            magnitude_difference = bath_law(mainshock, aftershocks)
            plot_bath_law(mainshock, aftershocks)
        else:
            print(f"No aftershocks found for mainshock {mainshock.name}")

if __name__ == "__main__":
    main()

