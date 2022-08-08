from asyncio.windows_events import NULL
from email.policy import default
from pickle import NONE
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.validators import InputRequired, ValidationError

db = SQLAlchemy()


pokedex = db.Table('pokedex',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    pokemon = db.relationship("User",
        primaryjoin = (pokedex.c.pokemon_id==id),
        secondaryjoin = (pokedex.c.user_id==id),
        secondary = pokedex,
        backref = db.backref("pokedex", lazy = "dynamic"),
        # lazy = "dynamic"    
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
    
    def catch_poke(self,pokemon_name):
        poke = Pokemon.query.filter_by(name=pokemon_name).first()
        print(self.pokemon)
        if len(self.pokemon) < 5:
            self.pokemon.append(poke)
            # self.pokemon.catch_pokemon()
        print("word")
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
    img_url = db.Column(db.String)

    def __init__(self,name,ability,type,Def,attack,hp,base_exp,img_url):
        self.name = name
        self.ability = ability
        self.type = type
        self.Def = Def
        self.attack = attack
        self.hp = hp 
        self.base_exp = base_exp
        self.img_url = img_url

    def catch_pokemon(self):
        db.session.add(self)
        db.session.commit()


    def rel_pokemon(self):
        self.trainer = None
        db.session.commit()
