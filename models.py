'''
ListTuner - Hendrik Scheeres
models.py

This file contains the models that define the database structure.
 '''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Seals(db.Model):
    ''' this table contains the seal playlist parameters '''

    __tablename__ = 'seals'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    playlist_id = db.Column(db.String(128))
    playlist_name = db.Column(db.String(128))
    playlist_creator = db.Column(db.String(128))
    playlist_href = db.Column(db.String(128))
