
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from conexion import conectar


def limpiar_widget(widget):
    if isinstance(widget, (tk.Entry, ttk.Entry)):
        widget.delete(0, tk.END)
    elif isinstance(widget, tk.Text):
        widget.delete("1.0", tk.END)
    elif isinstance(widget, ttk.Combobox):
        widget.set("")
        try:
            widget.current(newindex=-1)
        except Exception:
            pass
    elif isinstance(widget, tk.Radiobutton):
        var = widget.cget("variable")
        if var:
            var.set("")
    elif isinstance(widget, DateEntry):
        widget.set_date(widget._date)
    elif isinstance(widget, tk.Scale):
        widget.set(widget.cget("from"))
    elif hasattr(widget, "winfo_children"):
        for hijo in widget.winfo_children():
            limpiar_widget(hijo)


def limpiar_frame(frame):
    for widget in frame.winfo_children():
        limpiar_widget(widget)

def navegar_a_pagina(frame, nombre_clase, **kwargs):
    from crud.pacientes.listaPacientes import ListaPacientes
    from crud.pacientes.crearPacientes import CrearPacientes
    from crud.pacientes.actualizarPacientes import ActualizarPacientes
    from crud.usuarios.listaUsuarios import ListaUsuarios
    from crud.usuarios.crearUsuarios import CrearUsuario
    from crud.usuarios.actualizarUsuarios import ActualizarUsuarios
    from crud.medicamentos.listaMedicamentos import ListaMedicamentos
    from crud.medicamentos.crearMedicamentos import CrearMedicamentos
    from crud.medicamentos.actualizarMedicamentos import ActualizarMedicamentos
    from crud.tratamientos.actualizarTratamientos import ActualizarTratamientos
    from crud.tratamientos.listaTratamientos import ListaTratamientos
    from crud.tratamientos.crearTratamientos import CrearTratamientos
    
    
    

    paginas = {
        "Lista pacientes": ListaPacientes,
        "Lista usuarios": ListaUsuarios,
        "Crear pacientes": CrearPacientes,
        "Crear usuarios": CrearUsuario,
        "Actualizar usuarios": ActualizarUsuarios,
        "Lista medicamentos": ListaMedicamentos,
        "Crear medicamentos": CrearMedicamentos,
        "Actualizar medicamentos": ActualizarMedicamentos,
        "Actualizar pacientes": ActualizarPacientes,
        "Lista tratamientos": ListaTratamientos,
        "Crear tratamientos": CrearTratamientos,
        "Actualizar tratamientos": ActualizarTratamientos,
    }

    for widget in frame.winfo_children():
        widget.destroy()

    clase_instanciar = paginas.get(nombre_clase)
    if not clase_instanciar:
        raise Exception(f'diccionario paginas no conoce ese archivo: {nombre_clase}')

    clase_instanciar(frame, **kwargs)


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

def obtener_registro(nombre_tabla, nombre_columna, valor_columna):
    conexion = conectar()
    
    cursor = conexion.cursor(dictionary=True)
    
    query = f"SELECT * FROM {nombre_tabla} WHERE {nombre_columna} = {valor_columna}"
    
    cursor.execute(query)
    resultados = cursor.fetchone()
    cursor.close()
    conexion.close()
    print(resultados)
    return resultados

def insertar_registro(tabla, diccionario_usuario):
    usuario_keys = ", ".join(diccionario_usuario.keys()) 
    separadores = ", %s"*len(diccionario_usuario.values()) 
    sql = f"INSERT INTO {tabla} ({usuario_keys}) VALUES ({separadores[1:]})"
    print(sql)
    
    conexion = conectar()
    
    cursor = conexion.cursor()

    cursor.execute(sql, tuple(diccionario_usuario.values()))

    
    conexion.commit()
    
    cursor.close()
    conexion.close()

def actualizar_registro(tabla, diccionario_usuario, nombre_columna, valor_columna):
    usuario_keys = "=%s, ".join(diccionario_usuario.keys()) 
    
    sql = f"UPDATE {tabla} set {usuario_keys} =%s WHERE {nombre_columna} = {valor_columna}"
    print(sql)
    
    conexion = conectar()
    
    cursor = conexion.cursor()

    cursor.execute(sql, tuple(diccionario_usuario.values()))

    
    conexion.commit()
    
    cursor.close()
    conexion.close()

def obtener_valores(nombre_tabla, nombre_columna, nombre_columna1, nombre_columna2):
    conexion = conectar()
    
    cursor = conexion.cursor()
    
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM {nombre_tabla} "
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    print(resultados)
    return resultados

def obtener_valores_usuarios( nombre_columna, nombre_columna1, nombre_columna2, tipo_usuario):
    conexion = conectar()
    
    cursor = conexion.cursor()
    
    query = f"SELECT {nombre_columna}, {nombre_columna1}, {nombre_columna2} FROM usuarios WHERE us_tipo_usuario = '{tipo_usuario}'"
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    print(resultados)
    return resultados

def regresar_string(titulos):
    if titulos.startswith("tr_"):
        titulos = titulos.replace("tr", "",1)
    
    resultado = titulos.replace("_", " ")
    resultado = resultado.title()
    resultado = " ".join(resultado.split())
    return resultado

print(regresar_string("tr_tratamiento_final "))

    
    
    
    
    



    
    
    


       