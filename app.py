import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'food_factory'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    recipes = mongo.db.recipes.aggregate([{'$sample': {'size': 4}}])

    return render_template('index.html', recipes=recipes)


@app.route('/get_recipes/<key>/<value>')
def get_recipes(key, value):
    """ Filter recipes by a specified key in database """

    if key and value:
        if key == 'cuisine_type':
            cuisine_type = {'cuisine_type': value}

            recipes = mongo.db.recipes.find(cuisine_type)
            return render_template('recipes.html', recipes=recipes,
                                   title=value)
        else:
            recipes = mongo.db.recipes.find()
            return render_template('recipes.html', recipes=recipes,
                                   title='All')
    else:
        recipes = mongo.db.recipes.find()
        return render_template('recipes.html', recipes=recipes,
                               title='All')


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
    """Take user input from add_recipe form and insert into recipes collection"""

    recipes = mongo.db.recipes

    if request.method == 'POST':
        ingredients = request.form.getlist('ingredients')
        method = request.form.getlist('method')

        recipe_details = {
            'recipe_name': request.form['recipe_name'],
            'description': request.form['description'],
            'difficulty': request.form['difficulty'],
            'img_url': request.form['img_url'],
            'ingredients': ingredients,
            'method': method,
            }
        recipes.insert_one(recipe_details)

        return redirect(url_for('get_recipes', key='recipes',
                        value='all'))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)
