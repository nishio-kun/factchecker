#!/bin/sh

export FLASK_APP=./factchecker/app.py
export MODEL=./factchecker/distinction.h5
export MONOGRAM_KEYS=./factchecker/rich_monogram_keys.txt
export BIGRAM_KEYS=./factchecker/rich_bigram_keys.txt
flask run -h 0.0.0.0
