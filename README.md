# ambient-weather-exporter
Prometheus exporter for an Ambient Weather station as reported from their API

This little project is a messy hack, but it works against my [WS-2902](https://www.ambientweather.com/amws2902.html) which I've had for just a few weeks at the time I'm writing this. It may not work well for stations which ship less metrics to Ambient Weather.

# Libraries

Almost all of this code is just binding together two things:
* [ambient_api](https://github.com/avryhof/ambient_api) - a Python library which interfaces with the Ambient Weather API
* [prometheus/client_python](https://github.com/prometheus/client_python) - lets me register a series of metrics and runs a simple web server exposing the data read from Ambient as Prometheus metrics.

I use Docker to run this "in production" so there's a Dockerfile too, and [](builds on Docker Hub).

# What it looks like

[You came for a graph, so here's one](https://snapshot.raintank.io/dashboard/snapshot/XZJZDZlgPxQSaC6gP8pGKbuWsLmvGWYI) where you can clearly see that my weather station is not mounted properly (the wind is always coming from ~270 degrees?)

# How to use

- Get an API key from Ambient Weather.
- Use my Application Key (67a05cffa31946ad9f15ffbc0cbecdcf2e933d488eaa49ef84c8d40f566a0bcb) from Ambient below
- Run it with Docker
```
docker run -d --restart=unless-stopped  -e AMBIENT_API_KEY=yourkey -e AMBIENT_APPLICATION_KEY=67a05cffa31946ad9f15ffbc0cbecdcf2e933d488eaa49ef84c8d40f566a0bcb -p 8000:8000 trickv/ambient-weather-exporter:latest
```

[![Docker Pulls](https://img.shields.io/docker/pulls/trickv/ambient-weather-exporter.svg?style=plastic)](https://hub.docker.com/r/trickv/ambient-weather-exporter/)

Then configure Prom to scrape it every 60 seconds.

# Alternative approaches
Ideally, I'd rather get this data directly from the base station which sits in my house so that I'm not beholden to Ambient Weather's infrastructure. But I haven't found a way to do that.
