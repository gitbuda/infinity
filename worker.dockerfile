FROM ubuntu:14.04

MAINTAINER buda

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev build-essential
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip install numpy scipy

RUN mkdir -p /app

ADD algorithm /app/algorithm
ADD common /app/common
ADD data_structure /app/data_structure
ADD preprocess /app/preprocess
ADD util /app/util

# TODO: python path

EXPOSE 8001

ENV TERM dumb

CMD uwsgi --http-socket 0.0.0.0:8001 --wsgi-file computation.py --callable app --processes 2 --threads 1 --disable-logging --master 32768
