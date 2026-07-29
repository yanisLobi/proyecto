import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import threading
import time


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
    from crud.eventos.actualizarEventos import ActualizarEventosMongo
    from crud.eventos.consultarEventos import ConsultarEventosMongo
    from crud.eventos.crearEventos import CrearEventosMongo
    from crud.eventos.listaEventos import ListaEventosMongo
    
    
    
    
    from crud.calendario import CalendarioRecordatorios

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
        "Calendario": CalendarioRecordatorios,
        "Lista eventos": ListaEventosMongo,
        "Actualizar eventos": ActualizarEventosMongo,
        "Crear eventos": CrearEventosMongo,
        "Consultar eventos": ConsultarEventosMongo
    }

    for widget in frame.winfo_children():
        widget.destroy()

    clase_instanciar = paginas.get(nombre_clase)
    if not clase_instanciar:
        raise Exception(f"diccionario paginas no conoce ese archivo: {nombre_clase}")

    clase_instanciar(frame, **kwargs)

 

    


def regresar_string(titulos):
    palabras_remover = ["id", "tr", "us", "pa", "me", "re"]

    for palabra in palabras_remover:
        if titulos.startswith(palabra):
            titulos = titulos.replace(palabra, "", 1)

    resultado = titulos.replace("_", " ")
    resultado = resultado.title()
    resultado = resultado.strip()
    return resultado


# id_registo = 5, opciones = [(1, "juan"), (5, "yanet")], resultado o indice encontrado igual a 1

def obtener_indice(id_registro: int, opciones: list[tuple]):
    indice_encontrado = 0
    for opcion in opciones:
        if id_registro == opcion[0]:
            return indice_encontrado
        else:
            indice_encontrado = indice_encontrado + 1

    return 0

def mostrar_recordatorios():
    print("Inicio de la tarea...")
    time.sleep(2)  # Simulando una espera de I/O
    print("Tarea finalizada.")
