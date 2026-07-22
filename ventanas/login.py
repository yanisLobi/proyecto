import tkinter as tk
from tkinter import messagebox

from conexion import conectar
from ventanas.aplicacion import iniciar_aplicacion
from ventanas.registro import iniciar_registro
from herramientas import obtener_tabla
import ttkbootstrap as ttkb
        
def main():
    # esto se actualizara con datos de la db despues
    # Abre la conexión
    lista_usuarios = obtener_tabla('usuarios')

    def recargar_usuarios():
        nonlocal lista_usuarios
        lista_usuarios = obtener_tabla('usuarios')
    
    # temas: minty (verde), cosmo (blanco), darkly (obscuro)
    ventana = ttkb.Window(themename="darkly") 
    ventana.title("AbueCare Login")
    ventana.geometry("360x550")
    ventana.pack_propagate(False)
    ventana.resizable(False, False)
    imagen_original = tk.PhotoImage(file="recursos/1.png")
    ventana.iconphoto(True, imagen_original)

    imagen_original = tk.PhotoImage(file="recursos/1.png")
    imagen_pequena = imagen_original.subsample(10)
    
    etiqueta_logo = ttkb.Label(ventana, image=imagen_pequena)
    etiqueta_logo.pack(pady=(50, 30))
        
    contenido_frame = ttkb.Frame(ventana)
    contenido_frame.pack(padx=30, fill="x")
    contenido_frame.grid_columnconfigure(0, weight=1)

    # Entry para correo
    ttkb.Label(contenido_frame, text="Correo:").grid(row=0, column=0, sticky="w", pady=(5, 2))
    correo = ttkb.Entry(contenido_frame)
    correo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    
    # Entry para contraseña
    ttkb.Label(contenido_frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=(5, 2))
    contra = ttkb.Entry(contenido_frame)
    contra.grid(row=3, column=0, sticky="ew", pady=(0, 10))
    #-------------------------------------------------------------------------------
    


    def intentar_login():
        correo_introducido = correo.get().strip()
        contrasena_introducida  = contra.get().strip()
        
        if correo_introducido == "":
            messagebox.showinfo("Error al iniciar sesion", "Debes introducir correo y contraseña")
            return
        
        correos = [usuario.get("us_correo_electronico") for usuario in lista_usuarios]
        print(f"Correos encontrados en la DB: {correos}")
        
        if correo_introducido not in correos:
            messagebox.showinfo("Error al iniciar sesion", "El correo introducido no esta registrado")
            return
        
        contrasena_esperada = [usuario.get("us_contraseña") for usuario in lista_usuarios if usuario.get("us_correo_electronico") == correo_introducido ][0]
        print(f"Contraseña encontrada en la DB: {contrasena_esperada}")
        
        if contrasena_introducida != contrasena_esperada:
            messagebox.showinfo("Error al iniciar sesion", "La contrasena es incorrecta")
            return
        
        tipo_usuario = [usuario.get("us_tipo_usuario") for usuario in lista_usuarios if usuario.get("us_correo_electronico") == correo_introducido ][0]
        nombre_usuario = [usuario.get("us_nombre") for usuario in lista_usuarios if usuario.get("us_correo_electronico") == correo_introducido ][0]
        messagebox.showinfo("Inicio de sesion exitoso", f"Bienvenido a Abuecare {nombre_usuario}")
        iniciar_aplicacion(ventana, tipo_usuario, contra)

    def abrir_registro():
        iniciar_registro(ventana)
        recargar_usuarios()
        
    botones_frame = ttkb.Frame(contenido_frame)
    botones_frame.grid(row=4, column=0, sticky="ew", pady=(20, 30))
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)

    # Botón 1: Columna 0 ----- Boton de iniciar sesion
    iniciar = ttkb.Button(
        botones_frame, text="Iniciar Sesion", command=intentar_login, bootstyle="primary"
    )
    iniciar.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    # Botón 2: Columna 1 ----- Boton de registro
    registrar = ttkb.Button(
        botones_frame, text="Registrarse", command=abrir_registro, bootstyle="secondary"
    )
    registrar.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    # Ejecutar la aplicación
    ventana.mainloop()
    
if __name__ == "__main__":
    main()