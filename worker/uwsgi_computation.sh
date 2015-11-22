#!/bin/bash

# gunicorn api:app

# --ini http://uwsgi.it/configs/myapp.ini config from ini file
uwsgi --http :8001 --wsgi-file computation.py --callable app --processes 2 --threads 1 --disable-logging

