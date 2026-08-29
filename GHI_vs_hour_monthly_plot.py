"""
GHI vs Hour-of-Day plots (one subplot per month)
=================================================

WHAT THIS SCRIPT DOES:
  1. Reads a CSV file containing GHI (Global Horizontal Irradiance) data,
     where each row has a timestamp in YYYYMMDDHH format and a GHI value.
  2. Extracts the "month" and "hour" from each timestamp.
  3. For each month, plots GHI against hour-of-day (0-23).
  4. Arranges all 12 monthly plots in a 3x4 (or 4x3) grid in a single figure.

EXPECTED INPUT FORMAT (CSV):
    timestamp,GHI
    2023010100,0
    2023010101,0
    2023010112,540
    ...
  - "timestamp" column: YYYYMMDDHH (e.g. 2023010112 = Jan 1, 2023, 12:00)
  - "GHI" column: numeric irradiance value (W/m^2)

  If your column names are different, just change COL_TIMESTAMP and
  COL_GHI below to match your file.
"""

import pandas as pd              # for reading and manipulating tabular data
import matplotlib.pyplot as plt  # for plotting
import calendar                  # to convert month numbers (1-12) to names (Jan, Feb, ...)

# ----------------------------------------------------------------------
# 1. CONFIGURATION - change these to match your file
# ----------------------------------------------------------------------
CSV_PATH = "delhi_solar_weather.csv"     # path to your input CSV file
COL_TIMESTAMP = "timestamp"   # name of the timestamp column (YYYYMMDDHH)
COL_GHI = "ALLSKY_SFC_SW_DWN"               # name of the GHI value column

# ----------------------------------------------------------------------
# 2. LOAD THE DATA
# ----------------------------------------------------------------------
# dtype=str keeps the timestamp as text (e.g. "2023010112") instead of
# letting pandas convert it to a number and potentially drop leading digits.
df = pd.read_csv(CSV_PATH, dtype={COL_TIMESTAMP: str})

# ----------------------------------------------------------------------
# 3. PARSE THE TIMESTAMP INTO A REAL DATETIME OBJECT
# ----------------------------------------------------------------------
# format="%Y%m%d%H" tells pandas exactly how to interpret the YYYYMMDDHH
# string: 4-digit year, 2-digit month, 2-digit day, 2-digit hour.
df["datetime"] = pd.to_datetime(df[COL_TIMESTAMP], format="%Y%m%d%H")

# ----------------------------------------------------------------------
# 4. EXTRACT MONTH (1-12) AND HOUR (0-23) AS SEPARATE COLUMNS
# ----------------------------------------------------------------------
# These come for free once we have a proper datetime column -- pandas'
# .dt accessor lets us pull out any date/time component we need.
df["month"] = df["datetime"].dt.month
df["hour"] = df["datetime"].dt.hour

# ----------------------------------------------------------------------
# 5. SET UP A 3x4 GRID OF SUBPLOTS (12 months = 12 axes)
# ----------------------------------------------------------------------
# nrows=3, ncols=4 gives us 12 small plots arranged in 3 rows of 4.
# figsize controls the overall figure size in inches (width, height).
# sharex/sharey make all subplots use the same x and y axis ranges,
# which makes it easy to visually compare GHI patterns across months.
fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(18, 10),
                          sharex=True, sharey=True)

# axes is a 3x4 2D array of subplot objects; .flatten() turns it into a
# simple 1D list of 12 axes so we can loop over them with a single index.
axes = axes.flatten()

# ----------------------------------------------------------------------
# 6. LOOP OVER EACH MONTH AND PLOT GHI vs HOUR ON ITS OWN SUBPLOT
# ----------------------------------------------------------------------
for month_num in range(1, 13):                 # month_num goes 1 -> 12
    ax = axes[month_num - 1]                    # pick the subplot for this month

    # Filter the dataframe to keep only rows belonging to this month.
    month_data = df[df["month"] == month_num]

    # Group by hour and average the GHI for that hour across all days
    # in the month. This gives a smooth "typical day" profile instead
    # of an overlapping scatter of every single day's data.
    hourly_avg = month_data.groupby("hour")[COL_GHI].mean()

    # Plot the averaged hourly profile as a line with markers at each hour.
    ax.plot(hourly_avg.index, hourly_avg.values,
            marker="o", markersize=3, linewidth=1.5, color="tab:orange")

    # OPTIONAL: also show the raw scattered data points behind the average
    # line, so you can see the day-to-day spread. Comment out if too busy.
    ax.scatter(month_data["hour"], month_data[COL_GHI],
               s=5, alpha=0.15, color="gray")

    # calendar.month_name[month_num] converts 1 -> "January", 2 -> "February", etc.
    ax.set_title(calendar.month_name[month_num])

    ax.set_xticks(range(0, 24, 3))   # tick marks every 3 hours: 0,3,6,...,21
    ax.grid(True, alpha=0.3)         # light gridlines for readability

# ----------------------------------------------------------------------
# 7. ADD SHARED AXIS LABELS AND AN OVERALL TITLE
# ----------------------------------------------------------------------
# fig.text places text relative to the whole figure (0-1 coordinates)
# instead of a single subplot -- useful for one label shared by all plots.
fig.text(0.5, 0.04, "Hour of Day", ha="center", fontsize=12)
fig.text(0.08, 0.5, "GHI (W/m^2)", va="center", rotation="vertical", fontsize=12)
fig.suptitle("Average Hourly GHI Profile by Month", fontsize=16, y=0.98)

# ----------------------------------------------------------------------
# 8. LAYOUT AND SAVE / SHOW
# ----------------------------------------------------------------------
# rect leaves margin at the edges so the shared labels/title above don't
# get clipped by tight_layout's automatic spacing adjustment.
plt.tight_layout(rect=[0.09, 0.06, 1, 0.95])

# Save a high-resolution copy to disk...
plt.savefig("ghi_hourly_by_month.png", dpi=200)

# ...and also display it interactively if you're running this in an
# environment with a display (e.g. Jupyter, or a local Python session).
plt.show()