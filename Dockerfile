FROM python:3.10-slim-bullseye

LABEL maintainer "trick@vanstaveren.us"

WORKDIR /app
EXPOSE 8000
RUN apt-get update && \
    apt-get upgrade -y
COPY requirements.txt requirements.txt
RUN /usr/local/bin/pip install \
  --root-user-action=ignore \
  --disable-pip-version-check \
  -r requirements.txt
COPY * /app/
USER nobody
ENTRYPOINT ["/app/main.py", "--verbose=yes", "--config_file=config/config.yaml"]
