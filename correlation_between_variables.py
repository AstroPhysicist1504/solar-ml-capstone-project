# ============================================================
# PLOT 5: CORRELATION MATRIX
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
# STEP 2: SELECT THE VARIABLES
# ------------------------------------------------------------

# We don't need the timestamp for calculating numerical
# correlations.
#
# Therefore, we select only the numerical weather/solar
# variables.

variables = [
    "ALLSKY_SFC_SW_DWN",
    "ALLSKY_SFC_SW_DNI",
    "ALLSKY_SFC_SW_DIFF",
    "T2M",
    "RH2M",
    "WS10M",
    "WD10M",
    "PS",
    "PRECTOTCORR"
]


# Create a new DataFrame containing only these variables.

corr_data = df[variables]


# ------------------------------------------------------------
# STEP 3: CALCULATE CORRELATION
# ------------------------------------------------------------

# Pandas' corr() calculates the Pearson correlation
# coefficient between every pair of variables.
#
# The resulting values range from:
#
#       -1  → strong negative relationship
#        0  → little/no linear relationship
#       +1  → strong positive relationship

correlation_matrix = corr_data.corr()


# ------------------------------------------------------------
# STEP 4: DISPLAY THE CORRELATION VALUES
# ------------------------------------------------------------

# Print the matrix so that we can see the actual numerical
# correlation coefficients.

print(correlation_matrix)


# ------------------------------------------------------------
# STEP 5: CREATE A VISUAL REPRESENTATION
# ------------------------------------------------------------

plt.figure(figsize=(10, 8))


# imshow() converts the correlation matrix into a visual
# grid.
#
# Each cell represents the correlation between two variables.

plt.imshow(
    correlation_matrix,
    aspect="auto"
)


# ------------------------------------------------------------
# STEP 6: ADD VARIABLE NAMES TO THE AXES
# ------------------------------------------------------------

# Create positions for the variables on the x-axis and
# y-axis.

plt.xticks(
    range(len(variables)),
    variables,
    rotation=90
)

plt.yticks(
    range(len(variables)),
    variables
)


# ------------------------------------------------------------
# STEP 7: ADD A COLORBAR
# ------------------------------------------------------------

# The colorbar tells us what the visual scale represents.

plt.colorbar(
    label="Correlation coefficient"
)


# ------------------------------------------------------------
# STEP 8: ADD A TITLE
# ------------------------------------------------------------

plt.title("Correlation Matrix — Delhi Solar/Weather Data")


# Adjust the layout so that the long variable names don't
# overlap unnecessarily.

plt.tight_layout()


# Display the plot.

plt.show()