#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import logging
import sys
from sys import argv
from time import sleep

import click
from prometheus_client import Info
from prometheus_client import start_http_server
from yaml_config_wrapper import Configuration

from ambient_client import *

@click.command()
@click.option('--verbose', type=bool, default=False, help='Enable verbose logging.')
@click.option('--config_file', type=str, default=None, help='YAML configuration file', required=True)
def launch(verbose, config_file):
  config_logging(verbose)
  logging.info("Initializing Ambient Weather Client")

  config = Configuration(config_src=config_file, config_schema_path='config_schema.json')
  logging.debug("Configuration: " + str(config.get_config('ambient')))
  cli = AmbientClient(config.get_config('ambient'))
  cli.initialize_gauges()

  i = Info('ambient_weather_exporter', 'Prometheus export for Ambient Weather personal weather station')
  i.info({
    'version': '0.1'
  })

  server_port = int(config.get_config('listen_port'))
  logging.info('Starting HTTP server on port %i', server_port)
  start_http_server(server_port)

  interval = int(config.get_config('poll_interval'))
  logging.info('Starting to poll Ambient Weather every %i seconds', interval)
  while True:
    sleep(interval)
    try:
      logging.info("Polling Ambient Weather")
      cli.poll()
    except Exception as e:
      logging.error("Failed to pull data: %s", e)


def config_logging(verbose: bool):
  log_level = logging.DEBUG if verbose else logging.INFO
  logging.basicConfig(
    stream=sys.stdout,
    level=log_level,
    format='%(asctime)s (%(processName)s - %(name)s) [%(levelname)s] %(message)s'
    )

if __name__ == '__main__':
  print(str(argv))
  poll_time, api_key, app_key = launch()
