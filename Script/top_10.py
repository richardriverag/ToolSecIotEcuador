
from pymongo import MongoClient  # Conexión a la base de datos.
import re
from MongoCliente import get_db
db = get_db()  # Conexiíon a la BD

PortList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                        1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                        1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                        69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

data = []

def ranking():
    for port in PortList:
        countPort = db.Devices.find({'puerto.Puerto': str(port)})
        quantity = countPort.count()
        port_information = {'port': str(port), 'sum': str(quantity)}
        print(port_information)
        data.append(port_information)

    print(data)

print(ranking())