#!/bin/bash

uwsgi --http-socket 0.0.0.0:9001 --wsgi-file rest.py --callable app --processes 1 --threads 1 --master --disable-logging --buffer-size 32768
