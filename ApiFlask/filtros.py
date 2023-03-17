from pymongo import MongoClient  # Conexión a la base de datos.
import re
#from MongoCliente import getDevice_db
#Device client
#db = getDevice_db()

#funciones que faltan
def getDevice_db():
    client = 'client'
    passdb = 'kJwNCrAnmv4eXpwU'
    dbname = 'iotecuador'

    client = MongoClient("mongodb://localhost:27017/iotecuador")
    # get the database name
    db = client.get_database(dbname)
    # get the particular collection that contains the data
    Devicesdb = db.Devices
    return Devicesdb

db = getDevice_db()

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
            puerto = (str(x), cantidad)
            port_Info.append(puerto)

    return port_Info


def dataPort ():

    db = getDevice_db()

    PortList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                        1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                        1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                        69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

    data = []
    
    for port in PortList:
        countPort = db.find({'puerto.Puerto': str(port)})
        quantity = countPort.count()
        port_information = (port, quantity)
        data.append(port_information)
        
    return data


##Contraseña

def validar_password(password):
    if 8 <= len(password) <=16:
        if re.search('[a-z]', password) and re.search('[A-Z]', password):
            if re.search('[0-9]', password):
                if re.search('[$@#]', password):
                    return True

    return False

##map

def map():
    db = getDevice_db()
    capitalList =['Cuenca', 'Guaranda', 'Azogues', 'Tulcán', 'Riobamba', 'Latacunga', 'Machala', 'Esmeraldas',
                'Puerto Baquerizo Moreno', 'Guayaquil', 'Ibarra', 'Loja', 'Babahoyo', 'Portoviejo', 'Macas',
                'Tena', 'Francisco de Orellana', 'Puyo', 'Quito', 'Santa Elena', 'Santo Domingo', 'Nueva Loja',
                'Ambato', 'Zamora']

    codeCity = ['ec-az','ec-bo', 'ec-cn', 'ec-cr', 'ec-cb', 'ec-ct', 'ec-eo', 'ec-es', 'ec-ga', 'ec-gu', 'ec-im',
               'ec-lj', 'ec-lr', 'ec-mn', 'ec-ms', 'ec-1076', 'ec-na', 'ec-pa', 'ec-pi', 'ec-se', 'ec-sd', 'ec-su',
               'ec-tu', 'ec-zc' ]


    
    data = []


    for capital in capitalList:
        capital_filter = db.find({'Localizacion.city': capital, 'Estado': True})
        quantity = capital_filter.count()
        addInfo = quantity
        data.append(addInfo)

    #mostrar datos
    alldata =[]
    for contador in range(0, 24):
        capital = codeCity[contador]
        cantidad = data[contador]
        valor = [capital, cantidad]
        alldata.append(valor)

    return alldata



