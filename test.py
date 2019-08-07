#!/usr/bin/env python

import time

from ambient_api.ambientapi import AmbientAPI
from prometheus_client import Info, Gauge
from prometheus_client import start_http_server

api = AmbientAPI()
if not api.api_key:
    raise Exception("You must specify an API Key")
if not api.application_key:
    raise Exception("You must specify an Application Key")

#devices = api.get_devices()
#if len(devices) == 0:
#    raise Exception("No weather devices found on your account. Exiting.")

i = Info("ambient_weather_exporter", "Prometheus exporter for Ambient Weather personal weather station")
i.info({'version': '0'})

# {'dateutc': 1565188020000, 'tempinf': 77.7, 'humidityin': 54, 'baromrelin': 29.794, 'baromabsin': 29.103, 'tempf': 76.5, 'humidity': 60, 'winddir': 54, 'windspeedmph': 0, 'windgustmph': 0, 'maxdailygust': 1.1, 'hourlyrainin': 0, 'eventrainin': 0, 'dailyrainin': 0, 'weeklyrainin': 0.039, 'monthlyrainin': 0.15, 'totalrainin': 0.201, 'solarradiation': 48.56, 'uv': 0, 'feelsLike': 76.67, 'dewPoint': 61.56, 'lastRain': '2019-08-06T09:25:00.000Z', 'tz': 'America/Chicago', 'date': '2019-08-07T14:27:00.000Z'}

# {
# 'dateutc': 1565188020000,
# 'tempinf': 77.7,
# 'humidityin': 54,
# 'baromrelin': 29.794,
# 'baromabsin': 29.103,
# 'tempf': 76.5,
# 'humidity': 60,
# 'winddir': 54,
# 'windspeedmph': 0,
# 'windgustmph': 0,
# 'maxdailygust': 1.1,
# 'hourlyrainin': 0,
# 'eventrainin': 0,
# 'dailyrainin': 0,
# 'weeklyrainin': 0.039,
# 'monthlyrainin': 0.15,
# 'totalrainin': 0.201,
# 'solarradiation': 48.56,
# 'uv': 0,
# 'feelsLike': 76.67,
# 'dewPoint': 61.56,
# 'lastRain': '2019-08-06T09:25:00.000Z',
# 'tz': 'America/Chicago',
# 'date': '2019-08-07T14:27:00.000Z'}

indoor_temperature = Gauge("indoor_temperature", "Indoor Temperature in F")
outdoor_temperature = Gauge("outdoor_temperature", "Outdoor Temperature in F")
solar_radiation = Gauge("solar_radiation", "Solar Radiation (W/m2)")

start_http_server(8000)
while True:
    devices = api.get_devices()
    if len(devices) == 0:
        print("No devices found on Ambient Weather account.")
        indoor_temperature.set(None)
        outdoor_temperature.set(None)
        continue
    device = devices[0] # FIXME: handle multiple devices
    last_data = device.last_data
    print(device.info)
    print(device.mac_address)
    print(dir(device))
    print(last_data)
    indoor_temperature.set(last_data['tempinf'])
    outdoor_temperature.set(last_data['tempf'])
    solar_radiation.set(last_data['solarradiation'])
    print("sleeping 60");
    time.sleep(60)
