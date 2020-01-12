#!/bin/sh

export FLASK_APP=./factchecker/app.py
flask run -h 0.0.0.0
