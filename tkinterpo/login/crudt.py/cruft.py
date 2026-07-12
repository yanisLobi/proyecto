#CRUD con Tkinter POO

#CRUD significa:
#crear
#leer
#actualizar
#eliminar

import tkinter as tk

# 1. FUNCIÓN PARA CREAR (Añadir a la lista)
def crear():
    palabra = entrada.get()          # Lee lo que escribiste en el cuadro
    if palabra != "":                # Si no está vacío...
        lista_visual.insert(tk.END, palabra)  # ¡Lo mete al final de la lista!
        entrada.delete(0, tk.END)    # Borra el cuadro para dejarlo limpio

# 2. FUNCIÓN PARA LEER (Ver lo seleccionado)
def leer(event):
    indice = lista_visual.curselection()   # Averigua qué fila tocaste (0, 1, 2...)
    if indice:
        palabra = lista_visual.get(indice) # Agarra la palabra de esa fila
        entrada.delete(0, tk.END)          # Limpia el cuadro
        entrada.insert(0, palabra)         # Pone la palabra en el cuadro

# 3. FUNCIÓN PARA ACTUALIZAR (Modificar la lista)
def actualizar():
    indice = lista_visual.curselection()   # Mira qué fila está seleccionada
    nuevo_texto = entrada.get()            # Lee el nuevo texto modificado
    if indice and nuevo_texto != "":
        lista_visual.delete(indice)        # Borra la palabra vieja de esa fila
        lista_visual.insert(indice, nuevo_texto) # Mete la nueva palabra ahí mismo

# 4. FUNCIÓN PARA ELIMINAR (Borrar de la lista)
def eliminar():
    indice = lista_visual.curselection()   # Mira qué fila tocaste
    if indice:
        lista_visual.delete(indice)        # ¡La borra por completo!
        entrada.delete(0, tk.END)          # Limpia el cuadro de texto

# --- INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Mi CRUD Simple")

# Cuadro para escribir
entrada = tk.Entry(ventana)
entrada.pack()

# Botones de acción
tk.Button(ventana, text="1. Añadir (Crear)", command=crear).pack()
tk.Button(ventana, text="3. Cambiar (Actualizar)", command=actualizar).pack()
tk.Button(ventana, text="4. Borrar (Eliminar)", command=eliminar).pack()

# La lista visual en pantalla
lista_visual = tk.Listbox(ventana)
lista_visual.pack()

# Este truco hace que al hacer CLIC en la lista, se active la función de LEER (2)
lista_visual.bind("<<ListboxSelect>>", leer)

ventana.mainloop()

