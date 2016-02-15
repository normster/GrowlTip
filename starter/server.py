import sqlite3
import time
from flask import Flask, request, g, render_template
from blockchain import wallet

app = Flask(__name__)
DATABASE = 'growls.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def db_read_growls():
    cur = get_db().cursor()
    cur.execute("CREATE TABLE if not EXISTS growls (name TEXT, datetime TEXT, growl TEXT)")
    cur.execute("SELECT * FROM growls")
    return cur.fetchall()

def db_add_growl(name, growl):
    cur = get_db().cursor()
    t = str(time.time())
    growl_info = (name, t, growl)
    cur.execute("INSERT INTO growls VALUES (?, ?, ?)", growl_info)
    get_db().commit()

@app.route("/")
def hello():
    growls = db_read_growls()
    print(growls)
    return render_template('index.html', growls=growls)

@app.route("/", methods=["POST"])
def testing():
    print(request.form)
    db_add_growl(request.form['name'], request.form['growl'])
    return hello()

if __name__ == "__main__":
    app.debug = True
    app.run()
