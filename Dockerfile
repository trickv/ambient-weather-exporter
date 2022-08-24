FROM python:3.10-slim-bullseye

LABEL maintainer "trick@vanstaveren.us"

WORKDIR /app
EXPOSE 8000
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-virtualenv
RUN virtualenv --python=python3 /app             
COPY requirements.pip requirements.pip
RUN /app/bin/pip install -r requirements.pip
COPY test.py /app/test.py
USER nobody
ENTRYPOINT ["/app/bin/python", "/app/test.py"]
