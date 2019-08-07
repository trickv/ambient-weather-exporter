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

indoor_temperature = Gauge("indoor_temperature", "Indoor Temperature in F")
outdoor_temperature = Gauge("outdoor_temperature", "Outdoor Temperature in F")

start_http_server(8000)
while True:
    device = api.get_devices()[0]
    last_data = device.last_data
    print(device.info)
    print(device.mac_address)
    print(dir(device))
    print(last_data)
    indoor_temperature.set(last_data['tempinf'])
    outdoor_temperature.set(last_data['tempf'])
    print("sleeping 60");
    time.sleep(60)
