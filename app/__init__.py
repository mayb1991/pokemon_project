from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
# from .models import Pokedex


app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy(app)
from .models import db
from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)


from . import routes
from app import models