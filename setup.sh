#!/bin/bash

virtualenv -p python3 py3
source py3/bin/activate
pip install -r requirements_console.txt
