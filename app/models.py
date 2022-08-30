from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.validators import InputRequired, ValidationError
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


pokedex = db.Table('pokedex',
    db.Column('caughtby_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('caught_id', db.Integer, db.ForeignKey('pokemon.id')))
    # db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    # db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")))

battles = db.Table('battle',
    db.Column('battleWho_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('battler_id', db.Integer, db.ForeignKey('user.id')),

)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    pokedex = db.relationship("Pokemon",
        secondary = pokedex,
        backref = db.backref('pokemon_trainer', lazy = 'dynamic'),
        lazy = 'dynamic'  
    )


    # team = db.relationship("Pokemon",
    #     secondary = pokedex,
    #     backref='pokemon_trainer',
    #     lazy = 'dynamic'
    # )

    battle = db.relationship("User",
        primaryjoin = (battles.c.battleWho_id == id),
        secondaryjoin = (battles.c.battler_id == id),
        secondary = battles,
        backref = db.backref('battler', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def update_user(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def saveUpdates(self):
        db.session.commit()
    
    def catchPokemon(self, poke):
        self.pokedex.append(poke)
        db.session.commit()

    def releasePokemon(self,poke):
        self.pokedex.remove(poke)
        db.session.commit()

    def battles(self, user):
        self.battle.append(user)
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
