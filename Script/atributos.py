class Device:
    def __init__(self, ip, active, fecha ,location, whois, dominio, dns, puerto):
        self.ipv4 = ip
        self.active = active
        self.date = fecha
        self.location = location
        self.whois = whois
        self.dominio = dominio
        self.dns = dns
        self.puerto = puerto

    def toCollection(self):
        return{
            "Direccion": self.ipv4,
            "Estado": self.active,
            "Fecha": self.date,
            "Localizacion":self.location,
            "Whois": self.whois,
            "Dominio": self.dominio,
            "Dns": self.dns,
            "puerto": self.puerto
        }

