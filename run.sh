#! /usr/bin/env bash

export FLASK_APP=application.py
export FLASK_DEBUG=1
export DATABASE_URL=postgres://jqrzpszujkqmom:754d2283239f1e013ac639e527b0dcce4d6e82e5624a02c5f1f7df2df06e97ae@ec2-54-247-103-43.eu-west-1.compute.amazonaws.com:5432/dcc3rabca7n14k
export CLIENT_ID="faf48d2950e34b8a8140defd25918af8"
export CLIENT_SECRET="6a40135d61f84b16885aa3d336ed5fff"


flask run
