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
COPY test.py /app/test.py
USER nobody
ENTRYPOINT ["/usr/local/bin/python", "/app/test.py"]
