import email
import os
import re
from flask import Flask, render_template, request, url_for, redirect, session
import bcrypt 
from datetime import date, datetime
from bson.objectid import ObjectId
from pymongo import message
from filtros import getDevice_db, getClient_db, datainfo, datacity, validar_password, map
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from functools import wraps
from flask_mail import Mail, Message



app = Flask(__name__)
#app.secret_key
key = os.urandom(24)
app.secret_key = key

mail_settigns = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_SSL": True,
        "MAIL_USE_TLS": False,
        "MAIL_USERNAME": 'iotecuador2021@gmail.com',
        "MAIL_PASSWORD": 'HU#qf^OP8mwV',
        "MAIL_DEFAULT_SENDER": 'iotecuador2021@gmail.com'
}

app.config.update(mail_settigns)
mail = Mail(app)

#Device client
Devicesdb = getDevice_db()

#Device User
Userdb = getClient_db()

#Data info
varIpv4 = datainfo

#Data info
varGeoCity = datacity

#Validar Pass
validar_pass = validar_password

#Map
mapEcuador = map()



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    u = Userdb.find_one({"email": username})
    if not u:
        return None
    return User(username = u['email'], role=u['role'], id=u['_id'])


class User:
    def __init__(self, id, username, role) -> None:
        self.id = id
        self.username = username
        self.role = role

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username



### custom wrap to determine role access  ### 
def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if not current_user.is_authenticated:
                #print('The user is not authenticated.')
                return redirect(url_for('login'))
            
            #print(current_user.role)
            #print(role_names)
            if not current_user.role in role_names:
                #print('The user does not have this role.')
                return redirect(url_for('login'))
            else:
                #print('The user is in this role.')
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator




# inciar
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('Access/index.html', capilalizes=mapEcuador)


# registrar
@app.route("/register", methods=['POST', 'GET'])
def register():
    message = ''
    
    # if method post in index
    if current_user.is_authenticated:
        message = 'Revise su correo en Span'
        return render_template('Access/login.html', message=message)

    if request.method == "POST":
        username = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        msg = request.form.get("texto")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #TEXTBOX DEL porq quieres usar el sistema.

        # if found in database showcase that it's found
        user_found = Userdb.find_one({"name": username})
        email_found = Userdb.find_one({"email": email})

        if username == "" and lastname == "" and email == "" and msg == "" and password1 == "" and password2 == "":
            message = 'Todos los campos estan vacios'
            return render_template('Access/register.html', message=message)
        
        if username == "" or lastname == "" or email == "" or msg == "" or password1 == "" or password2 == "":
            message = 'Ninguno de los campos debe estar vacio'
            return render_template('Access/register.html', message=message)

        if email_found:
            message = 'Ya! Existe un usuario con ese email'
            return render_template('Access/register.html', message=message)

        if password1 != password2:
            message = 'Las contraseñas no coinciden'
            return render_template('Access/register.html', message=message)
        
    
        if  validar_pass(password1) == False: 
            message = 'La contraseña no es segura: Min 8 Caracteres, una letra mayusculas y un número y un caracter especial '
            return render_template('Access/register.html', message=message)

        if "@" in email and "." in email:
            
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

            # get date_joined.
            date = datetime.now()

            # assing them in a dictionary in key value pairs
            user_input = {'last_login': date, 'username': None, 'first_name': username, 'last_name': lastname, 'msg': msg, 
                          'email': email, 'password': hashed, 'is_active': False, 'date_joined': date, 'role': "user"}
            # insert it in the record collection
            Userdb.insert_one(user_input)

            # find the new created account and its email
            #user_data = Userdb.find_one({"email": email})
            #email_val= user_data['email']

            message = 'En un máximo de 48 horas se enviara una respuesta a su correo:', email
            return render_template('Access/login.html', message=message)
        else:
            message = 'El email no es correcto'
    
        return render_template('Access/register.html', message=message)

    return render_template('Access/register.html')


# ingresar

@app.route("/login", methods=["POST", "GET"])
def login():

    message = ''
    if request.method == "POST":


        email = request.form.get("email")
        password = request.form.get("password")

        
        if email == "" and password == "":
            message = 'Todos los campos estan vacios'
            return render_template('Access/login.html', message=message)

        if email == "" or password == "":
            message = 'Ninguno de los campos debe estar vacio'
            return render_template('Access/login.html', message=message)

        if "@" in email:
            
            # check if email exists in database
            email_found = Userdb.find_one({"email": email})
            is_active = email_found['is_active']

            if is_active == True:
                if email_found:
                    email_val = email_found['email']
                    passwordcheck = email_found['password']
                    # encode the password and check if it matches
                    if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                        session["email"] = email_val
                        user_obj = User(username=email_found['email'], role=email_found['role'], id=email_found['_id'])
                        login_user(user_obj)
                        # get date_joined.
                        date = datetime.now()
                        last_login = Userdb.update_one({"email": str(email_val)}, {
                                                    "$set": {"last_login": date}})
                        return redirect(url_for('home'))
                    else:
                        if current_user.is_authenticated:
                            return redirect(url_for("home"))
                        message = 'Wrong password'
                        return render_template('Access/login.html', message=message)
                else:
                    message = 'Email not found'
            else:
                message = 'Aún no se autoriza su cuenta'
        else:
                message = 'El correo no es válido'
            
        return render_template('Access/login.html', message=message)
    return render_template('Access/login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('index'))



# Dashboard
@app.route('/dashboard')
@login_required
@roles_required('user', 'admin')
def home():

    #validación de correo
    if current_user.is_authenticated:
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

        return render_template('dashboard/home.html', filters=Ipv4True, datos=data, users=info_user)
    else:
        return redirect(url_for("login"))

# busqueda por dirección Ipv4 Estado:True
@app.route('/dashboard/ipv4/<id>', methods=['GET'])
@login_required
@roles_required('user', 'admin')
def get_ipv4(id):
    if current_user.is_authenticated:
        todo_Ipv4 = Devicesdb.find({'_id': ObjectId(id)})
        return render_template('dashboard/busqueda.html', items=todo_Ipv4)
    else:
        return redirect(url_for('home'))


@app.route('/dashboard', methods=['POST'])
@login_required
@roles_required('user', 'admin')
def filter_info():
    #obtener parametros
    filter = request.form.get('filter')
    parameter = request.form.get('parameter')

    if current_user.is_authenticated:

        # Busqueda por dirección IPv4
        if(str(parameter) == "Dirección"):
                # filtro
            todo_filter = Devicesdb.find({'Direccion': filter})
            cantidad = todo_filter.count()
            data = varIpv4(cantidad, filter)

            return render_template('dashboard/home.html', filters=todo_filter,datos = data) 


        # Busqueda por dirección Puerto
        if(str(parameter) == "Puerto"):

            todo_filter = Devicesdb.find({'puerto.Puerto': filter})
            cantidad = todo_filter.count()
            data = varIpv4(cantidad, filter)

            return render_template('dashboard/home.html', filters=todo_filter, datos=data)


        #Busqueda por Cuidad
        if(str(parameter) == "Cuidad"):
            #Hacer que la primera letra sea Mayúscula
            capitalize = filter.capitalize()
            #Filtro por cuidad
            todo_filter = Devicesdb.find({'Localizacion.city': capitalize, 'Estado': True})
            cantidad = todo_filter.count()

            cityPort = varGeoCity(capitalize)

            # Contenedor de información 
            data = varIpv4(cantidad, filter)

            return render_template('dashboard/home.html', filters=todo_filter, cities = cityPort, datos=data)

        else:
            message = "Ups! algo salio mal :("
            return render_template(url_for('home', message))

    else:
        return redirect(url_for('home'))

#Admin Panel

# inciar
@app.route("/admin_panel", methods=["POST", "GET"])
@login_required
@roles_required('admin')
def admin_panel():
    if current_user.is_authenticated:
        email = session["email"]

        # Obtener información de usuario 
        user_found = Userdb.find({'role': "user"})

        return render_template('Admin/admin_panel.html', userslist = user_found)
    return redirect(url_for('index'))

# busqueda por dirección Ipv4 Estado:True
@app.route('/admin_panel/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def get_user(id):
    message = ''
    if current_user.is_authenticated:

        user_info = Userdb.find_one({'_id': ObjectId(id)})

        estado = user_info['is_active']
        email = user_info['email']
        name = user_info['first_name']
        last_name = user_info['last_name']
        user = [{
            'Name': name,
            'Last_name':last_name,
        }]
        
        if estado == False:
            Userdb.update_one({'_id': ObjectId(id)}, {"$set": {'is_active': True}})
            msg = Message(subject="Cuenta Activada!", recipients=[str(email)])
            msg.html = render_template('Mail/active_account.html', users=user)
            mail.send(msg)

            msg = Message(
                subject = '',
                recipients = [],
                body = '',
                html = '',
                sender = '',
                cc = [],
                bcc = [],
                attachments = [],
                reply_to = [],
                date = 'date',
                charset='',
                extra_headers={'':''},
                mail_options=[],
                rcpt_options=[]

            )

            message = 'Se ha enviado un correo a ', email
            return redirect(url_for("admin_panel"))

        else:
            Userdb.update_one({'_id': ObjectId(id)}, {"$set": {'is_active': False}})
            return redirect(url_for("admin_panel"))

    else:
        return redirect(url_for('login'))




# Actulizar InfoUser
@app.route("/profile", methods=['POST', 'GET'])
@login_required
@roles_required('user', 'admin')
def profile_user():
  
    email = session["email"]
    user_found = Userdb.find({"email": email})


    if request.method == "POST":
        newusername = request.form.get("name")
        newlastname = request.form.get("lastname")
        newemail = request.form.get("email")


        if newusername == "" and newlastname == "" and newemail == "":
            message = 'Todos los campos estan vacios'
            return render_template('User/profile.html', users = user_found, message=message)
        
        email_found = Userdb.find_one({"email": email})
        name = email_found['first_name']
        lastname = email_found['last_name']
        email = email_found['email']

        if newusername == name and newlastname == lastname and newemail == email:
            message = 'NO realizo ningun cambio'
            return render_template('User/profile.html', users = user_found, message=message)

        
        if newusername == "" or newlastname == "" or newemail == "" :
            message = 'Ninguno de los campos debe estar vacio'
            return render_template('User/profile.html', users=user_found, message=message)
        
        if "@" in newemail and "." in newemail:

            email_found = Userdb.find_one({"email": email})
            id = email_found['_id']

            if email_found:
                Userdb.update_one({'_id':ObjectId(id)}, {"$set": {'first_name': newusername, 'last_name': newlastname,'email': newemail}})

                message = 'Perfil Actualizado'
                return render_template('User/profile.html',users= user_found,  message=message)
                    
            else:
                return redirect(url_for("index"))
        else:
            message = 'El email no es correcto'

        return render_template('User/profile.html', users=user_found, message=message)

    return render_template('User/profile.html', users = user_found )

            


# Actulizar Contraseña
@app.route("/password", methods=['POST', 'GET'])
@login_required
@roles_required('user', 'admin')
def password_user():

    email = session["email"]
    email_found = Userdb.find_one({"email": email})

    if request.method == "POST":
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        repetpass = request.form.get("repetpass")


        passwordcheck = email_found['password']

        if oldpass == "" and newpass == "" and repetpass == "":
            message = 'Todos los campos estan vacios'
            return render_template('User/password.html', message=message)

        if oldpass == "" or newpass == "" or repetpass == "":
            message = 'Ninguno de los campos debe estar vacio'
            return render_template('User/password.html', message=message)

        if newpass != repetpass:
            message = 'Las contraseñas no coinciden'
            return render_template('User/password.html', message=message)
        
    
        if  validar_pass(newpass) == False: 
            message = 'La contraseña no es segura: Min 8 Caracteres, una letra mayusculas y un número y un caracter especial '
            return render_template('User/password.html', message=message)


        else:

            if bcrypt.checkpw(oldpass.encode('utf-8'), passwordcheck):
                if(newpass != "" or repetpass != ""):
                    email_found = Userdb.find_one({"email": email})
                    id = email_found['_id']
                    hashed = bcrypt.hashpw(repetpass.encode('utf-8'), bcrypt.gensalt())
                    Userdb.update_one({'_id':ObjectId(id)}, {"$set": {'password': hashed}})
                    message = 'Contraseña Actualizada'
                    return render_template('User/password.html', message=message)
                else:
                    message = 'La nueva contraseña esta vacia'
                return render_template('User/password.html', message=message)

            else:
                message = 'No coincide tu contraseña anterior'
                return render_template('User/password.html', message=message)
        
    return render_template('User/password.html')



@app.route("/blog", methods=['GET'])
@login_required
@roles_required('user', 'admin')
def blog():
    return render_template('dashboard/blog.html')

@app.route("/rango_direcciones", methods=['GET'])
@login_required
@roles_required('user', 'admin')
def rango():
    return render_template('dashboard/direcciones.html')