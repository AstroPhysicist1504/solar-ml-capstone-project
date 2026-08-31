# ============================================================
# PLOT 4: DISTRIBUTION OF GHI
# ============================================================

# Import Pandas
import pandas as pd

# Import Matplotlib
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

df = pd.read_csv("delhi_solar_weather.csv")


# ------------------------------------------------------------
# STEP 2: CONVERT TIMESTAMP
# ------------------------------------------------------------

# Convert NASA's YYYYMMDDHH timestamp into a proper
# datetime object.

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)


# ------------------------------------------------------------
# STEP 3: EXTRACT THE GHI COLUMN
# ------------------------------------------------------------

# Select the GHI column from our DataFrame.

ghi = df["ALLSKY_SFC_SW_DWN"]


# ------------------------------------------------------------
# STEP 4: CREATE THE HISTOGRAM
# ------------------------------------------------------------

# Create the figure.

plt.figure(figsize=(10, 6))


# Create a histogram.
#
# bins=50 means that the range of GHI values will be divided
# into 50 intervals (bins).
#
# The height of each bar represents how many observations
# fall into that GHI range.

plt.hist(
    ghi,
    bins=50
)


# ------------------------------------------------------------
# STEP 5: LABEL THE GRAPH
# ------------------------------------------------------------

plt.xlabel("GHI (W/m²)")

plt.ylabel("Number of hourly observations")

plt.title("Distribution of Delhi GHI — 2020")


# Display the graph.

plt.show()