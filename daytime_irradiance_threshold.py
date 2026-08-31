# ============================================================
# INVESTIGATING A DAYTIME IRRADIANCE THRESHOLD
# ============================================================

# Import Pandas for handling the dataset
import pandas as pd


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

# Read the Delhi solar-weather CSV file.
# Change the filename if your file has a different name.

df = pd.read_csv("delhi_solar_weather.csv")


# ------------------------------------------------------------
# STEP 2: CONVERT THE TIMESTAMP
# ------------------------------------------------------------

# NASA's timestamp is in the form:
#
# YYYYMMDDHH
#
# Example:
# 2020010107
#
# means:
# 2020 - year
# 01   - month
# 01   - day
# 07   - hour

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)


# ------------------------------------------------------------
# STEP 3: SELECT THE GHI COLUMN
# ------------------------------------------------------------

# ALLSKY_SFC_SW_DWN is the GHI value from NASA POWER.
#
# We store it in a shorter variable name because we'll be
# using it several times.

ghi = df["ALLSKY_SFC_SW_DWN"]


# ------------------------------------------------------------
# STEP 4: DEFINE CANDIDATE THRESHOLDS
# ------------------------------------------------------------

# These are NOT our final thresholds.
#
# We are simply testing several possible values to see how
# much of the dataset falls below each one.

thresholds = [
    0,
    10,
    25,
    50,
    75,
    100,
    150,
    200
]


# ------------------------------------------------------------
# STEP 5: CALCULATE THE NUMBER OF HOURS BELOW EACH THRESHOLD
# ------------------------------------------------------------

# Create an empty list.
#
# We'll put the results for each threshold into this list.

results = []


# Go through each threshold one at a time.

for threshold in thresholds:

    # Count how many observations have GHI less than or equal
    # to the current threshold.
    #
    # For example:
    #
    # ghi <= 50
    #
    # produces True/False values for every row.
    #
    # True  = GHI is <= 50
    # False = GHI is > 50
    #
    # .sum() counts the True values.

    hours_below = (ghi <= threshold).sum()


    # Calculate what percentage of all observations these
    # hours represent.

    percentage = (hours_below / len(ghi)) * 100


    # Store the results.

    results.append({
        "Threshold (W/m²)": threshold,
        "Hours <= threshold": hours_below,
        "Percentage (%)": percentage
    })


# ------------------------------------------------------------
# STEP 6: CONVERT RESULTS INTO A DATAFRAME
# ------------------------------------------------------------

# Turning our list into a DataFrame makes it easier to read.

threshold_table = pd.DataFrame(results)


# ------------------------------------------------------------
# STEP 7: DISPLAY THE RESULTS
# ------------------------------------------------------------

print("\nGHI THRESHOLD ANALYSIS")
print("----------------------")

print(threshold_table.to_string(index=False))