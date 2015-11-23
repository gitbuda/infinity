FROM ubuntu:14.04

MAINTAINER buda

RUN apt-get update
RUN apt-get install -y nginx htop python3-pip python3-dev build-essential
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip install cython uwsgi falcon ujson

WORKDIR /database

COPY database /database

EXPOSE 80

CMD uwsgi --http 0.0.0.0:80 --wsgi-file rest.py --callable app --processes 1 --threads 1 --disable-logging --master
