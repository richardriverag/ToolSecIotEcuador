from pymongo import MongoClient  # Conexión a la base de datos.

# Información del client de la base de datos.

client = 'test'
passdb = 'At3rpWYk4QYwQpW'
dbname = 'iotecuador'

# Conexión MongoAtlas.


def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb +"@cluster0.wdghc.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
        mydb = url_client.iotecuador

    except ConnectionError:
        print("Error de coneccion con el servidor: --->"+client)

    return mydb


def find_devices():
    db = get_db()  # Conexiíon a la BD
    search = db.Devices.find({"puerto.Puerto":"80"})
    for r in search:
        puertos = r['puerto']
        print("Puertos", puertos)



print("find_devices",find_devices())