from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.validators import InputRequired, ValidationError

db = SQLAlchemy()


pokedex = db.Table("pokedex",
    db.Column("pokedex_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("pokemon_id", db.Integer, db.ForeignKey("user.id")))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    pokemon = db.relationship("User",
        primaryjoin = (pokedex.c.pokemon_id==id),
        secondaryjoin = (pokedex.c.pokedex_id==id),
        secondary = pokedex,
        backref = db.backref("pokedex", lazy = "dynamic"),
        lazy = "dynamic"    
    )

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
    

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), nullable=False)
    ability = db.Column(db.String(65), nullable=False)
    type = db.Column(db.String(65), nullable=False)
    Def = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    base_exp = db.Column(db.Integer, nullable=False)

    def __init__(self,name,ability,type,Def,attack,hp,base_exp):
        self.name = name
        self.ability = ability
        self.type = type
        self.Def = Def
        self.attack = attack
        self.hp = hp
        self.base_exp

    
