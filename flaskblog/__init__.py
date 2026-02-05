
from flask import Flask, render_template, url_for , flash ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '8e4ef53df82522c718d6d97abd4941b4'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login' #this is a global configuration which means if the user tries to go to routes that are yet to be unlocked, they will just be redirected to the login site
login_manager.login_message_category = 'info'

from flaskblog import routes
