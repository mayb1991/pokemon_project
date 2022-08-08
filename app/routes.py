from app import app
from flask import render_template, request, url_for, redirect
import requests
from app.forms import LoginForm, PokemonSearchForm, UserCreationForm
from app.models import User, Pokemon
from app.models import db
from flask_login import logout_user,current_user, login_required


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

            # add user to database
            user = User(username, email, password)

            # add instance to our db
            db.session.add(user) 
            db.session.commit()
            # flash("Successfully registered a new user", 'success')
            return redirect('/login')
    return render_template('signup.html', form = form)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        print("Post request made")
        if form.validate():
            print("form valid")
            return redirect('/pokemon_search')
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
def search():
    form = PokemonSearchForm()
    caught = False
    pokemon_info = {}
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
            # if current_user.team_building.filter_by(name=pokemon.name):
            #     caught = True
        
    return render_template('search.html',form=form, pokemon_info=pokemon_info)
    # return render_template('search.html',form=form, pokemon_info = pokemon_info)
   

@app.route('/pokeball/<string:pokemon_name>', methods=["GET", "POST"])
@login_required
def catch_pokemon(pokemon_name):
    current_user.catch_poke(pokemon_name)
    # poke = Pokemon.query.filter_by(name=pokemon_name).first()
    # print(current_user.pokemon)
    # if len(current_user.pokemon) < 5:
    #     current_user.pokemon.append(poke)
    #     current_user.catch_pokemon()
    #     print("word")
    return redirect(url_for('search'))