
from conexion import conectar

def navegar_a_pagina(frame, nombre_clase: str):
    from crud.pacientes.listaPacientes import ListaPacientes
    from crud.pacientes.crearPacientes import CrearPacientes
    from crud.usuarios.listaUsuarios import ListaUsuarios
    from crud.usuarios.crearUsuarios import CrearUsuario
    

    paginas = {
        "Lista pacientes": ListaPacientes,
        "Lista usuarios": ListaUsuarios,
        "Crear pacientes": CrearPacientes,
        "Crear usuarios": CrearUsuario,
        
        
       
    }

    for widget in frame.winfo_children():
        widget.destroy()

    paginas[nombre_clase](frame)


def obtener_tabla(nombre_tabla):
    conexion = conectar()
    
    cursor = conexion.cursor(dictionary=True)
    
    query = f"SELECT * FROM {nombre_tabla}"
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    print(resultados)
    return resultados

def borrar_registro(nombre_tabla, nombre_columna, valor_columna):
    conexion = conectar()
    
    cursor = conexion.cursor()
    
    query = f"DELETE FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}";
    print(query)
    
    cursor.execute(query)
    conexion.commit()
    cursor.close()
    conexion.close()
    
    
    


       