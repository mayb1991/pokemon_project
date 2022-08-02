from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.validators import InputRequired, ValidationError

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password 

    def update_user(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def saveUpdates(self):
        db.session.commit()