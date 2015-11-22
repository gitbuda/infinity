#!/bin/bash

# gunicorn api:app

# --ini http://uwsgi.it/configs/myapp.ini config from ini file

# uwsgi --http :8001 --wsgi-file computation.py --callable app --processes 4 --threads 1 --disable-logging --master
# uwsgi --http :8001 --wsgi-file computation.py --callable app --async 4 --disable-logging --master
# gunicorn -w 4 computation:app -b localhost:8001 -t 120
# uwsgi --socket /opt/socket/uwsgi/infinity.sock --wsgi-file computation.py --callable app --processes 4 --threads 1 --vacuum --chown-socket www-data:www-data
# --chown-socker=user:group
uwsgi --socket 0.0.0.0:8001 --wsgi-file computation.py --callable app --processes 4 --threads 1 --disable-logging --buffer-size 32768

