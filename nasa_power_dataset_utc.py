# ============================================================
# NASA POWER API DOWNLOAD SCRIPT
# Delhi Solar + Weather Data — UTC time standard
# ============================================================
#
# Standardizes the data pull to explicitly request UTC
# timestamps (time-standard=UTC), so it lines up correctly
# with the pvlib solar-position calculations used in
# derive_pv_power.py.
#
# NASA POWER's hourly API caps each request at roughly one
# year of data, so this script loops year by year and
# concatenates the results.
#
# Parameters requested (11 total, well under the 15-parameter
# limit for the hourly API):
#
#   ALLSKY_SFC_SW_DWN   -> GHI  (all-sky global horizontal irradiance)
#   ALLSKY_SFC_SW_DNI   -> DNI  (direct normal irradiance)
#   ALLSKY_SFC_SW_DIFF  -> DHI  (diffuse horizontal irradiance)
#   CLRSKY_SFC_SW_DWN   -> Clear-sky GHI (for clear-sky index)
#   T2M                 -> Temperature at 2m
#   RH2M                -> Relative humidity at 2m
#   WS10M               -> Wind speed at 10m
#   WD10M               -> Wind direction at 10m
#   PS                  -> Surface pressure
#   PRECTOTCORR         -> Precipitation (bias-corrected)
#   CLOUD_AMT           -> Cloud amount
# ============================================================

import time
import requests
import pandas as pd

# ------------------------------------------------------------
# STEP 1: LOCATION AND DATE RANGE
# ------------------------------------------------------------

LATITUDE = 28.6139
LONGITUDE = 77.2090

START_YEAR = 2013
END_YEAR = 2017   # inclusive -- adjust for how many years you want

PARAMETERS = [
    "ALLSKY_SFC_SW_DWN",
    "ALLSKY_SFC_SW_DNI",
    "ALLSKY_SFC_SW_DIFF",
    "CLRSKY_SFC_SW_DWN",
    "T2M",
    "RH2M",
    "WS10M",
    "WD10M",
    "PS",
    "PRECTOTCORR",
    "CLOUD_AMT",
]

BASE_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point"


# ------------------------------------------------------------
# STEP 2: DOWNLOAD ONE YEAR AT A TIME
# ------------------------------------------------------------

def fetch_year(year: int) -> pd.DataFrame:
    """
    Fetches one calendar year of hourly NASA POWER data
    for the given location, explicitly in UTC.
    """

    params = {
        "parameters": ",".join(PARAMETERS),
        "community": "RE",           # Renewable Energy community
        "longitude": LONGITUDE,
        "latitude": LATITUDE,
        "start": f"{year}0101",
        "end": f"{year}1231",
        "format": "JSON",
        "time-standard": "UTC",      # <-- the standardization fix
    }

    response = requests.get(BASE_URL, params=params, timeout=120)
    response.raise_for_status()

    data = response.json()
    parameter_data = data["properties"]["parameter"]

    # Each parameter is a dict of {timestamp_str: value}.
    # timestamp_str is in YYYYMMDDHH format, same as your
    # existing CSV, so downstream code doesn't need to change.
    year_df = pd.DataFrame(parameter_data)
    year_df.index.name = "timestamp"

    return year_df


# ------------------------------------------------------------
# STEP 3: LOOP OVER ALL REQUESTED YEARS
# ------------------------------------------------------------

all_years = []

for year in range(START_YEAR, END_YEAR + 1):
    print(f"Fetching {year}...")
    year_df = fetch_year(year)
    all_years.append(year_df)

    # Be polite to the API between requests.
    time.sleep(1)

df = pd.concat(all_years)
df = df.reset_index()


# ------------------------------------------------------------
# STEP 4: BASIC CLEANUP
# ------------------------------------------------------------

# NASA POWER uses -999 as a missing-value sentinel.
df = df.replace(-999, pd.NA)

# Sort chronologically and drop any accidental duplicate
# timestamps from overlapping year boundaries.
df["timestamp"] = df["timestamp"].astype(str)
df = df.sort_values("timestamp").drop_duplicates(subset="timestamp")


# ------------------------------------------------------------
# STEP 5: SAVE THE RESULT
# ------------------------------------------------------------

OUTPUT_CSV = "delhi_solar_weather_utc_2013_2017.csv"
df.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved {len(df)} rows spanning {START_YEAR}-{END_YEAR} to {OUTPUT_CSV}")
print(f"\nMissing values per column:")
print(df.isna().sum())