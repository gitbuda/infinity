#!/bin/bash

uwsgi --socket 0.0.0.0:8001 --wsgi-file computation.py --callable app --processes 2 --threads 1 --disable-logging --buffer-size 32768

