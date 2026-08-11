import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import time
from datetime import datetime
import ttkbootstrap as ttkb
from db.db_mysql import obtener_registros
from db.db_mongo import (
    obtener_tabla,
    obtener_eventos_doctor,
    obtener_eventos_enfermera,
)


def agregar_boton_mostrar_contrasena(
        parent,
        entry,
        row,
        column,
        sticky="w",
        padx=(
            6,
            0),
    pady=0,
    width=3,
        bootstyle="outline-secondary"):
    """Agrega un botón para mostrar u ocultar la contraseña en un campo de entrada.
    Devuelve el botón y la variable de control para manejar su estado."""
    mostrar = tk.BooleanVar(value=False)

    def toggle_password_visibility():
        mostrar.set(not mostrar.get())
        entry.config(show="" if mostrar.get() else "*")
        boton.config(text="_" if mostrar.get() else "👁")

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
    """Limpia el contenido de un widget de interfaz.
    Funciona con widgets de texto, combosboxeses, Radiobuttons, etc.
    este metodo no ahorra codigo en cada una de las clases de formularios
    """
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
    """Limpia todos los widgets de un contenedor de la interfaz.
    Se usa para reiniciar formularios o paneles de forma rápida."""
    for widget in frame.winfo_children():
        limpiar_widget(widget)


def navegar_a_pagina(frame, nombre_clase, **kwargs):
    """Cambia la vista actual por otra pantalla de la aplicación.
    Recibe el nombre de la pantalla y los datos necesarios para construirla.
    
    Al importar las clases aqui, se evita un error de importación circular
    """
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
        raise Exception(
            f"diccionario paginas no conoce ese archivo: {nombre_clase}")

    clase_instanciar(frame, **kwargs)


def mostrar_sin_registros(frame, nombre_tabla):
    """Muestra un mensaje cuando no hay registros para mostrar.
    Recibe el nombre del elemento o sección para hacerlo más claro al usuario."""
    ttkb.Label(
        frame,
        text=f"La tabla \"{nombre_tabla}\" no contiene ningún registro.\nSi tienes algún problema contacta a tu administrador.",
        font=("Arial", 12),
        justify="center",
        anchor="center",
    ).pack(pady=(40, 10))


def validar_widget(widget, nombre_campo, max_len=None, tipo="texto",
                   requerido=True, min_len=None):
    """Valida el contenido de un campo de formulario.
    Revisaa si está vacío, si tiene el tipo correcto y si cumple con la longitud permitida."""
    import tkinter as tk
    from tkinter import messagebox

    if isinstance(widget, tk.Text):
        valor = widget.get("1.0", "end-1c").strip()
    else:
        valor = str(widget.get()).strip()

    if requerido and not valor:
        messagebox.showerror("Campo requerido",
                             f"El campo '{nombre_campo}' es obligatorio.")
        widget.focus_set()
        return False

    if valor:
        if tipo == "numerico" and not valor.isdigit():
            messagebox.showerror("Tipo inválido",
                                 f"'{nombre_campo}' solo acepta números.")
            widget.focus_set()
            return False
        if max_len and len(valor) > max_len:
            messagebox.showerror("Longitud excedida",
                                 f"'{nombre_campo}' no puede superar {max_len} caracteres.")
            widget.focus_set()
            return False
        if min_len and len(valor) < min_len:
            messagebox.showerror("Longitud insuficiente",
                                 f"'{nombre_campo}' debe tener al menos {min_len} caracteres.")
            widget.focus_set()
            return False

    return True


def validar_combo(stringvar, nombre_campo):
    """Verifica que un combo haya recibido una opción válida.
    Evita que se guarde el valor por defecto de 'ninguno'."""
    from tkinter import messagebox
    val = stringvar.get() if hasattr(stringvar, "get") else str(stringvar)
    if not val.strip() or val.strip().lower() == "ninguno":
        messagebox.showerror("Campo requerido",
                             f"Debes seleccionar un valor para '{nombre_campo}'.")
        return False
    return True


def obtener_columnas(columnas, tipo_usuario=""):
    """Filtra las columnas que deben mostrarse en pantalla.
    Oculta campos sensibles o internos según el tipo de usuario."""
    if tipo_usuario == "Administrador":
        columnas_ocultar = {"contraseña", "password", "passwd"}
    else:
        columnas_ocultar = {"_activo", "contraseña", "password", "passwd"}

    def debe_ocultarse(nombre):
        texto = str(nombre).lower()
        return any(token in texto for token in columnas_ocultar)

    return [columna for columna in columnas if not debe_ocultarse(columna)]


def regresar_string(titulos):
    """Convierte un nombre técnico en texto más legible para la interfaz.
    Elimina prefijos comunes y separa palabras con espacios."""
    palabras_remover = ["id", "tr", "us", "pa", "me", "re"]

    for palabra in palabras_remover:
        if titulos.startswith(palabra):
            titulos = titulos.replace(palabra, "", 1)

    resultado = titulos.replace("_", " ")
    resultado = resultado.title()
    resultado = resultado.strip()
    return resultado


# id_registo = 5, opciones = [(1, "juan"), (5, "yanet")], resultado o
# indice encontrado igual a 1

def obtener_indice(id_registro: int, opciones: list[tuple]):
    """Busca la posición de un registro dentro de una lista de opciones.
    Devuelve el índice correspondiente para usarlo en controles de selección."""
    indice_encontrado = 0
    for opcion in opciones:
        if id_registro == opcion[0]:
            return indice_encontrado
        else:
            indice_encontrado = indice_encontrado + 1

    return 0


def mostrar_recordatorios(id_usuario=None, tipo_usuario=None, stop_event=None):
    """Muestra recordatorios de eventos cuando se acercan a su hora.
    Revisa los eventos pendientes y avisa al usuario según el tiempo restante."""
    dif_eventos = [15, 5, 0]
    # Guardar por evento qué umbrales ya fueron notificadas.
    # Así se muestran 15 minutos antes, 5 minutos antes y a la hora exacta,
    # pero sin repetir el mismo aviso varias veces.
    _mostrados = {}
    while True:
        if stop_event is not None and stop_event.is_set():
            break

        if stop_event is None:
            time.sleep(1)
        else:
            stop_event.wait(1)
            if stop_event.is_set():
                break

        if tipo_usuario == "Doctor":
            eventos = obtener_eventos_doctor(id_usuario)
        elif tipo_usuario == "Enfermera":
            eventos = obtener_eventos_enfermera(id_usuario)
        else:
            eventos = obtener_tabla("consultas")

        for evento in eventos:
            fecha_partes = evento["re_fecha"].split("-")

            year_1 = fecha_partes[0]
            mes_1 = fecha_partes[1]
            dia_1 = fecha_partes[2]

            if evento["re_estado"] == "Completado":
                continue

            hora_partes = evento["re_hora_inicio"].split(":")
            hora = int(hora_partes[0])
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

            if diff_hora == 0 and diff_minutos >= 0:
               # print(
                   # f"{year_1} {mes_1} {dia_1} {hora} {minuto} - {year_2} {mes_1} {mes_2} {hora_a} {minuto_a}  ")
               # print(f" La diferencia es {diff_hora} {diff_minutos} ")
                if diff_minutos in dif_eventos:
                    id_evento = str(evento.get("id"))
                    if id_evento not in _mostrados:
                        _mostrados[id_evento] = set()
                    if diff_minutos in _mostrados[id_evento]:
                        continue

                    tratamiento = obtener_registros(
                        "tratamientos", "id_tratamientos", evento["id_tr"], False)[0]
                    paciente = obtener_registros(
                        "pacientes", "id_pacientes", tratamiento.get("id_paciente"), False)[0]
                    enfermera = obtener_registros(
                        "usuarios", "id_usuarios", paciente.get("id_enfermera_principal"), False)[0]
                    doctor = obtener_registros(
                        "usuarios", "id_usuarios", tratamiento.get("id_doctor"), False)[0]
                    observacion_evento = evento["re_observaciones"]

                    hora_inicio = evento["re_hora_inicio"]
                    hora_final = evento["re_hora_fin"]

                    messagebox.showinfo(
                        f"📅 {evento['re_titulo']}\n",
                        (

                            f" Tu evento comienza en {diff_minutos} minutos\n\n"

                            f" Tratamiento: {tratamiento.get('tr_nombre')}"

                            f" Fecha de inicio del tratamiento: {tratamiento.get('tr_fecha_inicio')}"
                            f" Fecha final del tratamiento: {tratamiento.get('tr_fecha_final')}\n\n"


                            f" Hora de inicio del evento: {hora_inicio}\n"
                            f" Hora de final del evento: {hora_final}\n\n"

                            f" Paciente: {paciente.get('pa_nombre')} {paciente.get('pa_apellidos')}\n\n"
                            f" Nombre del contacto de emergencia: {paciente.get('pa_nombre_contacto_emergencia')}\n\n"
                            f" Número del contacto de emergencia {paciente.get('pa_tel_contacto_emergencia')}\n\n"


                            f" Enfermera: {enfermera.get('us_nombre')} {enfermera.get('us_apellidos')}\n"
                            f" Cédula profesional: {enfermera.get('us_cedula')}\n"
                            f" Especialidad: {enfermera.get('us_especialidad')}\n\n"

                            f" Doctor: {doctor.get('us_nombre')} {doctor.get('us_apellidos')}\n"
                            f" Cédula profesional: {doctor.get('us_cedula')}\n"
                            f" Especialidad: {doctor.get('us_especialidad')}\n\n"


                            f" Observación evento: {observacion_evento}\n"
                            f" Observación tratamiento: {tratamiento.get('tr_descripcion')}"
                        ),
                    )
                    _mostrados[id_evento].add(diff_minutos)



