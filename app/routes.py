from app import app
from flask import render_template, request, url_for, redirect, flash
import requests
from app.forms import LoginForm, PokemonSearchForm, UserCreationForm

from app.models import User, Pokemon
from app.models import db
from flask_login import logout_user, current_user, login_required, login_user
from werkzeug.security import check_password_hash


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == "POST":
        print('POST request made')
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('signup.html', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        print("Post request made")
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Welcome back {form.username.data}!', category='success')

                print("form valid")
                return redirect('/pokemon_search')
            else:
                print("wrong info")
    return render_template('login.html', form = form)


@app.route('/user/update', methods=["GET", "POST"])
def update():
    form = UserCreationForm()
   
    if request.method=="POST":
        
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user_up = User.query.filter(User.username==username).first()
            print(user_up)
            user_up.update_user(username,email,password)
            user_up.saveUpdates()
            print("DONE!!!!!!")
            return redirect(url_for('/pokemon_search', username=username,user_up=user_up))
        else:
            print('Invalid form. Please fill out the form correctly.', 'danger')
    return render_template('search.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/pokemon_search', methods=['GET', 'POST'])
@login_required
def search():
    form = PokemonSearchForm()
    pokemon_info = {}
    poke_set = set()
    if request.method == 'POST':
        pn = form.name.data
        get_pokemon_info = f"https://pokeapi.co/api/v2/pokemon/{pn}"
        response = requests.get(get_pokemon_info)
        if response.ok:
            data = response.json()
            pokemon_info = {
                'name': data['forms'][0]['name'],
                'abilities': data['abilities'][1]['ability']['name'],
                'base_exp': data['base_experience'],
                'sprite': data['sprites']['front_shiny'],
                'attack': data['stats'][1]['base_stat'],
                'h_p': data['stats'][0]['base_stat'],
                'def': data['stats'][2]['base_stat'],
                'type': data['types'][0]['type']['name']
            }
            check_info = Pokemon.query.filter_by(name=pokemon_info['name']).first()
            if not check_info:
                pokemon = Pokemon(pokemon_info['name'], pokemon_info['abilities'], pokemon_info['type'], 
                pokemon_info['def'], pokemon_info['attack'], pokemon_info['h_p'], 
                pokemon_info['base_exp'],pokemon_info['sprite'])
                pokemon.catch_pokemon()
            print(current_user.id)
            p1 = current_user.pokedex              
            poke_set = {p.name for p in p1}
            print(poke_set)
            flag = False
            if pokemon_info['name'] in poke_set:
                flag = True
            
        
            return render_template('search.html',form=form, pokemon_info=pokemon_info, flag=flag)
    return render_template('search.html',form=form, pokemon_info = pokemon_info)
   

@app.route('/myPokemon')
@login_required
def getPoke():
    # if current_user.is_authenticated():
    pokemon = current_user.pokedex.all()
    print(pokemon)
    print(type(pokemon))
    print(pokemon[0].name)
    return render_template('user_pokedex.html',pokemon = pokemon)


@app.route('/catchPoke/<pokemon>')
@login_required
def catchPoke(pokemon):
    current_user
    poke = Pokemon.query.filter_by(name = pokemon).first()
    if len(current_user.pokedex.all()) < 5:
        current_user.catchPokemon(poke)
    else:
        flash("Your team is full please release a Pokemon", "danger")
    return redirect(url_for('search'))

@app.route('/releasePoke/<pokemon>')
@login_required
def releasePoke(pokemon):
    poke = Pokemon.query.filter_by(name = pokemon).first()
    current_user.releasePokemon(poke)
    return redirect(url_for('getPoke'))

@app.route('/battle')
def battle_royal():
    users = User.query.all()
    return render_template('battle.html', users=users)


@app.route('/battle/<int:user_id>')
def battling(user_id):
    user = User.query.get(user_id)
    pokes = user.pokedex.all()
    current_user.battles(user)
    return render_template('battling.html', user = user, pokes=pokes)