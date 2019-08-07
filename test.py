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

def new_gauge(ambient_name, prom_name, description):
    gauge = Gauge(prom_name, description)
    gauge._ambient_name = ambient_name
    return gauge

# Fields left to handle:
# dateutc
# lastRain
# date

gauges = {
    new_gauge("tempinf", "indoor_temperature", "Indoor Temperature (Degrees F)"), # FIXME: what if i change my prefs to C? Does it export in C?
    new_gauge("humidityin", "indoor_humidity", "Indoor Relative Humidity (RH%)"),
    new_gauge("baromrelin", "baromrelin", "Barometer FIXME 1"),
    new_gauge("baromabsin", "baromabsin", "Barometer FIXME 2"),
    new_gauge("tempf", "outdoor_temperature", "Outdoor Temperature (Degrees F)"),
    new_gauge("humidity", "outdoor_humidity", "Outdoor Relative Humidity (RH%)"),
    new_gauge("winddir", "wind_direction", "Wind Direction (0-359 degrees)"),
    new_gauge("windspeedmph", "wind_speed", "Wind Speed (MPH)"), # FIXME: what if i change my prefs to m/s?
    new_gauge("windgustmph", "wind_gust", "Wind Gust (MPH)"),
    new_gauge("maxdailygust", "wind_gust_daily_max", "Maximum Daily Wind Gust (MPH)"),

    # FIXME: should rain figures be Counters instead?
    new_gauge("hourlyrainin", "rain_hourly", "Rainfall per hour (inches)"), #FIXME: units?
    new_gauge("eventrainin", "rain_event", "Rainfall per this event? FIXME. Inches."),
    new_gauge("dailyrainin", "rain_daily", "Rainfall per day (inches)"),
    new_gauge("weeklyrainin", "rain_weekly", "Rainfall per week (inches)"),
    new_gauge("monthlyrainin", "rain_monthly", "Rainfall per month (inches)"),
    new_gauge("totalrainin", "rain_total", "Rainfall total (inches)"),

    new_gauge("solarradiation", "solar_radiation", "Solar Radiation (W/m2)"),
    new_gauge("uv", "uv", "Ultravoilet Index"),
    new_gauge("feelsLike", "outdoor_temperature_heat_index", "Outdoor Temperature Heat Index / Feels Like (Degrees F)"),
    new_gauge("dewPoint", "outdoor_temperature_dew_point", "Outdoor Temperature Dew Point (Degrees F)"),
}

start_http_server(8000)
while True:
    devices = api.get_devices()
    if len(devices) == 0:
        print("No devices found on Ambient Weather account.")
        for gauge in gauges:
            gauge.set(None) # FIXME: this doesn't work anyway and throws. What to do?
        continue
    device = devices[0] # FIXME: handle multiple devices
    # dir(device): ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'api_instance', 'convert_datetime', 'current_time', 'get_data', 'info', 'last_data', 'mac_address']
    last_data = device.last_data
    print(device.info)
    print(device.mac_address)
    print(last_data)
    for gauge in gauges:
        gauge.set(last_data[gauge._ambient_name])
    print("sleeping 60");
    time.sleep(60)
