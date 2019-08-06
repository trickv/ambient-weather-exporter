#!/usr/bin/env python

from ambient_api.ambientapi import AmbientAPI
from prometheus_client import Info, Gauge
from prometheus_client import start_http_server

api = AmbientAPI()
if not api.api_key:
    raise Exception("You must specify an API Key")
if not api.application_key:
    raise Exception("You must specify an Application Key")

device = api.get_devices()[0]
last_data = device.last_data
print(last_data)

i = Info("ambient_weather_exporter", "Prometheus exporter for Ambient Weather personal weather station")
i.info({'version': '0'})

g = Gauge("indoor_temperature", "Indoor Temperature in F")
g.set(last_data['tempinf'])
g = Gauge("outdoor_temperature", "Outdoor Temperature in F")
g.set(last_data['tempf'])

start_http_server(8000)
import time
time.sleep(10)
