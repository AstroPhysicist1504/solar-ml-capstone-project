# ============================================================
# REPRESENTATIVE DAILY GHI PLOTS
# Delhi Solar Data — 2020
# ============================================================

# Import Pandas for handling the dataset
import pandas as pd

# Import Matplotlib for creating the plots
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

# Read the CSV file into a Pandas DataFrame.
# Change the filename if your CSV has a different name.

df = pd.read_csv("delhi_solar_weather.csv")


# ------------------------------------------------------------
# STEP 2: CONVERT THE TIMESTAMP
# ------------------------------------------------------------

# NASA POWER timestamps are in the format:
#
# YYYYMMDDHH
#
# Example:
# 2020011512
#
# means:
# 15 January 2020, 12:00
#
# We explicitly specify the format so Pandas interprets it
# correctly.

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)


# ------------------------------------------------------------
# STEP 3: CREATE A DATE COLUMN
# ------------------------------------------------------------

# We create a separate column containing only the date.
#
# For example:
#
# 2020-01-15 12:00:00
#
# becomes:
#
# 2020-01-15
#
# This makes it easier to select an entire day.

df["date"] = df["timestamp"].dt.date


# ------------------------------------------------------------
# STEP 4: DEFINE THE REPRESENTATIVE DAYS
# ------------------------------------------------------------

# These are the middle days of four representative months.
#
# January  → Winter
# April    → Pre-summer / summer transition
# July     → Monsoon
# October  → Post-monsoon / autumn
#
# We use these days to get an intuitive idea of how the
# daily GHI curve changes throughout the year.

representative_dates = [
    "2020-01-15",
    "2020-04-15",
    "2020-07-15",
    "2020-10-15"
]


# ------------------------------------------------------------
# STEP 5: CREATE THE PLOT
# ------------------------------------------------------------

# Create one figure for all four days.

plt.figure(figsize=(12, 6))


# ------------------------------------------------------------
# STEP 6: PLOT EACH REPRESENTATIVE DAY
# ------------------------------------------------------------

# Go through each date one by one.

for date in representative_dates:

    # Convert the date string into a date object.
    date_object = pd.to_datetime(date).date()

    # Select only the rows belonging to this particular day.

    day_data = df[df["date"] == date_object]

    # Extract the hour from the timestamp.
    #
    # This gives:
    #
    # 0, 1, 2, 3, ... 23
    #
    # which we will use on the x-axis.

    hours = day_data["timestamp"].dt.hour

    # Extract the GHI values for this day.

    ghi = day_data["ALLSKY_SFC_SW_DWN"]

    # Plot GHI against hour.

    plt.plot(
        hours,
        ghi,
        marker="o",
        label=date
    )


# ------------------------------------------------------------
# STEP 7: LABEL THE GRAPH
# ------------------------------------------------------------

# Label the x-axis.

plt.xlabel("Hour of day")


# Label the y-axis.

plt.ylabel("GHI (W/m²)")


# Give the graph a title.

plt.title("Representative Daily GHI Profiles — Delhi 2020")


# Set the x-axis to show every hour from 0 to 23.

plt.xticks(range(0, 24))


# Add a grid to make the values easier to read.

plt.grid(True)


# Add a legend so we know which curve corresponds to which
# date.

plt.legend(title="Date")


# Automatically adjust spacing so that labels don't overlap.

plt.tight_layout()


# Display the graph.

plt.show()