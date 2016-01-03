FROM ubuntu:14.04

MAINTAINER buda

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev build-essential
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip install cython uwsgi falcon ujson pymongo bson

RUN mkdir -p /app
COPY common /app/common
COPY database /app/database
COPY data_structure /app/data_structure
COPY preprocess /app/preprocess
COPY 20news-18828 /app/20news-18828

ENV TERM dumb
ENV PYTHONPATH $PYTHONPATH:/app

EXPOSE 9001

WORKDIR /app/database
CMD uwsgi --http-socket 0.0.0.0:9001 --wsgi-file rest.py --callable app --processes 1 --threads 1 --master --logto /app/log.txt --buffer-size 32768
