#! /usr/bin/env bash

export FLASK_APP=application.py
export FLASK_DEBUG=1
export DATABASE_URL=
export CLIENT_SECRET=""


flask run
