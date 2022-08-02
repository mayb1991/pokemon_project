from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .models import User

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)


@login.user_loader
def load_user(username):
    return User.query.get(username)


# db = SQLAlchemy(app)
from .models import db
from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)


from . import routes
from app import models