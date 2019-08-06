#!/usr/bin/env python

from ambient_api.ambientapi import AmbientAPI

api = AmbientAPI()
if not api.api_key:
    raise Exception("You must specify an API Key")
if not api.application_key:
    raise Exception("You must specify an Application Key")

device = api.get_devices()[0]
print(device.last_data);
