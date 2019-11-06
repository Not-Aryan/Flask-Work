from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import random


app = Flask("jumbled--words")
app.config["MONGO_URI"]= "mongodb://127.0.0.1:27017/one-stop-db"
app.config['SECRET_KEY'] = 'same'

Bootstrap(app)


mongo = PyMongo(app)
@app.route('/', methods=["GET", "POST"])
def jw():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add-product.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            doc[item] = request.form[item]
        mongo.db.products.insert_one(doc)
        return redirect('/')

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'GET':
        session['cart-items'] = {}
        found_products = mongo.db.products.find()
        return render_template('buy.html', products=found_products)
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            if int(request.form[item] != 0):
                doc[item] = request.form[item]
    session['cart-items'] = doc
    return redirect('/checkout')

@app. route('/checkout')
def checkout():
total = 0
# Initializing the total amount to zero total — # An empty list to hold the information which will be delivered to the HTML page
cart_items = []
# Storing session information in a variable = session ['cart—items' stored info {ID: chosenquantity, ID: chosenquantity, .
stored_info = session['cart-items']

for ID in stored_info:
    found_item = mongo.db.items.find_one({ ' _ id' : Objectld(ID)})
    found_item ['bought'] = stored_info[ID]
    found_item['item—total'] = int(found_item['price']) * int(found_item['bought'])

    ''bought'] ) ca rt_items . append ( found _ item) total += ' item—total'] return render _ template( 'checkout. html' , p roducts=ca rt_items , total—total)


app.run(debug=True)
