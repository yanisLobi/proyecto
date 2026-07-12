import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password= "",
        database = "geriatria3"
    )
    
    print("conexion exitosa")
    return conexion


if __name__ == "__main__":
    # Solo se ejecuta si corremos este archivo 
    con = conectar()