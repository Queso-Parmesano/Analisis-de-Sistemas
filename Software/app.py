from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from flask import Flask, render_template, redirect, url_for, flash
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import datetime

app = Flask(__name__, static_folder="templates", static_url_path="")

app.config['SECRET_KEY'] = 'zaza'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/automoviliaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
