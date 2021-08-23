from pymongo import MongoClient  # Conexión a la base de datos.

def getDevice_db():
    client = 'client'
    passdb = 'kJwNCrAnmv4eXpwU'
    dbname = 'iotecuador'

    client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
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
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
    # get the database name
    db = client.get_database(dbname)
    # get the particular collection that contains the data
    Userdb = db.User
    return Userdb

    
#filtro de número de direcciones
def datainfo(cantidad, filter):
    db = getDevice_db()
    AllIPv4 = db.find().count()
    dataInfo = [
            {
                'PuertoTrue': cantidad,
                'AllIPv4': AllIPv4,
                'Filter': filter
            }
            
        ]

    return dataInfo


#filtro por cuidades

def datacity(capitalize):
    
    db = getDevice_db()

    PortsList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                 1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                 1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                 69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

    port_Info = []

    for x in PortsList:
        #Filtro
        port_filter = db.find({'Localizacion.city': capitalize, 'puerto.Puerto': str(x) })
        #Cantidad de Puertos
        cantidad = port_filter.count()
        if cantidad != 0:
            #add port_info
            puerto = {"Puerto": str(x), "Cantidad": cantidad}
            port_Info.append(puerto)

    return port_Info

