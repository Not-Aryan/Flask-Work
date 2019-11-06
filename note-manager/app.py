from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

app = Flask("note-manager")
app.config["MONGO_URI"]= "mongodb://127.0.0.1:27017/my-address-book-db"

Bootstrap(app)

mongo = PyMongo(app)

@app.route('/', methods=["GET", "POST"])
def note_saver():
    if request.method == "GET":
        documents = mongo.db.NoteCollection.find()
        return render_template('index.html', savedNotes=documents)
    elif request.method == "POST":
        document = {}
        for item in request.form:
            document[item] = request.form[item]
        mongo.db.NoteCollection.insert_one(document)
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)