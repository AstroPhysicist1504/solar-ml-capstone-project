# Plotting GHI v/s time to check the solar availability in Delhi for the year 2020 
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("delhi_solar_weather.csv")

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype(str),
    format="%Y%m%d%H"
)

plt.figure(figsize=(15, 5))
plt.plot(df["timestamp"], df["ALLSKY_SFC_SW_DWN"])
plt.xlabel("Time")
plt.ylabel("GHI (W/m²)")
plt.title("Delhi GHI — 2020")
plt.show()