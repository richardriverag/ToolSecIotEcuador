from dns import ipv4
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket

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
    saved_todos = mydb.db.Devices.find().limit(10)
    cantidad = saved_todos .count()
    return render_template('index.html', filters=saved_todos, cantidades = cantidad)



@app.route('/busqueda/<id>', methods=['GET'])
def get_info(id):
    mydb = get_db()
    todo_item = mydb.db.Devices.find({'_id': ObjectId(id)})
    return render_template('busqueda.html', items = todo_item)




@app.route('/', methods=['POST'])
def filter_info():
    filter = request.form.get('filter')
    parameter = request.form.get('parameter')

    if(str(parameter) == "Dirección"):
        mydb = get_db()
        todo_filter = mydb.db.Devices.find({'Direccion': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "Puerto"):
        mydb = get_db()
        todo_filter = mydb.db.Devices.find({'puerto.Puerto': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "Cuidad"):
        mydb = get_db()
        capitalize = filter.capitalize()
        todo_filter = mydb.db.Devices.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    if(str(parameter) == "GeoLocalización"):
        mydb = get_db()
        capitalize = filter.capitalize()
        todo_filter = mydb.db.Devices.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        return render_template('index.html', filters=todo_filter, cantidades=cantidad)

    else:
        msg = "Ups! algo salio mal :("
        return redirect(url_for('index'))

    
    