# ============================================================
# PV POWER DERIVATION USING A PHYSICAL MODEL (pvlib)
# Delhi Solar Data — builds the PV_Power_kW target column
# ============================================================
#
# Pipeline:
#   NASA POWER (GHI, DNI, DHI, T2M, WS10M)
#        |
#        v
#   Solar position               (pvlib.location.Location.get_solarposition)
#        |
#        v
#   Plane-of-array irradiance    (pvlib.irradiance.get_total_irradiance)
#        |
#        v
#   Cell temperature             (pvlib.temperature.faiman)
#        |                       <- this is where wind speed and
#        |                          ambient temperature earn their place
#        v
#   DC power, temp-corrected     (pvlib.pvsystem.pvwatts_dc)
#        |
#        v
#   AC power after losses        (pvlib.pvsystem.pvwatts_ac)
#        |
#        v
#   PV_Power_kW  <-- your ML target column
#
# IMPORTANT: this script assumes your timestamps are UTC.
# NASA POWER's hourly API defaults to Local Solar Time (LST)
# unless the download request explicitly set time-standard=UTC.
# If your CSV was pulled without that parameter, re-pull it
# with time-standard=UTC before running this script, or the
# solar-position calculation below will be wrong.
#
# System assumptions (standard 5kW rooftop system, Delhi):
#   Latitude         : 28.6139 N
#   Longitude        : 77.2090 E
#   Altitude         : 216 m (approx. Delhi elevation)
#   Tilt             : 28 deg   (~ latitude, common fixed-tilt rule of thumb)
#   Azimuth          : 180 deg  (south-facing, Northern Hemisphere)
#   DC capacity      : 5000 W
#   Temp coefficient : -0.004 /degC (typical crystalline-silicon)
#   System losses    : 14% (PVWatts default: wiring, soiling, mismatch, availability)
#   Inverter eff.    : 96%
#
# These are documented design assumptions, not measured values —
# state them explicitly in your report as the hypothetical system
# spec, since no real 5kW installation exists to calibrate against.
# ============================================================

import pandas as pd
import pvlib


# ------------------------------------------------------------
# STEP 1: LOAD THE DATASET
# ------------------------------------------------------------

INPUT_CSV = "delhi_solar_weather.csv"

df = pd.read_csv(INPUT_CSV)

# NASA POWER timestamp format: YYYYMMDDHH
df["timestamp"] = pd.to_datetime(df["timestamp"].astype(str), format="%Y%m%d%H")

df = df.set_index("timestamp")

# pvlib needs a timezone-aware DatetimeIndex.
# Localize as UTC -- see the note at the top of this file.
df.index = df.index.tz_localize("UTC")


# ------------------------------------------------------------
# STEP 2: SYSTEM AND LOCATION PARAMETERS
# ------------------------------------------------------------

LATITUDE = 28.6139
LONGITUDE = 77.2090
ALTITUDE = 216  # meters

TILT = 28       # degrees from horizontal
AZIMUTH = 180   # degrees from north (south-facing)

DC_CAPACITY_W = 5000     # 5 kW system
GAMMA_PDC = -0.004       # temperature coefficient, per degC
SYSTEM_LOSSES = 0.14     # 14% (PVWatts default)
INVERTER_EFF = 0.96      # 96%

location = pvlib.location.Location(
    latitude=LATITUDE,
    longitude=LONGITUDE,
    altitude=ALTITUDE,
    tz="UTC",
)


# ------------------------------------------------------------
# STEP 3: SOLAR POSITION
# ------------------------------------------------------------

solar_position = location.get_solarposition(df.index)

df["solar_zenith"] = solar_position["apparent_zenith"]
df["solar_azimuth"] = solar_position["azimuth"]


# ------------------------------------------------------------
# STEP 4: PLANE-OF-ARRAY (POA) IRRADIANCE
# ------------------------------------------------------------
# Converts horizontal GHI/DNI/DHI into the irradiance actually
# striking a tilted panel at TILT/AZIMUTH.

poa = pvlib.irradiance.get_total_irradiance(
    surface_tilt=TILT,
    surface_azimuth=AZIMUTH,
    solar_zenith=df["solar_zenith"],
    solar_azimuth=df["solar_azimuth"],
    dni=df["ALLSKY_SFC_SW_DNI"],
    ghi=df["ALLSKY_SFC_SW_DWN"],
    dhi=df["ALLSKY_SFC_SW_DIFF"],
)

df["poa_global"] = poa["poa_global"]


# ------------------------------------------------------------
# STEP 5: CELL TEMPERATURE
# ------------------------------------------------------------
# Faiman's model uses ambient temperature and wind speed to
# estimate how much the module heats up above ambient under
# the given irradiance -- this is the physical mechanism that
# gives wind speed a real role in the pipeline.

df["cell_temperature"] = pvlib.temperature.faiman(
    poa_global=df["poa_global"],
    temp_air=df["T2M"],
    wind_speed=df["WS10M"],
)


# ------------------------------------------------------------
# STEP 6: DC POWER (TEMPERATURE-CORRECTED)
# ------------------------------------------------------------

df["dc_power_w"] = pvlib.pvsystem.pvwatts_dc(
    g_poa_effective=df["poa_global"],
    temp_cell=df["cell_temperature"],
    pdc0=DC_CAPACITY_W,
    gamma_pdc=GAMMA_PDC,
)


# ------------------------------------------------------------
# STEP 7: AC POWER (AFTER SYSTEM LOSSES + INVERTER)
# ------------------------------------------------------------

pdc0_derated = DC_CAPACITY_W * (1 - SYSTEM_LOSSES)
pdc_derated = df["dc_power_w"] * (1 - SYSTEM_LOSSES)

# NOTE: pvsystem.pvwatts_ac() was deprecated in pvlib 0.9 and
# removed in 0.10 -- the same PVWatts inverter model now lives
# in pvlib.inverter.pvwatts() instead.
df["ac_power_w"] = pvlib.inverter.pvwatts(
    pdc=pdc_derated,
    pdc0=pdc0_derated,
    eta_inv_nom=INVERTER_EFF,
)

# Final target column, in kW for readability.
df["PV_Power_kW"] = df["ac_power_w"] / 1000.0

# Guard against small negative values from nighttime edge effects
# in the irradiance/temperature models.
df["PV_Power_kW"] = df["PV_Power_kW"].clip(lower=0)


# ------------------------------------------------------------
# STEP 8: SANITY CHECKS
# ------------------------------------------------------------
# Compare these against the seasonal pattern you already found
# in your EDA (Apr/May/Jun highest, Jan/Nov/Dec lowest).

print("PV_Power_kW summary statistics:")
print(df["PV_Power_kW"].describe())

print("\nMax PV_Power_kW by month (should peak around Apr/May):")
print(df.groupby(df.index.month)["PV_Power_kW"].max())

print("\nMean PV_Power_kW at hour 0 UTC (should be at or near 0):")
print(df[df.index.hour == 0]["PV_Power_kW"].mean())

print("\nMean PV_Power_kW at the sunniest hour found (approx. local noon):")
peak_hour = df.groupby(df.index.hour)["PV_Power_kW"].mean().idxmax()
print(f"Hour {peak_hour} UTC -> mean PV_Power_kW = "
      f"{df[df.index.hour == peak_hour]['PV_Power_kW'].mean():.3f}")


# ------------------------------------------------------------
# STEP 9: SAVE THE RESULT
# ------------------------------------------------------------

OUTPUT_CSV = "delhi_solar_weather_with_pv_power.csv"
df.to_csv(OUTPUT_CSV)
print(f"\nSaved: {OUTPUT_CSV}")