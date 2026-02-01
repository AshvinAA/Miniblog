
from flask import Flask, render_template, url_for , flash ,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8e4ef53df82522c718d6d97abd4941b4'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

from flaskblog import routes
