#!/bin/sh

gunicorn --log-level info --log-file=./gunicorn.log --workers 4 --name app -b 0.0.0.0:5000 --reload app.exporter:app