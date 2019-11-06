from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import random


app = Flask("jumbled--words")
app.config["MONGO_URI"]= "mongodb://127.0.0.1:27017/jumbled-words-db"

Bootstrap(app)


mongo = PyMongo(app)
@app.route('/', methods=["GET", "POST"])
def jw():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/jumble', methods=['GET', 'POST'])
def jumble():
    if request.method == 'GET':
        return render_template('jw.html')
    elif request.method == 'POST':
        print("HI")
        doc = {'word': request.form['word'].strip().upper()}
        mongo.db.words.insert_one(doc)
        return redirect('/')

@app.route('/figureout', methods=['GET', 'POST'])
def figureout():
    found_docs = list(mongo.db.words.find())
    total_words = len(found_docs)
    print(total_words, found_docs)
    if request.method == "GET":
        for doc in found_docs:
            jwl = list(doc['word'])
            random.shuffle(jwl)
            jw = ''.join(jwl)
            doc['word'] = jw
        return render_template('findwords.html', docs=found_docs, count=total_words)
    elif request.method == 'POST':
        score = 0
        ua = []
        found_docs = list(mongo.db.words.find())
        data = request.form.to_dict(flat = False)
        print(data)
        # print(len(data))
        # print(request.form)
        for i in data['word']:
            print(i)
            ua.append(i.strip().upper())
        # print(ua)
        for index in range(len(ua)):
            if ua[index] == found_docs[index]['word']:
                score += 1
        return render_template('results.html', score=str(score))

app.run(debug=True)
