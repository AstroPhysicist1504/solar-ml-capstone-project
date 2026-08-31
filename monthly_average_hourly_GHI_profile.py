# ============================================================
# PLOT 6: MONTHLY-AVERAGE HOURLY GHI PROFILES
# Delhi Solar Data — 2020
# ============================================================

# Import Pandas for data handling
import pandas as pd

# Import Matplotlib for plotting
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

# Read the CSV file.
# Change the filename if your CSV has a different name.

df = pd.read_csv("delhi_solar_weather.csv")


# ------------------------------------------------------------
# STEP 2: CONVERT TIMESTAMP
# ------------------------------------------------------------

# NASA POWER timestamp format:
#
# YYYYMMDDHH
#
# Example:
# 2020041512
#
# = 15 April 2020, 12:00

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)


# ------------------------------------------------------------
# STEP 3: EXTRACT MONTH AND HOUR
# ------------------------------------------------------------

# Extract the month number from the timestamp.
#
# January = 1
# February = 2
# ...
# December = 12

df["month"] = df["timestamp"].dt.month


# Extract the hour of the day.
#
# 00:00 → 0
# 01:00 → 1
# ...
# 23:00 → 23

df["hour"] = df["timestamp"].dt.hour


# ------------------------------------------------------------
# STEP 4: CALCULATE MONTHLY HOURLY AVERAGE
# ------------------------------------------------------------

# We group the data according to:
#
#     month + hour
#
# Then calculate the mean GHI for each group.
#
# For example:
#
# January + 12:00
#
# will contain the GHI values at 12:00 for ALL January days.
#
# Their average becomes the representative January 12:00 GHI.

monthly_hourly_ghi = (
    df.groupby(["month", "hour"])["ALLSKY_SFC_SW_DWN"]
    .mean()
)


# ------------------------------------------------------------
# STEP 5: CREATE THE PLOT
# ------------------------------------------------------------

# Create a large figure so all twelve curves can be seen
# clearly.

plt.figure(figsize=(14, 7))


# ------------------------------------------------------------
# STEP 6: PLOT EACH MONTH
# ------------------------------------------------------------

# Month names to make the legend easier to understand.

month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


# Loop through all twelve months.

for month in range(1, 13):

    # Select the hourly averages belonging to this month.

    month_data = monthly_hourly_ghi.loc[month]


    # Plot hour against average GHI.

    plt.plot(
        month_data.index,
        month_data.values,
        marker="o",
        label=month_names[month - 1]
    )


# ------------------------------------------------------------
# STEP 7: LABEL THE AXES
# ------------------------------------------------------------

# X-axis = hour of day

plt.xlabel("Hour of day")


# Y-axis = average GHI

plt.ylabel("Average GHI (W/m²)")


# ------------------------------------------------------------
# STEP 8: ADD TITLE
# ------------------------------------------------------------

plt.title(
    "Monthly-Average Hourly GHI Profiles — Delhi 2020"
)


# ------------------------------------------------------------
# STEP 9: FORMAT THE X-AXIS
# ------------------------------------------------------------

# Show every hour from 0 to 23.

plt.xticks(range(0, 24))


# ------------------------------------------------------------
# STEP 10: ADD GRID
# ------------------------------------------------------------

# Grid makes it easier to compare the curves.

plt.grid(True)


# ------------------------------------------------------------
# STEP 11: ADD LEGEND
# ------------------------------------------------------------

# Display the month names.

plt.legend(
    title="Month",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)


# ------------------------------------------------------------
# STEP 12: IMPROVE LAYOUT
# ------------------------------------------------------------

# Prevent the legend and labels from being cut off.

plt.tight_layout()


# ------------------------------------------------------------
# STEP 13: DISPLAY THE GRAPH
# ------------------------------------------------------------

plt.show()