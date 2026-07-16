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
    
    # temas: minty (verde), cosmo (blanco), darkly (obscuro)
    ventana = ttkb.Window(themename="darkly") 
    ventana.title("AbueCare Login")
    ventana.geometry("300x580")
    ventana.pack_propagate(False)
    imagen_original = tk.PhotoImage(file="recursos/1.png")
    ventana.iconphoto(True, imagen_original)

    imagen_original = tk.PhotoImage(file="recursos/1.png")
    imagen_pequena = imagen_original.subsample(10)
    
    etiqueta_logo = tk.Label(ventana, image=imagen_pequena)
    etiqueta_logo.pack(pady=50, padx=45, anchor="w")
        
    # Entry para correo
    tk.Label(ventana, text="Correo:").pack(pady=5, padx=30, anchor="w")
    correo = tk.Entry(ventana, width=25)
    correo.pack(pady=5, padx=30, anchor="w")
     
    
    # Entry para contraseña
    tk.Label(ventana, text="Contraseña:").pack(pady=5, padx=30, anchor="w")
    contra = tk.Entry(ventana, width=25)
    contra.pack(pady=5, padx=30, anchor="w")
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
        
    botones_frame = tk.Frame(ventana)
    botones_frame.pack(pady=20, padx=30, anchor="w", fill="x")

    # Botón 1: Columna 0 ----- Boton de iniciar sesion
    iniciar = tk.Button(botones_frame, text="Iniciar Sesion", command=intentar_login)
    iniciar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # Botón 2: Columna 1 ----- Boton de registro
    registrar = tk.Button(botones_frame, text="Registrarse", command=abrir_registro)
    registrar.grid(row=0, column=1, sticky="ew",padx=10, pady=10 )

    # Ejecutar la aplicación
    ventana.mainloop()
    
if __name__ == "__main__":
    main()