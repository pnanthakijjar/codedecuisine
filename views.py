from flask import Flask, render_template, request, redirect
import string
import recipelistdb as recipesdb
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
		if x == general:
			#do the check with recipe name/title
			recipe_chosen.append(str(x))

		elif x == diet:
			#do the check with diets
			recipe_chosen.append(str(x))

	for recipe in recipe_chosen:
		recipe_list.append(recipesdb.RecipeList()[recipe])

	return render_template('search.html', recipelist=recipe_list)

@app.route('/edit_recipes')
def edit():
	return render_template('edit_recipes.html', author=author, name=name)

@app.route('/add_recipes', methods=['POST'])
def add_recpies():
# INSERT new recipe name and ingredients into the database
	return render_template('add_recipes.html', author=author, name=name)



if __name__=='__main__':
	app.run(debug=True)
