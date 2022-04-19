from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "12a4e803344ea1f00f9bc9fb530f0a9e7f7ea3e19213"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["CLIENT_FILE"] = "/mnt/c/users/ahmad/desktop/flask_project"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_project import routes