import re
from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt 
from datetime import datetime
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

client = 'test'
passdb = 'At3rpWYk4QYwQpW'
dbname = 'mydb'
client = pymongo.MongoClient("mongodb+srv://jeff:Barcelona1925@cluster0.j8qp4.mongodb.net/mydb?retryWrites=true&w=majority")

#get the database name
db = client.get_database(dbname)
#get the particular collection that contains the data
Devicesdb = db.todos
Userdb = db.user



#inciar
@app.route("/")
def index():
    return render_template('Access/index.html')

#registrar
@app.route("/register", methods=['POST', 'GET'])
def register():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
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
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

            #get date_joined.
            date = datetime.now()

            #assing them in a dictionary in key value pairs
            user_input = {'last_login': date, 'username': username, 'first_name':"", 'last_name':"", 'email': email, 'password': hashed, 'is_active':True, 'date_joined': date}
            #insert it in the record collection
            Userdb.insert_one(user_input)
            
            #find the new created account and its email
            user_data = Userdb.find_one({"email": email})
            new_email = user_data['email']
            asset='activo'
            #if registered redirect to logged in as the registered user
            return render_template('Dashboard/home.html', email=new_email, assets=asset)
            
    return render_template('Access/register.html')



@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = Userdb.find_one({"email": email})

        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val

                #get date_joined.
                date = datetime.now()
                last_login = Userdb.update_one({"email": str(email_val)}, {"$set": {"last_login": date}})
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




#Dashboard
@app.route('/Dashboard')
def home():
    if "email" in session:
        email = session["email"]
        saved_todos = Devicesdb.find().limit(10)
        cantidad = saved_todos.count()
        asset = 'activo'
        return render_template('Dashboard/home.html', filters=saved_todos, cantidades = cantidad,email=email, assets=asset)
    else:
        return redirect(url_for("login"))


@app.route('/Dashboard/busqueda/<id>', methods=['GET'])
def get_info(id):
    todo_item = Devicesdb.find({'_id': ObjectId(id)})
    return render_template('Dashboard/busqueda.html', items = todo_item)



@app.route('/Dashboard', methods=['POST'])
def filter_info():
    filter = request.form.get('filter')
    parameter = request.form.get('parameter')

    if(str(parameter) == "Dirección"):
        todo_filter = Devicesdb.find({'Direccion': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        asset = 'activo'
        return render_template('Dashboard/home.html', filters=todo_filter, cantidades=cantidad, assets=asset)

    if(str(parameter) == "Puerto"):
    
        todo_filter = Devicesdb.find({'puerto.Puerto': filter})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        asset = 'activo'
        return render_template('Dashboard/home.html', filters=todo_filter, cantidades=cantidad,assets=asset)

    if(str(parameter) == "Cuidad"):

        capitalize = filter.capitalize()
        todo_filter = Devicesdb.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        asset = 'activo'
        return render_template('Dashboard/home.html', filters=todo_filter, cantidades=cantidad, assets=asset)

    if(str(parameter) == "GeoLocalización"):
   
        capitalize = filter.capitalize()
        todo_filter = Devicesdb.find({'Locatizacion.city': capitalize})
        cantidad = todo_filter.count()
        print("catidad", cantidad)
        asset = 'activo'
        return render_template('Dashboard/home.html', filters=todo_filter, cantidades=cantidad, assets=asset)

    else:
        msg = "Ups! algo salio mal :("
        asset = 'activo'
        return redirect(url_for('home'))

    
    
#User
@app.route("/setting", methods=['POST', 'GET'])
def user():




    asset = 'activo'
    return render_template('User/setting.html',assets = asset )
@app.route("/blog", methods=['GET'])
def blog():
    return render_template('Dashboard/blog.html')

@app.route("/rango_direcciones", methods=['GET'])
def rango():
    return render_template('Dashboard/direcciones.html')