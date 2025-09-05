import pandas as pd
import numpy as np
import os

# Input file
INPUT_FILE = "stations_group_1986.csv"

# Output files
AVG_TEMP_FILE = "average_temp.txt"
TEMP_RANGE_FILE = "largest_temp_range_station.txt"
STABILITY_FILE = "temperature_stability_stations.txt"

def get_season_from_month(month: int) -> str:
    """Australian seasons."""
    if month in (12, 1, 2):
        return "Summer"
    elif month in (3, 4, 5):
        return "Autumn"
    elif month in (6, 7, 8):
        return "Winter"
    else:
        return "Spring"

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare DataFrame for analysis from monthly data format."""
    
    # Keep only needed columns
    id_col = "STATION_NAME" if "STATION_NAME" in df.columns else "STN_ID"
    month_cols = [c for c in df.columns if c not in ["STATION_NAME", "STN_ID", "LAT", "LON"]]

    # Convert wide (months as columns) -> long format
    df_long = df.melt(id_vars=[id_col], value_vars=month_cols,
                      var_name="MonthName", value_name="MeanTemp")
    df_long.rename(columns={id_col: "Station"}, inplace=True)

    # Map month names to numbers
    month_map = {m: i for i, m in enumerate(
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"], 1)}
    df_long["Month"] = df_long["MonthName"].map(month_map)

    # Assign Australian season
    df_long["Season"] = df_long["Month"].apply(get_season_from_month)

    # Ensure numeric temperatures
    df_long["MeanTemp"] = pd.to_numeric(df_long["MeanTemp"], errors="coerce")

    # Drop missing values
    df_long = df_long.dropna(subset=["MeanTemp"])
    return df_long


def seasonal_average(df: pd.DataFrame, out_file: str):
    """Compute average temperature per season."""
    seasonal = df.groupby("Season")["MeanTemp"].mean()
    order = ["Summer", "Autumn", "Winter", "Spring"]
    with open(out_file, "w") as f:
        for s in order:
            if s in seasonal:
                f.write(f"{s}: {seasonal[s]:.1f}°C\n")
            else:
                f.write(f"{s}: No data\n")


def temperature_range(df: pd.DataFrame, out_file: str):
    """Compute largest temperature range across stations (based on monthly mean temps)."""
    station_max = df.groupby("Station")["MeanTemp"].max()
    station_min = df.groupby("Station")["MeanTemp"].min()
    ranges = station_max - station_min
    max_range = ranges.max()
    winners = ranges[ranges == max_range].index.tolist()
    with open(out_file, "w") as f:
        for st in winners:
            f.write(f"Station {st}: Range {max_range:.1f}°C "
                    f"(Max: {station_max[st]:.1f}, Min: {station_min[st]:.1f})\n")


def temperature_stability(df: pd.DataFrame, out_file: str):
    """Find most stable and most variable stations (std dev of monthly means)."""
    std_devs = df.groupby("Station")["MeanTemp"].std()
    if std_devs.empty:
        with open(out_file, "w") as f:
            f.write("No station stddev data available\n")
        return
    min_std = std_devs.min()
    max_std = std_devs.max()
    most_stable = std_devs[std_devs == min_std].index.tolist()
    most_variable = std_devs[std_devs == max_std].index.tolist()
    with open(out_file, "w") as f:
        f.write("Most Stable:\n")
        for st in most_stable:
            f.write(f"{st}: StdDev {min_std:.1f}°C\n")
        f.write("\nMost Variable:\n")
        for st in most_variable:
            f.write(f"{st}: StdDev {max_std:.1f}°C\n")

def main():
    df_raw = pd.read_csv(INPUT_FILE)
    df = prepare_dataframe(df_raw)

    seasonal_average(df, AVG_TEMP_FILE)
    temperature_range(df, TEMP_RANGE_FILE)
    temperature_stability(df, STABILITY_FILE)

    print("Analysis complete. Results written to text files.")

if __name__ == "__main__":
    main()
