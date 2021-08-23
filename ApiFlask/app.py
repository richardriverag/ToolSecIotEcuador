import json
import os
from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt 
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps, loads



app = Flask(__name__)
key = os.urandom(24)
app.secret_key = key
#app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

client = 'client'
passdb = 'kJwNCrAnmv4eXpwU'
dbname = 'iotecuador'

client = pymongo.MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
# get the database name
db = client.get_database(dbname)
# get the particular collection that contains the data
Devicesdb = db.Devices
Userdb = db.User


# inciar
@app.route("/")
def index():
    return render_template('Access/index.html')


# registrar
@app.route("/register", methods=['POST', 'GET'])
def register():
    message = ''
    # if method post in index
    if "email" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # if found in database showcase that it's found
        user_found = Userdb.find_one({"name": username})
        email_found = Userdb.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('Access/register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('Access/register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('Access/register.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

            # get date_joined.
            date = datetime.now()

            # assing them in a dictionary in key value pairs
            user_input = {'last_login': date, 'username': username, 'first_name': "", 'last_name': "",
                          'email': email, 'password': hashed, 'is_active': True, 'date_joined': date}
            # insert it in the record collection
            Userdb.insert_one(user_input)

            # find the new created account and its email
            user_data = Userdb.find_one({"email": email})
            email_val= user_data['email']
            info_user = user_data['username']
            asset = 'activo'
            session["email"] = email_val
            # if registered redirect to logged in as the registered user
            #return render_template('dashboard/home.html', users=info_user, assets=asset)
            return redirect(url_for('home'))

    return render_template('Access/register.html')


# ingresar
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = Userdb.find_one({"email": email})

        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val

                # get date_joined.
                date = datetime.now()
                last_login = Userdb.update_one({"email": str(email_val)}, {
                                               "$set": {"last_login": date}})
                return redirect(url_for('home'))
            else:
                if "email" in session:
                    return redirect(url_for("home"))
                message = 'Wrong password'
                return render_template('Access/login.html', message=message)
        else:
            message = 'Email not found'

            return render_template('Access/login.html', message=message)
    return render_template('Access/login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("Access/index.html")
    else:
        return render_template('Access/register.html')



# Dashboard
@app.route('/dashboard')
def home():

    #validación de correo
    if "email" in session:
        email = session["email"]

        # Obtener información de usuario 
        user_found = Userdb.find_one({"email": email})
        info_user = user_found['username']

        # Listar 10 direcciones "Estado":True
        Ipv4True = Devicesdb.find({'Estado': True}).limit(10)
        cantidad = Ipv4True.count()
        
        # Listar todas la direcciones IPv4 Analizadas

        # Contenedor de información 
        data = datainfo(cantidad, "")

        #activar rutas.
        assetUrl = 'activo'

        return render_template('dashboard/home.html', filters=Ipv4True, datos=data, users=info_user, assets=assetUrl)
    else:
        return redirect(url_for("login"))

# busqueda por dirección Ipv4 Estado:True
@app.route('/dashboard/ipv4/<id>', methods=['GET'])
def get_ipv4(id):
    if "email" in session:
        todo_Ipv4 = Devicesdb.find({'_id': ObjectId(id)})
        return render_template('dashboard/busqueda.html', items=todo_Ipv4)
    else:
        return redirect(url_for('home'))


@app.route('/dashboard', methods=['POST'])
def filter_info():
    #obtener parametros
    filter = request.form.get('filter')
    parameter = request.form.get('parameter')

    # Busqueda por dirección IPv4
    if(str(parameter) == "Dirección"):
            # filtro
        todo_filter = Devicesdb.find({'Direccion': filter})
        cantidad = todo_filter.count()
        data = varIpv4(cantidad, filter)
        asset = 'activo'
        return render_template('dashboard/home.html', filters=todo_filter,datos = data, assets=asset,) 


    # Busqueda por dirección Puerto
    if(str(parameter) == "Puerto"):

        todo_filter = Devicesdb.find({'puerto.Puerto': filter})
        cantidad = todo_filter.count()
        data = varIpv4(cantidad, filter)
        asset = 'activo'
        return render_template('dashboard/home.html', filters=todo_filter,datos=data, assets=asset)


    #Busqueda por Cuidad
    if(str(parameter) == "Cuidad"):
        #Hacer que la primera letra sea Mayúscula
        capitalize = filter.capitalize()
        #Filtro por cuidad
        todo_filter = Devicesdb.find({'Locatizacion.city': capitalize, 'Estado': True})
        cantidad = todo_filter.count()

        cityPort = varGeoCity(capitalize)

        print("cantiad de Puertos", cityPort)
        
        # Contenedor de información 
        data = varIpv4(cantidad, filter)
        asset = 'activo'
        return render_template('dashboard/home.html', filters=todo_filter, cities = cityPort, datos=data, assets=asset)

    else:
        msg = "Ups! algo salio mal :("
        asset = 'activo'
        return redirect(url_for('home'))


# Actulizar InfoUser
@app.route("/setting", methods=['POST', 'GET'])
def user():
    asset = 'activo'
    return render_template('user/setting.html', assets=asset)


# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-es

@app.route("/blog", methods=['GET'])
def blog():
    return render_template('dashboard/blog.html')

@app.route("/rango_direcciones", methods=['GET'])
def rango():
    return render_template('dashboard/direcciones.html')


#filtro de número de direcciones
def datainfo(cantidad, filter):
    AllIPv4 = Devicesdb.find().count()
    dataInfo = [
            {
                'PuertoTrue': cantidad,
                'AllIPv4': AllIPv4,
                'Filter': filter
            }
            
        ]

    return dataInfo

varIpv4 = datainfo


#filtro por cuidades

def datacity(capitalize):
    #filtrado que muestre solo los puertos.
    #cluster = Devicesdb.find({'Locatizacion.city': capitalize, 'Estado': True},
                            #{"puerto.Puerto":1})

    PortsList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                 1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                 1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                 69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

    port_Info = []

    for x in PortsList:
        #Filtro
        port_filter = Devicesdb.find({'Locatizacion.city': capitalize, 'puerto.Puerto': str(x) })
        #Cantidad de Puertos
        cantidad = port_filter.count()
        if cantidad != 0:
            #add port_info
            puerto = {"Puerto": str(x), "Cantidad": cantidad}
            port_Info.append(puerto)

    return port_Info

varGeoCity = datacity
