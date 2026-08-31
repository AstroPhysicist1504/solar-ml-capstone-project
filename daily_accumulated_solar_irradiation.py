# ============================================================
# PLOT 3: DAILY SOLAR IRRADIATION
# ============================================================

# Import Pandas for handling the dataset
import pandas as pd

# Import Matplotlib for plotting
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

# Read the CSV file into a Pandas DataFrame.
# Change the filename if your CSV has a different name.
df = pd.read_csv("delhi_solar_weather.csv")


# ------------------------------------------------------------
# STEP 2: CONVERT TIMESTAMP TO DATETIME
# ------------------------------------------------------------

# NASA POWER represents the timestamp as:
#
# YYYYMMDDHH
#
# For example:
#
# 2020010100 = 1 January 2020, 00:00
#
# We explicitly tell Pandas the format so that it does not
# misinterpret the timestamp.

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)


# ------------------------------------------------------------
# STEP 3: MAKE TIMESTAMP THE INDEX
# ------------------------------------------------------------

# A time-series dataset is easier to work with when the
# timestamp is the DataFrame index.

df = df.set_index("timestamp")


# ------------------------------------------------------------
# STEP 4: CALCULATE DAILY IRRADIATION
# ------------------------------------------------------------

# Our GHI values are hourly values in W/m².
#
# Since each value represents approximately one hour,
# summing the 24 hourly values gives:
#
#       W/m² × hour
#
# which is numerically equivalent to:
#
#       Wh/m²
#
# Therefore, summing the hourly GHI values for each day
# gives us an approximate daily irradiation value.

daily_irradiation = df["ALLSKY_SFC_SW_DWN"].resample("D").sum()


# ------------------------------------------------------------
# STEP 5: PLOT THE RESULT
# ------------------------------------------------------------

# Create a figure.
# figsize controls the width and height of the plot.

plt.figure(figsize=(15, 5))


# Plot daily irradiation against the date.

plt.plot(
    daily_irradiation.index,
    daily_irradiation
)


# Give the x-axis a descriptive label.

plt.xlabel("Date")


# Give the y-axis a descriptive label.
# The unit is Wh/m²/day.

plt.ylabel("Daily irradiation (Wh/m²/day)")


# Give the graph a title.

plt.title("Delhi Daily Solar Irradiation — 2020")


# Display the plot.

plt.show()