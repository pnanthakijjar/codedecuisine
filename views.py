from flask import Flask, render_template, request, redirect
import string
import cuisineRecipedb as recipesdb
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', author=author, name=name)

@app.route('/search')
def search():
# Search by Diets and Name
	recipe_chosen =[]
	recipe_list = []

	for x in request.form:
		recipe_chosen.append(int(x))

	for recipe in recipe_chosen:
		recipe_list.append(recipesdb.RecipeList()[recipe])

	return render_template('search.html', recipelist=recipe_list)

@app.route('/view_recipes', methods=['POST'])
#Show ALL RECIPES
def view_recipes():
	recipe_list = []

	for r in recipesdb:
		recipe_list.append(r)

	return render_template('view_recipes.html', recipelist=recipe_list)

@app.route('/edit_recipes')
def edit():
	return render_template('edit_recipes.html', author=author, name=name)

@app.route('/add_recipes', methods=['POST'])
def add_recpies():
# INSERT new recipe name and ingredients into the database
	return render_template('add_recipes.html', author=author, name=name)



if __name__=='__main__':
	app.run(debug=True)
