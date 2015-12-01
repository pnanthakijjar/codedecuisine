from flask import Flask, render_template, request, redirect
app = Flask(__name__)
import MySQLdb
import MySQLdb.cursors
import string
import gc
gc.collect()

@app.route('/')
def webpage():
    return render_template('webpage.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        g = request.form['general']
        d = request.form['diet']
        #g = "can"
        #d = None
        if g == "Null":
            g = None
        if d == "Null":
            d = None
        if g is None and d is None:
            db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM Recipes""")
            rv = cursor.fetchall()
            db.close()
            return render_template('search.html', rv=rv, methods=['GET', 'POST'])
        elif g is None:
            db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM Recipes WHERE diet='{0}'""".format(d))
            rv = cursor.fetchall()
            db.close()
            return render_template('search.html', rv=rv, methods=['GET', 'POST'])
        elif d is None:
            db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM Recipes WHERE 
                name LIKE '%{0}%' OR ingredients LIKE '%{0}%' 
                OR description LIKE '%{0}%'""".format(g))
            rv = cursor.fetchall()
            db.close()
            return render_template('search.html', rv=rv, methods=['GET', 'POST'])
        else:
            db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM Recipes WHERE diet='{0}' AND 
                (name LIKE '%{1}%' OR ingredients LIKE '%{1}%' OR 
                description LIKE '%{1}%')""".format(d, g))
            rv = cursor.fetchall()
            db.close()
            return render_template('search.html', rv=rv, methods=['GET', 'POST'])
    else:
        return render_template('search.html')

@app.route('/view/<int:rec_id>', methods=['GET', 'POST'])
def view(rec_id):
    rec_id = str(rec_id)
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Recipes WHERE recipeID='{0}'""".format(rec_id))
    rv = cursor.fetchone()
    db.close()
    if rv :
        return render_template('view_recipes.html', rec=rec_id, rv=rv)
    else:
        return "error"

@app.route('/edit/<int:rec_id>', methods=['GET', 'POST'])
def edit(rec_id):
    rec_id = str(rec_id)
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Recipes WHERE recipeID='{0}'""".format(rec_id))
    rv = cursor.fetchone()
    db.close()
    if rv :
        return render_template('edit_recipes.html', rec=rec_id, rv=rv)
    else:
        return "error"

@app.route('/edited', methods=['GET', 'POST'])
def edited():
    if request.method == "GET":
        if request.args['sub'] == "submit":
            nam = request.args['name']
            die = request.args["diet"]
            des = request.args["desc"]
            ing = request.args["ingr"]
            ins = request.args["inst"]
            rID = request.args["rID"]
            db = MySQLdb.Connection(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("""UPDATE Recipes SET name='{0}', diet='{1}', description='{2}', 
                ingredients='{3}', instructions='{4}' WHERE recipeID='{5}'"""
                .format(nam, die, des, ing, ins, rID))
            db.commit()
            # insert into ingredients table
            ingredient_list = ing.rstrip().split('\n')
            ingr_list = []
            for i in ingredient_list:
                if ":" not in i:
                    ingr_list.append(i)
                else:
                    ing_index = i.index(':')
                    ing = i[ing_index:]
                    ing_list = list(ing)
                    ing_list.remove(':')
                    ing_list.remove(" ")
                    ingr_list.append(ing_list)
            lst = []
            for j in ingr_list:
                lst.append(''.join(j))
            for i in lst:
                cursor.execute("""SELECT * FROM Diets WHERE name='{0}'""".format(die))
                rv = cursor.fetchone()
                if rv is None:
                    cursor.execute("""INSERT INTO Ingredients(name) VALUES('{0}')""".format(i))
                    db.commit()
            cursor.execute("""SELECT * FROM Recipes WHERE recipeID='{0}'""".format(rID))
            rv = cursor.fetchone()
            db.close()
            return render_template('view_recipes.html', rec=rID, rv=rv)
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add_recipes.html')

@app.route('/submitedited', methods=['GET', 'POST'])
def submitEdited():
    if request.method == "GET":
        if request.args['sub'] == "submit":
            nam = request.args['name']
            die = request.args["diet"]
            des = request.args["desc"]
            ing = request.args["ingr"]
            ins = request.args["inst"]
            db = MySQLdb.Connection(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            # check if diet exists
            cursor.execute("""SELECT * FROM Diets WHERE name='{0}'""".format(die))
            rv = cursor.fetchone()
            if rv is None:
                cursor.execute("""INSERT INTO Diets(name) VALUES('{0}')""".format(die))
                db.commit()
            # insertion
            cursor.execute("""INSERT INTO 
                Recipes(name, diet, description, ingredients, instructions) 
                VALUES('{0}', '{1}', '{2}', '{3}', '{4}')"""
                .format(nam, die, des, ing, ins))
            db.commit()
            # insert into ingredients table
            ingredient_list = ing.rstrip().split('\n')
            ingr_list = []
            for i in ingredient_list:
                if ":" not in i:
                    ingr_list.append(i)
                else:
                    ing_index = i.index(':')
                    ing = i[ing_index:]
                    ing_list = list(ing)
                    ing_list.remove(':')
                    ing_list.remove(" ")
                    ingr_list.append(ing_list)
            lst = []
            for j in ingr_list:
                lst.append(''.join(j))
            for i in lst:
                cursor.execute("""SELECT * FROM Diets WHERE name='{0}'""".format(die))
                rv = cursor.fetchone()
                if rv is None:
                    cursor.execute("""INSERT INTO Ingredients(name) VALUES('{0}')""".format(i))
                    db.commit()
            # go to view of new entry
            cursor.execute("""SELECT * FROM Recipes WHERE instructions='{0}'""".format(ins))
            rv = cursor.fetchone()
            rec_id = rv["recipeID"]
            db.close()
            return render_template('view_recipes.html', rec=rec_id, rv=rv)
        if request.args["can"] == "cancel":
            return render_template('index.html')
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)

