#!/bin/bash

uwsgi --socket 0.0.0.0:8001 --wsgi-file computation_mock.py --callable app --processes 1 --threads 1 --disable-logging --buffer-size 32768
