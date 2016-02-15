import sqlite3
import time
from flask import Flask, request, g, render_template
from blockchain import wallet


tip_amount = 110000 #amount in Satoshi 
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
    cur.execute("CREATE TABLE if not EXISTS growls (name TEXT, datetime TEXT, growl TEXT, wallet TEXT)")
    cur.execute("SELECT * FROM growls")
    return cur.fetchall()

def db_add_growl(name, growl, wallet):
    cur = get_db().cursor()
    t = str(time.time())
    growl_info = (name, t, growl, wallet)
    cur.execute("INSERT INTO growls VALUES (?, ?, ?, ?)", growl_info)
    get_db().commit()

def db_get_dest_address(this_growl, time):
    cur = get_db.cursor()
    cur.execute("SELECT wallet FROM growls where datetime = time AND growl= this_growl")


@app.route("/")
def hello():
    growls = db_read_growls()
    print(growls)
    return render_template('index.html', growls=growls)

@app.route("/", methods=["POST"])
def testing():
    print(request.form)
    db_add_growl(request.form['name'], request.form['growl'], request.form['wallet'])
    return hello()


@app.route("/api/growl", methods=["POST"])
def receive_growl():
    print(request.form)
    db_add_growl(request.form['name'], request.form['growl'], request.form['wallet'])
    return hello()
    # TODO: redirect to "/"

@app.route("/api/tip/<dest_wallet>", methods=["POST"])
def send_tip(dest_wallet):
    print(request.form)
    identifier = request.form['identifier']
    password = request.form['password']
    amount = request.form['amount']
    wal = wallet.Wallet("{0}".format(identifier), "{0}".format(password))
    wal.send(dest_wallet, amount)
    print("Sending " + amount + " Satoshis from " + wal.list_addresses + " to " + dest_wallet)
    return hello()
    

@app.route("/tip/<dest_wallet>")
def tip_login(dest_wallet):
    return render_template('tip.html', dest_wallet  = dest_wallet)

if __name__ == "__main__":
    app.debug = True
    app.run()
