FROM python:3.5.3

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt requirements-dev.txt /tock/

RUN pip install -r /tock/requirements.txt -r /tock/requirements-dev.txt
