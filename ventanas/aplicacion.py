import tkinter as tk

from herramientas import navegar_a_pagina


def mostrar_contenido(contenido_frame, titulo, texto, clase_contenido= None):
    
    for widget in contenido_frame.winfo_children():
        widget.destroy()
        pass

    tk.Label(
        contenido_frame,
        text=titulo,
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Arial", 18, "bold")
    ).pack(pady=(40, 10))

    tk.Label(
        contenido_frame,
        text=texto,
        bg="#ecf0f1",
        fg="#34495e",
        font=("Arial", 12)
    ).pack()
    
    
    if clase_contenido:
        clase_contenido(contenido_frame)
        
        
def iniciar_aplicacion(ventana_login, tipo_usuario, campo_password):
    # Ocultamos la ventana que nos llamó (la ventana de inicio de sesion)
    ventana_login.withdraw()
    ventana = tk.Toplevel()
    ventana.title("AbueCare")
    ventana.geometry("1500x900")
    imagen_original = tk.PhotoImage(file="recursos/1.png")
    ventana.iconphoto(True, imagen_original)
    
    # Asegurar que si el usuario cierra el Dashboard con la 'X', se cierre todo el programa
    ventana.protocol("WM_DELETE_WINDOW", ventana_login.destroy)

# Columna 0 (Menú): peso 1. Columna 1 (Contenido): peso 4. Total = 5 partes (1/5 y 4/5)
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=4)
    ventana.grid_rowconfigure(0, weight=1) # El row 0 se estira verticalmente

# 1. FRAME DEL MENÚ LATERAL (Ocupa la columna 0)
# Se usa 'sticky="nsew"' para que el frame se estire en todas direcciones
    menu_frame = tk.Frame(ventana, bg="#2c3e50")
    menu_frame.grid(row=0, column=0, sticky="nsew")

    imagen_original = tk.PhotoImage(file="recursos/1.png")
    imagen_pequena = imagen_original.subsample(10)
# Crear una etiqueta (Label) y asignarle la imagen
    etiqueta_logo = tk.Label(menu_frame, image=imagen_pequena)
    etiqueta_logo.pack(pady=50)
   
   
        
# 2. FRAME DEL CONTENIDO (Ocupa la columna 1)
    contenido_frame = tk.Frame(ventana, bg="#ecf0f1")
    contenido_frame.grid(row=0, column=1, sticky="nsew")

    mostrar_contenido(contenido_frame, "Área de Contenido", "Selecciona una opción del menú")
    
    
    def cambiar_a_calendario():
        mostrar_contenido(contenido_frame,"Calendario", "Aquí aparecerá la gestión del calendario", )

    

    def cambiar_a_usuarios():
        navegar_a_pagina(contenido_frame, "Lista usuarios")

    def cambiar_a_pacientes():
        navegar_a_pagina(contenido_frame, "Lista pacientes")

    def cambiar_a_medicamentos():
        navegar_a_pagina(contenido_frame, "Lista usuarios")
    
    def cambiar_a_recordatorios():
        navegar_a_pagina(contenido_frame, "Lista usuarios")
    
    def cerrar_sesion():
        ventana.destroy()          # Cierra por completo el Dashboard
        ventana_login.deiconify()  # Hace visible otra vez el Login
        campo_password.delete(0, tk.END) # borra la contraseña de ulimo inicio de sesion

    # Aqui van los botones del menu que se muestran para todos los tipos de usuarios
    tk.Button(menu_frame, text="Calendario", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_calendario).pack(fill="x")    
    tk.Button(menu_frame, text="Pacientes", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_pacientes).pack(fill="x")    
    tk.Button(menu_frame, text="Recordatorios", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_recordatorios).pack(fill="x")

    # Mostrar los botones especiales segun que tipo de usuario inicio sesion
    if tipo_usuario == "Doctor":
        tk.Button(menu_frame, text="Usuarios", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_usuarios).pack(fill="x")
        tk.Button(menu_frame, text="Medicamentos", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_medicamentos).pack(fill="x")
    elif tipo_usuario == "Administrador":
        tk.Button(menu_frame, text="Usuarios", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_usuarios).pack(fill="x")
        tk.Button(menu_frame, text="Medicamentos", height=3,font=("Arial", 10, "bold"), fg="black", command=cambiar_a_medicamentos).pack(fill="x")
    
    tk.Button(menu_frame, text="Cerrar sesión", height=3,font=("Arial", 10, "bold"), fg="black", command=cerrar_sesion).pack(fill="x")
    
    # Ejecutar la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    pass
