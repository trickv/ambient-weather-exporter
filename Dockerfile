FROM debian:10-slim

LABEL maintainer "trick@vanstaveren.us"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-virtualenv \
    python3-pip \
    python-virtualenv \
    && \
    virtualenv --python=python3 /app

WORKDIR /app
EXPOSE 8000

COPY requirements.pip requirements.pip

RUN /app/bin/pip3 install -r requirements.pip

COPY test.py /app/test.py

USER nobody

ENTRYPOINT ["/app/bin/python", "/app/test.py"]
