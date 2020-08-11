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
                                   title='All Recipes')
    else:
        recipes = mongo.db.recipes.find()
        return render_template('recipes.html', recipes=recipes,
                               title='All Recipes')


if __name__ == "__main__":
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)
