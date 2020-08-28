#!/bin/bash

gunicorn orderingsys.wsgi -c gunicorn.py

tail -f /dev/null
