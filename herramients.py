import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import threading
import time
from datetime import datetime
import ttkbootstrap as ttkb
from db_mysql import obtener_registros
from db_mongo import obtener_tabla


def agregar_boton_mostrar_contrasena(parent, entry, row, column, sticky="w", padx=(6, 0), pady=0, width=3, bootstyle="outline-secondary"):
    mostrar = tk.BooleanVar(value=False)

    def toggle_password_visibility():
        mostrar.set(not mostrar.get())
        entry.config(show="" if mostrar.get() else "*")
        boton.config(text="🙈" if mostrar.get() else "👁")

    boton = ttkb.Button(
        parent,
        text="👁",
        command=toggle_password_visibility,
        bootstyle=bootstyle,
        width=width,
    )
    boton.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
    return boton, mostrar


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

 
def obtener_columnas(columnas):
    columnas_ocultar = {"_activo", "_contraseña", "contraseña", "password", "passwd"}

    def debe_ocultarse(nombre):
        texto = str(nombre).lower()
        return any(token in texto for token in columnas_ocultar) or texto.endswith("_activo")

    return [columna for columna in columnas if not debe_ocultarse(columna)]
    


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
    dif_eventos= [15, 5, 0]
    while True:
        time.sleep(50)
        eventos = obtener_tabla("consultas")
        
        
        
        
        
        for evento in eventos:
            fecha_partes = evento["re_fecha"].split("-")
            
            
            year_1= fecha_partes[0]
            mes_1=fecha_partes[1]
            dia_1 = fecha_partes[2]
            
            if evento["re_estado"] == "Completado":
                continue
           
            hora_partes = evento["re_hora_inicio"].split(":")
            hora= int(hora_partes[0]) 
            minuto = int(hora_partes[1])

            ahora = datetime.now()
            year_2 = ahora.strftime("%Y")
            mes_2 = ahora.strftime("%m")
            dia_2 = ahora.strftime("%d")
            
            hora_a = int(ahora.strftime("%H"))
            minuto_a = int(ahora.strftime("%M"))
            
            
            
            
            if year_1 != year_2 or mes_1 != mes_2 or dia_1 != dia_2:
                
                continue
            
            
            diff_hora = hora - hora_a
            diff_minutos = minuto - minuto_a
            
            
            if diff_hora == 0:
                print(f"{year_1} {mes_1} {dia_1} {hora} {minuto} - {year_2} {mes_1} {mes_2} {hora_a} {minuto_a}  ")  
                print(f" La diferencia es {diff_hora} {diff_minutos} ")
                if diff_minutos in dif_eventos: #Numeros positivos son minutos faltantes
                    
                    tratamiento = obtener_registros("tratamientos", "id_tratamientos", evento["id_tr"] )[0]
                    paciente = obtener_registros("pacientes", "id_pacientes", tratamiento.get("id_paciente"))[0]
                    enfermera = obtener_registros("usuarios", "id_usuarios", paciente.get("id_enfermera_principal"))[0]
                    doctor = obtener_registros("usuarios", "id_usuarios", tratamiento.get("id_doctor"))[0]
                    observacion_evento = evento["re_observaciones"]
                    
                    
                    
                    frecuencia = evento["re_frecuencia"]
                    hora_inicio = evento["re_hora_inicio"]
                    hora_final = evento["re_hora_fin"]
                    
                    
                    """ tr_fecha_inicial = obtener_registros("tratamientos", "tr_fecha_inicio", tratamiento.get("tr_fecha_inicio"))[5].split("-")
                    fecha_mes_1= int(tr_fecha_inicial[1])
                    fecha_dia_1 = int(tr_fecha_inicial[2])
                    
                    tr_fecha_final = obtener_registros("tratamientos", "tr_fecha_final", tratamiento.get("tr_fecha_final"))[6].split("-")
                    fecha_mes_2= int(tr_fecha_inicial[1])
                    fecha_dia_2 = int(tr_fecha_final[2])
                    
                    dif_mes = fecha_mes_1 - fecha_mes_2
                    print(dif_mes)
                    dif_dia = fecha_dia_1 - fecha_dia_2
                    print(dif_dia) """
                   
                    messagebox.showinfo(
                            f"📅 {evento['re_titulo']}\n",
                            (
                                
                                f"⏰ Tu evento comienza en {diff_minutos} minutos\n\n"
                                
                                f"💊 Tratamiento: {tratamiento.get('tr_nombre')}"
                                
                                f"💊 Fecha de inicio del tratamiento: {tratamiento.get('tr_fecha_inicio')}"
                                f"💊 Fecha final del tratamiento: {tratamiento.get('tr_fecha_final')}\n\n"
                                
                                
                                f"🕒 Hora de inicio del evento: {hora_inicio}\n"
                                f"🕒 Hora de final del evento: {hora_final}\n\n"
                                
                                f"🧑 Paciente: {paciente.get('pa_nombre')} {paciente.get('pa_apllidos')}\n\n"
                                f"🧑 Nombre del contacto de emergencia: {paciente.get('pa_nombre_contacto_emergencia')}\n\n"
                                f"🧑 Número del contatco de emergencia {paciente.get('pa_tel_contatco_emergencia')}\n\n"
                                
                                 
                                f"👩‍⚕️ Enfermera: {enfermera.get('us_nombre')} {enfermera.get('us_apellidos')}\n"
                                f" 🆔 Cédula profesional: {enfermera.get('us_cedula')}\n"
                                f" 🆔 Especialidad: {enfermera.get('us_especialidad')}\n\n"
                                
                                f"👨‍⚕️ Doctor: {doctor.get('us_nombre')} {doctor.get('us_apellidos')}\n\n"
                                f" 🆔 Cédula profesional: {doctor.get('us_cedula')}\n"
                                f" 🆔 Especialidad: {doctor.get('us_especialidad')}\n\n"
                                
                               
                                f"📝 Observación evento: {observacion_evento}\n"
                                f"💊 Observación tratamiento: {tratamiento.get('tr_descripcion')}"
                            ),
                        )



def encriptar_contrasena(contrasena):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasena.encode("utf-8"), salt).decode("utf-8")