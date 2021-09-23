from enum import unique
from os import name
from pymongo import MongoClient # Conexión a la base de datos.
import re

import pymongo


client = 'client'
passdb = 'kJwNCrAnmv4eXpwU'
dbname = 'iotecuador'

client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
# get the database name
db = client.get_database(dbname)
# get the particular collection that contains the data
#db.Devices.create_index([("Direccion", pymongo.DESCENDING)], name="'IPv4'", unique=True)
#email_found = Userdb.find_one({"email": email})

#db.User.create_index([("email", pymongo.ASCENDING)], name="'Correo'", unique=True)
