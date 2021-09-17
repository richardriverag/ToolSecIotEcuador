import logging
from selenium.webdriver.chrome import options
from bcolor import bcolors  # Clase contenedora de los colores.
from atributos import Device  # Clase atributos.
from pymongo import MongoClient  # Conexión a la base de datos.
from pymongo.errors import ServerSelectionTimeoutError
import sys
import getpass  # Obtener información del usuario
# pip install alive_progress & pip install tqdm
from alive_progress import alive_bar
from time import sleep
from icecream import ic  # Debug de codigo.
import colorama  # Imprime texto en colores.
import pyfiglet  # Modificar la forma del Título.
from dns import reversename  # Para obtener el DNS.
# Para calcular la diferencia de fechas cuando la ip está en la BD.
from datetime import datetime, timedelta
# Comprobar sockets abiertos.
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout, getfqdn
from selenium import webdriver  # Abrir FireFox para capturas de pantallas.
from ipwhois import IPWhois  # Whois.
import pygeoip  # Para la geolcalización de las direcciones ip.
from ipaddress import IPv4Address  # Manejos de IPv4.
from random import randint  # Para la generación de ipv4 al azar.
hostname = getpass.getuser()  # Obtener el nombre de la maquina local.

from funcionamiento import herramienta

# Generar información de diagnostico para scripts con el módulo logging.
logging.basicConfig(filename='logs/iotInfo.log', level='INFO',
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = 'edison'
passdb = 'GnzNw2aAyJjKGOs7'
dbname = 'iotecuador'

# Conexión MongoAtlas.


def get_db():
    try:
        url_client = MongoClient("mongodb+srv://"+client+":"+passdb +
                                 "@iotecuador.qbeh8.mongodb.net/"+dbname+"?retryWrites=true&w=majority")
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





# Valida la existencia de la Ipv4 en la BD.
# 0: No Existe la IPv4 en la BD.
# 1: Existe la dirección IPv4, supera el tiempo limite en días.
# -1: Existe la dirección IPv4, No! supera el tiempo limite en días.
# Estado True: Contiene puertos activos asignados.
# Estado False: No! contiene puertos activos asignados.

def find_devices(IPV4):
    try:
        db = get_db()  # Conexiíon a la BD
        valor = 0
        Ipv4Bd = ''

        search = db.Devices.find({'Direccion': IPV4})
        for r in search:
            Ipv4Bd = r['Direccion']
            ic.disable()
            ic(Ipv4Bd)
            estadoBd = r['Estado']
            ic.disable()
            ic(estadoBd)
            fechaBd = r['Fecha']
            ic.disable()
            ic(fechaBd)

        if(Ipv4Bd != ''):  # Existe!

            if(estadoBd == True):  # Existen Puertos Abiertos
                ic.disable()
                ic(estadoBd)
                Tiempoconsulta = 30  # Tiempo en días.

                valor = DateTime(fechaBd, Tiempoconsulta)
                ic.enable()
                ic(valor)

            else:
                ic.disable()
                ic(estadoBd)
                Tiempoconsulta = 15  # Tiempo en días.

                valor = DateTime(fechaBd, Tiempoconsulta)
                ic.enable()
                ic(valor)

        else:  # No Existe!
            valor = 0

            #print ("No existe la direccion IPV4 ingresada",band)

        return valor

    except Exception:
        logging.error(
            "Al buscar la Direccion IPv4 : %s en la base de datos. find_devices()", IPV4)
        exit(1)

# Fecha de la Base de datos.


def DateTime(FechaBD, days):
    try:
        # Válida los paremetros de la fecha y hora
        cadena = datetime.strptime(FechaBD, "%Y-%m-%d %H:%M:%S")
        ahora = datetime.now()  # Obtener la hora actual de equipo
        # Establecer los días máximos a superar.
        treintadias = timedelta(days=days)
        fechaacomparar = ahora - treintadias

        ic(cadena, fechaacomparar)

        if cadena < fechaacomparar:  # Supera el limite de días establecidos.
            estadoFecha = 1

        else:
            estadoFecha = -1

        ic.enable()
        ic(estadoFecha)

        return estadoFecha

    except Exception as e:
        logging.error(
            "Se ha producido un error al validar la fecha. DateTime()")
        exit(1)

# Impresión de Texto Principal.


def cabecera():
    # install pip install pyfiglet
    try:
        Title = pyfiglet.figlet_format(
            "IOT ECUADOR \n", font="epic", justify="center")
        Users = ":.HERRAMIENTA DE ANÁLISIS DE VULNERABILIDADES EN DISPOSITIVOS IOT EN ECUADOR.:\n\n"
        inicio = 'Bienvenido!  >>>' + hostname + '<<<'

        print(bcolors.WARNING + Title + bcolors.ENDC)
        print(typewrite(Users))
        print(typewrite(inicio))

    except Exception:
        logging.error("Cabecera()")
        exit(1)

# Validar el número a entero.


def lee_entero():
    try:

        while True:
            entrada = input('Introduce la cantidad:')
            try:
                entrada = int(entrada)
                return entrada

            except ValueError:
                wow = "Wow! >>> " + entrada + " <<< no es un número entero:  "
                ic(typewrite(wow))

    except Exception:
        logging.error("lee_entero()")
        exit(1)

# Velocidad de escritura de los prints.


def typewrite(text):
    try:

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()

            if char != "\n":
                sleep(0.04)
            else:
                sleep(0.7)
        return char

    except Exception:
        logging.error("Typewrite()")
        exit(1)


def opc1():
    pr = " \nOk!. Cúantas direcciones Ipv4 Aleatorias deseas Analizar: \n"
    print(typewrite(pr))
    cant = lee_entero()
    maxCant = repeat(cant)
    agregar(int(maxCant))


def main():
    try:

        while True:
            pr = "\nCuéntame, que deseas hacer el día de hoy? \n"
            print(typewrite(pr))

            op1 = " 1)\tAnalizar direcciones Ipv4 en Ecuador "
            print(typewrite(op1))
            sleep(1)
            op2 = " 2)\tConocer como funciona la herramienta? "
            print(typewrite(op2))
            sleep(1)
            op3 = " 3)\tSalir\n"
            print(typewrite(op3))

            num = input('Introduce el Opción: ')

            if num == str(1):
                opc1()
                break

            if num == str(2):

                Obj = herramienta()
                print((typewrite(Obj) + "\n"))
                main()

                break

            if num == str(3):
                print("\n\n\t Gracias por usar el sistemas de Busqueda \n\n")
                exit(1)

            if num == '':
                print('No has ingresado una opción ')
                print('Favor de volverlo a intentar.')

            else:
                print('La opcion ingresada no es la corecta')
                print('Favor de volverlo a intentar.')

        return num

    except Exception as e:
        logging.warning(
            "Se ha producido un error al introducir la opción: %s. main()", num)
        exit(1)


# Direcciones IPV4  de Ecuador aleatorias.

def Generar_IP_Ecuador_Aleatoria():
    try:
        while True:  # Bucle que se cierra una ves obtenga la direcciones ipv4 de Ecuador

            ip = IPv4Address('{0}.{1}.{2}.{3}'.format(
                randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)))

            obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')

            # Validar que la direccion  ipv4 es de ecuador
            if(obj.country_code_by_addr(str(ip)) == "EC"):

                break

        return str(ip)  # guardar ipv4 de Ecuador

    except Exception as e:
        logging.error(
            "Se ha producido un error al crear una dirección Ipv4 randomica. Generar_IP_Ecuador_Aleatoria()")
        exit(1)


# Recibe un host y los puertos que queremos comprobar y devuelve los puertos abiertos

def OpenPort(host, puerto):
    try:
        setdefaulttimeout(0.5)  # Tiempo de conexión segundos
        s = socket(AF_INET, SOCK_STREAM)  # Puerto IPv4, TCP PROTOCOL
        resultado = s.connect_ex((str(host), puerto))
        if resultado == 0:
            return True  # Puerto abierto
        else:
            return False  # Puerto cerrado

    except Exception as e:
        logging.error("Al crear la conexión desde el host: %s ",
                      host, " con el puerto: %s. OpenPort()", puerto)
        exit(1)


# Captura la pantalla de la ip y el puerto dado.
# Al existir una imagen con el mismo nombre, simplemente lo actualiza.
# En caso que la ruta del directorio contenedor de sea incorrecta, se envia un mensaje con el recpectivo error!.
# El nombre que toma la img es la dirección Ipv4.

def capturadepantalla(ip, puerto):
    setdefaulttimeout(30)
    try:

        nombreimagen = "Noimagen.png"
        #browser=""#UnboundLocalError: local variable 'browser' referenced before assignment
        optionsChr = webdriver.ChromeOptions()
        optionsChr.add_argument("--headless")
        optionsChr.add_argument('--disable-gpu')
        optionsChr.add_argument('--log-level=3')
        optionsChr.set_capability("acceptInsecureCerts", True)
        optionsChr.add_argument("--incognito")
        optionsChr.add_argument('--ignore-certificate-errors')
        optionsChr.add_argument('--version')

        browser = webdriver.Chrome(
            executable_path=r'C:\\xampp\\htdocs\\Flask_IotEcuador\\IoT_Divices\\FirefoxDriver\\chromedriver.exe', options=optionsChr)
        
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(10)
        browser.get("http://{0}".format(ip)+":"+str(puerto))
        nombreimagen = str(ip)+","+str(puerto)+".png"  # Nombre de la Img.
        sleep(1)
        ic.enable()
        ic(nombreimagen)
        screenshot = browser.get_screenshot_as_file(

            r"C:\\xampp\\htdocs\\Flask_IotEcuador\\ApiFlask\static\\capturas\\" + str(nombreimagen))  # Bool
        ic.disable()
        ic(screenshot)


        state = screenshot
        ic.disable()
        ic("screenshot", state)
        browser.close()

    except Exception:
        state = False
        nombreimagen = "Noimagen.png"
        return nombreimagen

    print("Captura Exitosa!")
    return nombreimagen

    


# Obtiene la información correspondiente a esos puertos y añadirlos o actualizarlos.

def addNewDevices(ip, portOpen, exist):
    try:
        puertoList = []

        for puerto in portOpen:
            try:
                connection = socket(AF_INET, SOCK_STREAM)
                connection.connect((ip, puerto))
                connection.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = ""  # Inicializamos banner por si al final hay error en el siguiente paso
                banner = connection.recv(1024)  # Max 1024 Bytes contenido
                aux = str(banner).replace('\\r\\n', '<br/>')
                # Quitamos el espacio incial y los finales que no interesan. Ya tenemos el banner
                banner = aux[2:len(aux)-3]

            except Exception:
                logging.warning(
                    "Al realizar la conexion con el banner, puerto: %s. ", puerto)
                banner = None

            connection.close()

            # adñadir información de la direccion Ipv4
            obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
            location = obj.record_by_addr(str(ip))

            ic.disable()
            ic('location: ', location)
            for key, val in location.items():
                ic.disable()
                ic('%s : %s' % (key, val))

            #Realizar la captura.
            imagen = capturadepantalla(ip, puerto)


            # Almacena 'Documentos' dentro de un arreglo, usando append.
            puerto = {'Puerto': str(puerto), 'Banner': str(
                banner), 'Imagen': str(imagen)}
            puertoList.append(puerto)
            ic(puerto)

        # Información de los puertos:
        dominio = getfqdn(ip)  # Dominio
        whois = IPWhois(ip).lookup_whois()  # Whois
        dns = reversename.from_address(ip)  # DNS
        # Fecha y hora del Equipo.
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        ic.disable()
        ic(banner)
        ic.disable()
        ic(dominio)
        ic.disable()
        ic(whois)
        ic.disable()
        ic(dns)
        ic.disable()
        ic(date)
        ic.disable()
        ic(puertoList)

        # Agrega la infromacion a la base de datos por primera vez.
        # Los atributos que se asignan son los siguientes: (ip, img, fecha ,location, whois, dominio, dns, puerto)
        if exist == 0:
            estado = True
            db = get_db()
            datos = Device(str(ip), estado, date, location,
                           whois, str(dominio), str(dns), puertoList)
            db.Devices.insert_one(datos.toCollection())
            logging.info("Ipv4: %s, Agregada!", ip)

            return "Se agrego correctamente!\n"

        # Paso el límite los días esblecidos
        if exist == 1:
            db = get_db()
            db.Devices.update_one({"Direccion": str(ip)}, {"$set": {"Estado": True, "Fecha": date,
                                  "Whois": whois, "Dominio": str(dominio), "Dns": str(dns), "puerto": puertoList}})

            logging.info("Ipv4: %s, Actualizada!", ip)
            return "Se actualizo correctamente!\n"

    except Exception:
        logging.error(
            "La direccion IPv4: %s no puede agregar o actualizar.", ip, "Conexion: Fallida! addNewDevices")
        exit(1)

# finalización de la busqueda.


def new_search(valor):
    try:
        if ((valor == "Si") or (valor == "si") or (valor == "s") or (valor == "S")):
            return opc1()
        else:
            print(bcolors.HEADER +
                  "\n\n\t Gracias por usar el sistemas de Busqueda \n\n" + bcolors.ENDC)
            exit(1)

    except Exception:
        logging.error(
            "Se ha producido un error al generar una nueva busqueda. new_search()", )
        exit(1)
    # Si se recibe un parámetro se comprobaran tantas direcciones ip como es parámetro (limitando a 1000)

# Número de busquedas.


def repeat(repeticiones):
    try:
        # repeticiones=1 ## si usuario no ingresa ningun valor, por defecto es 1 direción ip
        # Realizara una busqueda de 100 direciones ipv4.
        if int(repeticiones) > 1000:
            repeticiones = 1000

        ic.enable()
        ic("Se van a examinar:", repeticiones)
        return repeticiones

    except Exception:
        logging.error(
            "Se ha producido un error en la cantidad de repeticiones. ", )
        exit(1)

# No existen puertos abiertos.


def EmptyPort(IPv4, exist):
    try:
        estadoBd = False  # Se agrege la nueva direccion IPv4
        db = get_db()  # Conexiíon a la BD
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        search = db.Devices.find({'Direccion': IPv4})
        for r in search:
            estadoBd = r['Estado']

        if(exist == 1 and estadoBd == False):  # Actualizacíon de los puertos
            db.Devices.update_one({"Direccion": str(IPv4)}, {
                                  "$set": {"Fecha": date}})
            return "Se actualizo correctamente!\n"

        if(exist == 1 and estadoBd == True):  # Actualizacíon de los puertos
            db.Devices.update_one({"Direccion": str(IPv4)}, {
                                  "$set": {"puerto": None, "Estado": False}})

            return "Se actualizo correctamente!\n"

        if(exist == 0):  # Agregar
            estado = False
            obj = pygeoip.GeoIP('Geo/GeoLiteCity.dat')
            location = obj.record_by_addr(str(IPv4))
            datos = Device(str(IPv4), estado, date, location,
                           None, None, None, None)
            db.Devices.insert_one(datos.toCollection())
            return "Se agrego correctamente!\n"

    except Exception:
        logging.warning(
            "La direccion IPv4: %s, PuertosActivos: 0 no puede agregarse o actualizarse.", IPv4, "Conexion: Fallida")
        exit(1)





def agregar(repeticiones):

    try:

        PortList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                        1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                        1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                        69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]


        # agregarle en una funcion
        #print("repeticiones", repeticiones)
        for contador in range(0, int(repeticiones)):
            # validar el tipo de busqueda.
            ip = Generar_IP_Ecuador_Aleatoria()  # llamamos a la funcion, ip aleatorias
            ic.enable()
            Num = contador+1
            ic(Num, ip)
            # Comprobamos si la IPv4 está en la base de datos MongpAtlas
            findDeviceBD = find_devices(ip)

            ic.enable()
            ic(findDeviceBD)

            if(findDeviceBD == 0 or findDeviceBD == 1):
                portOpen = []

                num = len(PortList)
                with alive_bar(num) as bar:
                    for port in PortList:
                        bar()

                        estadoPort = OpenPort(ip, port)

                        if estadoPort == True:

                            ic.disable()
                            ic(port, estadoPort)
                            portOpen.append(port)

                        else:
                            ic.disable()
                            ic(port, estadoPort)

                    portsNumbers = len(portOpen)

                if int(portsNumbers) != 0:
                    ic.enable()
                    ic(portOpen)
                    Estado = addNewDevices(ip, portOpen, findDeviceBD)
                    ic.enable()
                    ic(Estado)

                else:
                    ic.enable()
                    ic(portsNumbers)
                    Estado = EmptyPort(ip, findDeviceBD)
                    ic.enable()
                    ic(Estado)
                    ic.enable()

            else:
                print("La dirección IPv4", ip,
                      " ya existe y es menor a los días establecidos")

        print("\n\nBusqueda Finalizada :) \n\n")
        return final()

    except Exception as e:
        print("Se ha producido un error al agregar o actualizar la dirección IPv4:" +
              bcolors.WARNING + e + bcolors.ENDC)
        exit(1)

    # resultado


def final():

    try:
        print("Desea realizar una nueva busqueda \n")
        valor = input("Ingrese Si / No: ")
        ic.disable()
        ic(new_search(valor))

    except Exception:
        logging.error("Validar la opción (Si / No):")
        exit(1)


if __name__ == "__main__":
    colorama.init()
    cabecera()
    main()
