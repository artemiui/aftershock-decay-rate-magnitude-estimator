import pandas as pd
from datetime import timedelta
from utils import calculate_distance
from ri_data import ri_mainshocks  

usgs_file_path = r"E:\quakequest_code\data\usgs\2022-2024.csv"
output_file_path = r"E:\quakequest_code\data\output_mainshocks\compiled_mainshocks_aftershocks.csv"

def identify_mainshocks_aftershocks(usgs_data, ri_mainshocks, output_file_path, time_window_days=100, spatial_radius_deg=50, magnitude_threshold=0.5):
    mainshock_aftershock_data = []
    mainshock_name_tracker = {}

    print("Starting mainshock and aftershock identification using UPRI mainshocks and USGS data...")

    # Load USGS data 
    if isinstance(usgs_data, str):
        usgs_data = pd.read_csv(usgs_data)

    # Ensure consistent timezone-naive datetime format for USGS data
    usgs_data['time'] = pd.to_datetime(usgs_data['time'], errors='coerce').dt.tz_localize(None)

    # Keep only the relevant columns
    columns_to_keep = ['time', 'latitude', 'longitude', 'mag', 'place']
    usgs_data = usgs_data[columns_to_keep]

    # Ensure the 'mag' column is properly named for processing
    usgs_data.rename(columns={'mag': 'magnitude'}, inplace=True)

    # Sort USGS data by time
    usgs_data = usgs_data.sort_values(by='time').reset_index(drop=True)

    # Debug: Print the USGS data loaded
    print(f"Loaded USGS data:\n{usgs_data.head()}")

    # Process each UPRI mainshock instance
    for i, mainshock in enumerate(ri_mainshocks):
        mainshock_time = pd.to_datetime(mainshock.time).tz_localize(None)
        mainshock_lat = float(mainshock.latitude)
        mainshock_lon = float(mainshock.longitude)
        mainshock_mag = float(mainshock.mag)

        # Generate unique mainshock name if necessary (handle duplicate names with different magnitudes)
        if mainshock.name in mainshock_name_tracker:
            # Check if the current magnitude is the same as previously seen for this name
            if mainshock_mag == mainshock_name_tracker[mainshock.name]:
                unique_mainshock_name = mainshock.name
            else:
                # Append a number to the mainshock name if the magnitude is different
                unique_mainshock_name = f"{len(mainshock_name_tracker)}{mainshock.name}"
        else:
            unique_mainshock_name = mainshock.name

        # Track the mainshock name and its magnitude
        mainshock_name_tracker[mainshock.name] = mainshock_mag

        print(f"\nProcessing mainshock '{unique_mainshock_name}': time={mainshock_time}, magnitude={mainshock_mag}, location=({mainshock_lat}, {mainshock_lon})")

        # Define the time window for aftershock identification
        end_time = mainshock_time + timedelta(days=time_window_days)

        # Filter USGS data for potential aftershocks within the time window
        filtered_usgs_data = usgs_data[(usgs_data['time'] > mainshock_time) & (usgs_data['time'] <= end_time)]
        print(f"Filtered USGS data for mainshock '{unique_mainshock_name}':\n{filtered_usgs_data.to_string(index=False)}")  # Display entire filtered DataFrame for debugging

        if filtered_usgs_data.empty:
            print(f"No USGS events found within the time window for mainshock '{unique_mainshock_name}'.")
            continue

        # Identify aftershocks in filtered USGS data
        for _, aftershock in filtered_usgs_data.iterrows():
            aftershock_time = aftershock['time']
            aftershock_mag = aftershock['magnitude']

            spatial_dist = calculate_distance(mainshock_lat, mainshock_lon, aftershock['latitude'], aftershock['longitude'])
            if spatial_dist > spatial_radius_deg:
                continue

            # Magnitude check: aftershock magnitude must be lower than mainshock magnitude by the threshold
            if aftershock_mag < mainshock_mag - magnitude_threshold:
                mainshock_aftershock_data.append({
                    'mainshock_name': unique_mainshock_name,
                    'mainshock_time': mainshock_time,
                    'mainshock_magnitude': mainshock_mag,
                    'aftershock_time': aftershock_time,
                    'aftershock_magnitude': aftershock_mag,
                    'aftershock_place': aftershock['place'],
                    'aftershock_latitude': aftershock['latitude'],
                    'aftershock_longitude': aftershock['longitude']
                })
                print(f"  Found aftershock: time={aftershock_time}, magnitude={aftershock_mag}, location=({aftershock['latitude']}, {aftershock['longitude']}), place={aftershock['place']}")

    print("Mainshock and aftershock identification complete.")

    # Compile all aftershocks into a single DataFrame
    if mainshock_aftershock_data:
        export_df = pd.DataFrame(mainshock_aftershock_data)

        # Save the compiled DataFrame to a single CSV file
        try:
            export_df.to_csv(output_file_path, index=False)  # Save the DataFrame to CSV
            print(f"All aftershocks exported to {output_file_path}")
        except Exception as e:
            print(f"An error occurred while exporting data to {output_file_path}: {e}")
    else:
        print("No aftershocks identified. No CSV file created.")

# Call the function with the USGS data and UPRI mainshocks
identify_mainshocks_aftershocks(usgs_file_path, ri_mainshocks, output_file_path)
