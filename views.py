from flask import Flask, render_template, request, redirect
import string
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', author=author, name=name)

@app.route('/search')
def search():
	return render_template('search.html', author=author, name=name)

@app.route('/view_recipes')
def view_recipes():
	return render_template('view_recipes.html', author=author, name=name)

@app.route('/edit_recipes')
def edit():
	return render_template('edit_recipes.html', author=author, name=name)

@app.route('/add_recipes')
def add_recpies():
	return render_template('add_recipes.html', author=author, name=name)



if __name__=='__main__':
	app.run(debug=True)
