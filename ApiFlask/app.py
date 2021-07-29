from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

def get_db():
    #Connection MongoDB
    client = 'test'
    passdb = 'At3rpWYk4QYwQpW'
    dbname = 'iotecuador'
    app.config['MONGO_URI'] = "mongodb+srv://"+client+":"+passdb +"@cluster0.wdghc.mongodb.net/"+dbname+"?retryWrites=true&w=majority"
    mongo = PyMongo(app)

    return mongo



@app.route('/')
def index():
    mydb = get_db()
    saved_todos = mydb.db.Devices.find()
    return render_template('index.html', todos=saved_todos)

@app.route('/complete/<oid>')
def complete(oid):
    mydb = get_db()
    todo_item = mydb.db.find_one({'_id': ObjectId(oid)})
    #todo_item['complete'] = True
    #todos.save(todo_item)
    print("Id: ",todo_item)
    return redirect(url_for('index'))
