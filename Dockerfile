FROM python:3.10-slim-bullseye

LABEL maintainer "fleureed@gmail.com"
WORKDIR /app
RUN apt-get update && \
    apt-get upgrade -y
COPY src/requirements.txt requirements.txt
RUN /usr/local/bin/pip install \
  --root-user-action=ignore \
  --disable-pip-version-check \
  -r requirements.txt
COPY src/* /app/
USER nobody
ENTRYPOINT ["/app/main.py", "--config_file=config/config.yaml"]
