import logging
import yaml

from ambient_api.ambientapi import AmbientAPI
from prometheus_client import Gauge

class ClientInitializationException(Exception):
  pass

class StaleDataException(Exception):
  pass

class AmbientClient:
  def __init__(self, config: dict):
    field_config = 'fields.yaml'

    if 'field_mapping' in config and config['field_mapping'] is not None:
      field_config = config['field_mapping']
    logging.debug('loading field mapping from %s', field_config)
    with open(field_config, 'r') as f:
      self.field_mapping = yaml.safe_load(f)
    logging.debug('loaded field mapping: %s', self.field_mapping)

    logging.debug('building ambient client')
    self.client = AmbientAPI(
      AMBIENT_API_KEY=config['api_key'],
      AMBIENT_APPLICATION_KEY=config['application_key']
    )

  def initialize_gauges(self):
    logging.debug('initializing_guages')
    self.gauges = {}
    dat = self.pull_data()
    if dat is None:
      raise ClientInitializationException("No devices detected.  Cannot initialize.")

    logging.debug('data: %s', str(dat))
    for k in dat.keys():
      if k in self.field_mapping.keys():
        self.gauges[k] = Gauge(self.field_mapping[k]['name'], self.field_mapping[k]['description'])

    logging.debug('gauges: %s', self.gauges)
    self.populate_gauges(dat)


  def pull_data(self) -> dict:
    logging.debug('pulling data')
    resp = self.client.get_devices()
    if len(resp) == 0:
      logging.warn("No data returned.")
      return None
    return resp[0].last_data # FIXME: Handle multiple devices

  def populate_gauges(self, device_data: dict):
    for k in device_data.keys():
      if k in self.gauges.keys():
        logging.debug('using %s to set %s to %s', k, self.gauges[k], device_data[k])
        self.gauges[k].set(device_data[k])

  def poll(self):
    dat = self.pull_data()
    self.populate_gauges(dat)
