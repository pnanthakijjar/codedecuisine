from flask import Flask, render_template, request, redirect
app = Flask(__name__)
import MySQLdb
import MySQLdb.cursors
import gc
gc.collect()

@app.route('/')
def index():
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    diet = "3"
    cursor.execute("""SELECT * FROM Diets WHERE dietID=%s""", (diet))
    rv = cursor.fetchall()
    db.close()
    #return rv[0]['name']
    return render_template('index.html')

@app.route('/home')
def home():
    return '<h1>Hello, Home!!!</h1>'

@app.route('/search')
def search():
    #return '<h1>Hello, Search!!!</h1>'
    return render_template('search.html')

#@app.route('/view/<int:rec_id>')
#def view(rec_id):
@app.route('/view')
def view():
    #return '<h1>Hello, View!!!</h1>'
    return render_template('view.html')

#@app.route('/edit/<int:rec_id>')
#def edit(rec_id):
app.route('/edit')
def edit():
    #return '<h1>Hello, Edit!!!</h1>'
    return render_template('edit.html')

@app.route('/submit')
def submit():
    #return '<h1>Hello, View!!!</h1>'
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)

