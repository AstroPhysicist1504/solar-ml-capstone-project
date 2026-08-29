import requests
import pandas as pd

url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

params = {
    "parameters": ",".join([
        "ALLSKY_SFC_SW_DWN",
        "ALLSKY_SFC_SW_DNI",
        "ALLSKY_SFC_SW_DIFF",
        "T2M",
        "RH2M",
        "WS10M",
        "WD10M",
        "PS",
        "PRECTOTCORR"
    ]),
    "community": "RE",
    "longitude": 77.2090,
    "latitude": 28.6139,
    "start": "20200101",
    "end": "20201231",
    "format": "JSON"
}

response = requests.get(url, params=params)

print(response.status_code)

data = response.json()
parameters = data["properties"]["parameter"]

df = pd.DataFrame(parameters)

df.index.name = "timestamp"

df.to_csv("delhi_solar_weather.csv")

print(df.head())