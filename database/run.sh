#!/bin/bash

uwsgi --http :3000 --wsgi-file rest.py --callable app --processes 1 --threads 1 --master --disable-logging
