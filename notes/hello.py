from flask import Flask
app = Flask(__name__)

from flaskext.mysql import MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'cuisineRecipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
@app.route('/')
def index():
        return 'Index Page'

@app.route('/hello')
def hello():
    cursor = mysql.connect().cursor()
    insert_stmt = (
              "INSERT INTO Recipes (name, description, dietID, servings) "
                "VALUES (%s, %s, %s, %s)"
                )
    data = ('waffles', 'delicious waffles', 2, 3)
    cursor.execute(insert_stmt, data)
    #ingredient = 'egg'
    #cursor.execute("SELECT * from Recipes WHERE name='" + ingredient + "'")
    #data = cursor.fetchone()

@app.route('/world')
def hello_world():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
