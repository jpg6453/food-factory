import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'food_factory'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY']= os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    recipes = mongo.db.recipes.aggregate([{'$sample': {'size': 4}}])

    return render_template('index.html', recipes=recipes)

@app.route('/register', methods=['GET', 'POST'])
def register():

        form = RegistrationForm(request.form)

        if request.method =='POST' and form.validate_on_submit():
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                flash(f'Username already exists, please login','danger')
                return redirect(url_for("login"))
            
            register = {
                "username": request.form.get("username").lower(),
                "email": request.form.get("email").lower(),
                "password": generate_password_hash(
                    request.form.get("password")) 
            }
            mongo.db.users.insert_one(register)
            
            session["user"] = request.form.get("username").lower()

            flash(f'Your account has been created! You are now able to log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method =='POST':
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()

                flash("Welcome back {}!".format(
                    request.form.get("username")), 'success')
                return redirect(url_for(
                    "index"))
            else:
                flash("Incorrect Username/password, Please try again", 'danger')
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username/password, Please try again", 'danger')
            return redirect(url_for("login"))

    return render_template('login.html', title='Login',form=form)

@app.route('/logout')
def logout():
    """ clears the session of the user which logs them out """
    session.clear()
    return redirect(url_for('index'))


@app.route('/get_recipes')
def get_recipes():
    """ Filter recipes by a specified key in database """

    cuisine_type = request.args.get("cuisine_type")
    difficulty = request.args.get("difficulty")
    main_ingredient = request.args.get("main_ingredient")
    sub_title = main_ingredient

    if cuisine_type:
        recipes = mongo.db.recipes.find({'cuisine_type': cuisine_type})
        title = cuisine_type
        sub_title = ''
    elif difficulty:
        recipes = mongo.db.recipes.find({'difficulty': difficulty})
    elif main_ingredient:
        recipes = mongo.db.recipes.find({'main_ingredient': main_ingredient})
        title = 'all'
        sub_title = main_ingredient
    else:
        recipes = mongo.db.recipes.find().sort('_id', -1)
        title = 'all'
        sub_title = ''
    return render_template('recipes.html', recipes=recipes, title=title, sub_title=sub_title)


@app.route('/recipe_detail/<recipe_id>')
def recipe_detail(recipe_id):
    """ Render template to display a recipe in detail """

    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/add_recipe')
def add_recipe():
    """ Displays user form to add a recipe """

    return render_template('add_recipe.html')


@app.route('/insert_recipe', methods=['GET', 'POST'])
def insert_recipe():
    """
    Take user input from add_recipe form 
    and insert into recipes collection
    """
    recipes = mongo.db.recipes

    if request.method == 'POST':
        ingredients = request.form.getlist('ingredients')
        method = request.form.getlist('method')
        date = datetime.now()

        recipe_details = {
            'recipe_name': request.form['recipe_name'],
            'description': request.form['description'],
            'prep_time': request.form['prep_time'],
            'serves': request.form['serves'],
            'difficulty': request.form['difficulty'],
            'cuisine_type': request.form['cuisine_type'],
            'img_url': request.form['img_url'],
            'ingredients': ingredients,
            'main_ingredient': request.form['main_ingredient'],
            'method': method,
            'created_by':session['user'],
            'create_date': date
            }
        recipes.insert_one(recipe_details)
        flash("Recipe added successfully!", 'success')
        return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    """ Supply user with a populated form to edit """

    difficulty = ['Easy', 'Medium', 'Hard']

    cuisines = ['Chinese', 'Indian', 'Italian', 'Mediterranean']

    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe=recipe, difficulty=difficulty, cuisines=cuisines)


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    """ Update the amended recipe in the database """
    recipe = mongo.db.recipes
    recipe.find_one({'_id': ObjectId(recipe_id)})
    recipe.update_one({'_id': ObjectId(recipe_id)},
                      {'$set': {
                          'recipe_name': request.form.get('recipe_name'),
                          'description': request.form.get('description'),
                          'difficulty': request.form.get('difficulty'),
                          'prep_time': request.form.get('prep_time'),
                          'cuisine_type': request.form.get('cuisine_type'),
                          'serves': request.form.get('serves'),
                          'img_url': request.form.get('img_url'),
                          'ingredients': request.form.getlist('ingredients'),
                          'main_ingredient': request.form.get('main_ingredient'),
                          'method': request.form.getlist('method')

                      }})

    flash("Recipe updated!", 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """ Delete a document from recipe collection """
    
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})

    flash("Recipe deleted", 'danger')

    return redirect(url_for(
    'my_recipes', created_by=session['user']))


@app.route('/my_recipes')
def my_recipes():

    created_by = request.args.get("created_by")

    if created_by:
        recipes = mongo.db.recipes.find({'created_by': created_by}).sort('create_date',-1)
    
    return render_template('my_recipes.html', recipes=recipes)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)
