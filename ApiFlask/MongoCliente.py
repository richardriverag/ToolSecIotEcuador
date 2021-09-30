from pymongo import MongoClient  # Conexión a la base de datos.
import re

def getDevice_db():
    client = 'client'
    passdb = 'kJwNCrAnmv4eXpwU'
    dbname = 'iotecuador'

    client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?ssl=true&ssl_cert_reqs=CERT_NONE")
    # get the database name
    db = client.get_database(dbname)
    # get the particular collection that contains the data
    Devicesdb = db.Devices
    return Devicesdb


def getClient_db():

    client = 'client'
    passdb = 'kJwNCrAnmv4eXpwU'
    dbname = 'iotecuador'
    client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?ssl=true&ssl_cert_reqs=CERT_NONE")
    # get the database name
    db = client.get_database(dbname)
    # get the particular collection that contains the data
    Userdb = db.User
    return Userdb