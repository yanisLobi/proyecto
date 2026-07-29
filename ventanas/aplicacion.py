import tkinter as tk
import ttkbootstrap as ttkb
import threading
import time

from herramients import navegar_a_pagina, navegar_a_pagina, mostrar_recordatorios
from crud.calendario import CalendarioRecordatorios



def mostrar_contenido(contenido_frame, titulo, texto, clase_contenido= None ):
    for widget in contenido_frame.winfo_children():
        widget.destroy()
        pass

    ttkb.Label(
        contenido_frame,
        text=titulo,
        font=("Arial", 18, "bold")
    ).pack(pady=(40, 10))

    ttkb.Label(
        contenido_frame,
        text=texto,
        font=("Arial", 12)
    ).pack()
    
    
    if clase_contenido:
        clase_contenido(contenido_frame)

        
def iniciar_aplicacion(ventana_login, usuario, campo_password):
    tipo_usu = usuario.get("us_tipo_usuario")
    
   

    # Crear el hilo indicando la función objetivo
    hilo = threading.Thread(target=mostrar_recordatorios)

    # Iniciar el hilo
    hilo.start()
   

    
    # Ocultamos la ventana que nos llamó (la ventana de inicio de sesion)
    ventana_login.withdraw()
    ventana = tk.Toplevel()
    ventana.title("AbueCare")
    ventana.geometry("1500x900")
    ventana.resizable(False, False)
    imagen_original = tk.PhotoImage(file="recursos/1.png")
    ventana.iconphoto(True, imagen_original)
    
    # Asegurar que si el usuario cierra el Dashboard con la 'X', se cierre todo el programa
    ventana.protocol("WM_DELETE_WINDOW", ventana_login.destroy)

# Columna 0 (Menú): ancho fijo. Columna 1 (Contenido): ocupa el resto del espacio.
    ventana.grid_columnconfigure(0, weight=0, minsize=300)
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(0, weight=1) # El row 0 se estira verticalmente

# 1. FRAME DEL MENÚ LATERAL (Ocupa la columna 0)
# Se usa 'sticky="nsew"' para que el frame se estire en todas direcciones,
# pero con un ancho fijo para que no cambie al cargar tablas.
    menu_frame = ttkb.Frame(ventana, width=300)
    menu_frame.grid(row=0, column=0, sticky="nsew")
    menu_frame.grid_propagate(False)

    imagen_original = tk.PhotoImage(file="recursos/1.png")
    imagen_pequena = imagen_original.subsample(10)
    ttkb.Label(
                menu_frame,
                
                text=f"Hola, {tipo_usu}(a) {usuario.get("us_nombre").title()}",
                font=("Arial", 12)
            ).pack(padx=15)
    etiqueta_logo = ttkb.Label(menu_frame, image=imagen_pequena)
    etiqueta_logo.pack(pady=50)
   
   
        
# 2. FRAME DEL CONTENIDO (Ocupa la columna 1)
    contenido_frame = ttkb.Frame(ventana)
    contenido_frame.grid(row=0, column=1, sticky="nsew")

    
    
    
    def cambiar_a_calendario():
        def navegar_cb(tipo, nombre_clase, **kwargs):
            if tipo == "mongo":
                navegar_a_pagina(contenido_frame, nombre_clase, usuario=usuario, **kwargs)
            else:
                navegar_a_pagina(contenido_frame, nombre_clase,
                                 tipo_usuario=usuario.get("us_tipo_usuario"), **kwargs)
        mostrar_contenido(contenido_frame, "Calendario", "",
                          lambda f: CalendarioRecordatorios(f, navegar_cb=navegar_cb, usuario=usuario))

    cambiar_a_calendario()
    

    def cambiar_a_usuarios():
        navegar_a_pagina(contenido_frame, "Lista usuarios", usuario = usuario)

    def cambiar_a_pacientes():
        navegar_a_pagina(contenido_frame, "Lista pacientes", usuario=usuario)

    def cambiar_a_medicamentos():
        navegar_a_pagina(contenido_frame, "Lista medicamentos", usuario=usuario)
    
    def cambiar_a_recordatorios():
        navegar_a_pagina(contenido_frame, "Lista eventos", usuario=usuario)


    
    def cambiar_a_tratamiento():
        navegar_a_pagina(contenido_frame, "Lista tratamientos", usuario=usuario)
        
    
    
    def cerrar_sesion():
        ventana.destroy()          # Cierra por completo el Dashboard
        ventana_login.deiconify()  # Hace visible otra vez el Login
        campo_password.delete(0, tk.END) # borra la contraseña de ulimo inicio de sesion


   
    # Aqui van los botones del menu que se muestran para todos los tipos de usuarios
    menu_button_style = "Menu.TButton"
    menu_button_padding = (12, 12)
    ttkb.Style().configure(menu_button_style, font=("Arial", 12, "bold"))
    ttkb.Button(
        menu_frame,
        text="Calendario",
        command=cambiar_a_calendario,
        bootstyle="secondary",
        padding=menu_button_padding,
        style=menu_button_style,
    ).pack(fill="x")
    ttkb.Button(
        menu_frame,
        text="Pacientes",
        command=cambiar_a_pacientes,
        bootstyle="secondary",
        padding=menu_button_padding,
        style=menu_button_style,
    ).pack(fill="x")
    ttkb.Button(
        menu_frame,
        text="Recordatorios",
        command=cambiar_a_recordatorios,
        bootstyle="secondary",
        padding=menu_button_padding,
        style=menu_button_style,
    ).pack(fill="x")
    #tk.Button(menu_frame, text="Usuarios", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_usuarios).pack(fill="x") 
    # Mostrar los botones especiales segun que tipo de usuario inicio sesion
    if tipo_usu == "Doctor":
        #tk.Button(menu_frame, text="Usuarios", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_usuarios).pack(fill="x")
        ttkb.Button(
            menu_frame,
            text="Medicamentos",
            command=cambiar_a_medicamentos,
            bootstyle="secondary",
            padding=menu_button_padding,
            style=menu_button_style,
        ).pack(fill="x")
        ttkb.Button(
            menu_frame,
            text="Tratamiento",
            command=cambiar_a_tratamiento,
            bootstyle="secondary",
            padding=menu_button_padding,
            style=menu_button_style,
        ).pack(fill="x")
        
    elif tipo_usu == "Administrador":
        ttkb.Button(
            menu_frame,
            text="Usuarios",
            command=cambiar_a_usuarios,
            bootstyle="secondary",
            padding=menu_button_padding,
            style=menu_button_style,
        ).pack(fill="x")
        #tk.Button(menu_frame, text="Medicamentos", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_medicamentos).pack(fill="x")
    
    ttkb.Button(
        menu_frame,
        text="Cerrar sesión",
        command=cerrar_sesion,
        bootstyle="danger",
        padding=menu_button_padding,
        style=menu_button_style,
    ).pack(fill="x", side="bottom")
    ttkb.Separator(menu_frame).pack(fill="x", side="bottom", pady=(10, 0))
    
    
    
    
    
    
    
    
    
    
    
    # Ejecutar la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    pass
