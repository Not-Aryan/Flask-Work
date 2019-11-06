from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId



app = Flask("address-book")
app.config["MONGO_URI"]= "mongodb://127.0.0.1:27017/my-address-book-db"

Bootstrap(app)

mongo = PyMongo(app)

@app.route('/', methods=["GET", "POST"])
def note_saver():
    if request.method == "GET":
        contacts = mongo.db.mycontacts.find()
        return render_template('index.html', contacts=contacts)
    elif request.method == "POST":
        document = {}
        for item in request.form:
            document[item] = request.form[item]
        mongo.db.mycontacts.insert_one(document)
        return redirect('/')

@app.route('/delete/<identity>')
def delete_contact(identity):
    found = mongo.db.mycontacts.find_one({'_id': ObjectId(identity)})
    mongo.db.mycontacts.remove(found)
    return redirect('/')

app.run(debug=True)
