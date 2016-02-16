# GrowlTip

Today we are building GrowlTip, a simple ChangeTip clone within Growler, made by Hackers @ Berkeley. Growler is itself a clone of Twitter, written in Flask. We will be building on top of the completed Growler app, and as such we assume you have some basic familiarity with Python and the Flask framework. If you would like a refresher, take a look at the original tutorial for building Growler, available at [https://github.com/HackBerkeley/Growler](https://github.com/HackBerkeley/Growler).

If you get stuck or don't understand something at any point in this workshop, please do ask us. Chances are someone else is also confused or stuck.

# Step 1: Make sure you have Python 3.5

**You probably already have Python 3.5 installed** if you're taking CS 61A. To check, type

    python3 --version
in your command line.

- If you have Python 3.5 or greater, go to the next step.
- If you do not have Python 3.5 or greater, you will need to install it. To install Python:

### Windows or Mac
Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) and click the big yellow download button for Python 3. Then install it.

### Linux
Type `sudo apt-get install python3` in your Terminal.

# Step 2: Install Dependencies (flask and blockchain)

First, what exactly is a web framework? When a person goes to a website, they send what's called an *HTTP request* to that website, asking for the site's content. Our web framework, Flask, will handle requests that are sent to us, and send back our site's content via an *HTTP response*.

Flask is a web framework for Python. It makes it really easy to write web apps. Let's get it installed.

In your command line, type

    pip3 install flask

- If you get the error `'pip3' is not recognized as an internal or external command` blah blah blah, you're probably using Windows. You will need to set your PATH variable so that Windows can locate pip3. You will need to add `C:\<Your Python installation directory here>\Scripts\` to your PATH variable. Ask Google, or your neighbor if you're unsure of how to do this, or ask a mentor if you're really stuck.

Now we need to install Blockchain.info's `blockchain` package to make calls to their platform.

In your command line, type

    pip3 install blockchain

# Step 3: Get the starter code

If you've used Git, clone this repo and look in the `starter` folder. Otherwise, download and unzip this zip file [https://www.dropbox.com/s/2yzqa65f3ccmwx6/starter.zip?dl=0](https://www.dropbox.com/s/2yzqa65f3ccmwx6/starter.zip?dl=0)

# Step 4: Include wallet info for each growl

To start, we will modify our database to include one more piece of information. In order to receive payments, the growler must include their receiving wallet address so let's modify our SQL query in `server.py` when we create the SQL table.

```python
def db_read_growls():
    cur = get_db().cursor()
    cur.execute("CREATE TABLE if not EXISTS growls (name TEXT, datetime TEXT, growl TEXT, wallet TEXT)")
    cur.execute("SELECT * FROM growls")
    return cur.fetchall()
```

And also when we add new growls. 

```python
def db_add_growl(name, growl, wallet):
    cur = get_db().cursor()
    t = str(time.time())
    growl_info = (name, t, growl, wallet)
    cur.execute("INSERT INTO growls VALUES (?, ?, ?, ?)", growl_info)
    get_db().commit()
```

Now that we've added support for wallet addresses, we have to edit our `index.html` page to accept the new information when people send a new growl. 

```html 
    <input name="growl" type="text" maxlength="76" />
    <br></br>
    Your wallet ID:
    <input name="wallet" type="text" />
    <br></br>
```

# Step 5:  Add a tip button to each growl
We will start by creating a redirect to a new tip page in `server.py`. Like `hello()` we will create a new `app.route`.

```python 
@app.route("/tip/<dest_wallet>")
def tip_login(dest_wallet):
    return render_template('tip.html', dest_wallet  = dest_wallet)
```

Here we are doing a little tricky Flask magic by using variable route. The `<dest_wallet>` allows us to pass the value of the user's wallet address through to the actual tip page. 
 
Next, we will add a button giving users the ability to tip each growl. We will edit the flask `for` loop in `index.html`. This button must redirect the page to the `/tip/<dest_wallet>`. 

```html
{% for growl in growls %}
        <div class="growl">
            <b>{{ growl[0] }}</b>
            <p>{{ growl[2] }}</p>
            <form action='/tip/{{ growl[3] }}'  method='GET'>
              <input type="submit" value="Tip Me"/>
            </form>
        </div>
        {% endfor %}
```
        
The `action='/tip/{{ growl[3] }}` access the database and retrieves the corresponding wallet address and redirects to the `tip.html` file we will be creating next. 

# Step 6: Create a Tip Login Page
We will now create a tip page where a user can login to their blockchain.info wallet and send a variable amount of btc to the user who wrote a growl. 

Create a new file called `tip.html` in the `templates` folder. We can copy over the `<head>` info from `index.html`. The `<body>` will contain 3 fields, blockchain.info identifier, password, and amount to send. 

```html 
  <body>
    <h1>GrowlTip</h1>
    <div id="feed">
      <h2>Enter information below</h2>
      <form action="/api/tip/{{ dest_wallet }}" method="POST">
        Blockchain wallet identifier:
        <input name="identifier" type="text">
        <br></br>
        Password:
        <input name="password" type="password">
        <br></br>
        Amount in Satoshis:
        <input name="amount" type="number">
        <br></br>
        <input type="submit"/>
      </form>
    </div>
  </body>
```

The Blockchain wallet identifier is not the address of the wallet itself, but rather a unique identifier used to login to a blockchain.info wallet. This allows us to use the Blockchain.info API to send. 

Satoshi is one of the smallest representation of bitcoins that is publicly used. They represent an easier way to deal with bitcoin when talking about prices. The transaction fee for using blockchain.info is 10000 satoshis or about $0.04 at the writing of this README (February 15, 2015), thus the value in the satoshis must be greater than 10000 for it to be confirmed on the bitcoin network. 


# Step 7: Create the API call
The final step is to link the Blockchain API to the account and make the payment to the Growler. In `server.py`, we will add a final route that will make the API call and return you back to the homepage. 

```python 
@app.route("/tip/<dest_wallet>", methods=["POST"])
def send_tip(dest_wallet):
    print(request.form)
    identifier = request.form['identifier']
    password = request.form['password']
    amount = request.form['amount']
    wal = wallet.Wallet("{0}".format(identifier), "{0}".format(password))
    wal.send(dest_wallet, amount)
    print("\n\nSending " + str(amount) + " Satoshis to " + str(dest_wallet) + "\n\n")
    return hello()
```


Congratulations, you have officially made a Bitcoin app! Beware that you will waste a lot of money by repeatedly using the app since transaction fees eat into your bitcoin balance. However, you can take my word that this does in fact work. 

## Future Modifications
I honestly don't know? Make ChangeTip all over again and steal their users or something




