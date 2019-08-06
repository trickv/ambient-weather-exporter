#!/usr/bin/env python

from ambient_api.ambientapi import AmbientAPI

api = AmbientAPI()
device = api.get_devices()[0]
print(device.last_data);
