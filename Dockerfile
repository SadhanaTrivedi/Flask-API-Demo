FROM python:3.7.5-alpine

COPY ./src /app
COPY requirements.txt /app/

WORKDIR /app
RUN pip install -r requirements.txt

ENV SIMPLE_SETTINGS=settings_common,settings_docker

EXPOSE 5000
