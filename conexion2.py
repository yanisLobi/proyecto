from pymongo import MongoClient
from pymongo.errors import PyMongoError

class Conexion:
    def __init__(self):
        self.url = "mongodb+srv://2025310115_db_user:o4QXDEqGOwWePdNs@cluster0.b5kz2o4.mongodb.net/?appName=Cluster0"
        self.cliente = None
        self.db = None
        self.coleccion = None
        self.error = None

        try:
            self.cliente = MongoClient(self.url, serverSelectionTimeoutMS=1000)
            self.cliente.admin.command("ping")
            self.db = self.cliente["Recordatorios"]
            self.coleccion = self.db["consultas"]
        except PyMongoError as e:
            self.error = e

    def obtener_coleccion(self):
        return self.coleccion

if __name__ == "__main__":
    conexion = Conexion()
    print(conexion.obtener_coleccion())
    print("conexion")
    
    
