from pymongo import MongoClient  # Conexión a la base de datos.
import logging
from pymongo.errors import ServerSelectionTimeoutError

client = 'admin'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'iotecuador'

# Generar información de diagnostico para scripts con el módulo logging.
logging.basicConfig(filename='logs/iotInfo.log', level='INFO',
                    format='%(asctime)s: %(levelname)s: %(message)s')

# Conexión MongoAtlas.

def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?ssl=true&ssl_cert_reqs=CERT_NONE")
        mydb = url_client.iotecuador

    except Exception:
        logging.error(
            'No se puede conectar con la DataBase: %s. Verifique el cliente de conexion: get_db()', dbname)
        exit(1)

    except ServerSelectionTimeoutError as e:
        logging.error(
            'No se puede conectar con la DataBase: %s. Verifique su conexion', dbname)
        exit(1)
    return mydb