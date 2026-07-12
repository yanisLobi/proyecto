import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_info():
    info = (
        f"Entry: {entry.get()}\n"
        f"Text: {text.get('1.0', tk.END).strip()}\n"
        f"Checkbutton: {'Activo' if var_chk.get() else 'Inactivo'}\n"
        f"Radiobutton: {var_radio.get()}\n"
        f"Combobox: {combo.get()}\n"
        f"Listbox: {listbox.get(tk.ACTIVE)}\n"
        f"Scale: {scale.get()}"
    )
    messagebox.showinfo("Información", info)

root = tk.Tk()
root.title("Cheatsheet Completo Tkinter")
root.geometry("700x750")

# Label
tk.Label(root, text="Ejemplo de Label").pack(pady=5)

# Entry
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Text
text = tk.Text(root, height=4, width=40)
text.pack(pady=5)

# Checkbutton
var_chk = tk.BooleanVar()
chk = tk.Checkbutton(root, text="Activar opción", variable=var_chk)
chk.pack(pady=5)

# Radiobutton
var_radio = tk.StringVar(value="Opción 1")
tk.Radiobutton(root, text="Opción 1", variable=var_radio, value="Opción 1").pack()
tk.Radiobutton(root, text="Opción 2", variable=var_radio, value="Opción 2").pack()

# Combobox
combo = ttk.Combobox(root, values=["A", "B", "C"])
combo.current(0)
combo.pack(pady=5)

# Listbox
listbox = tk.Listbox(root)
for item in ["Item 1", "Item 2", "Item 3"]:
    listbox.insert(tk.END, item)
listbox.pack(pady=5)

# Canvas
canvas = tk.Canvas(root, width=200, height=100, bg="lightgray")
canvas.create_rectangle(50, 20, 150, 80, fill="blue")
canvas.pack(pady=5)

# Frame
frame = tk.Frame(root, bg="lightblue", width=200, height=50)
frame.pack(pady=5)
tk.Label(frame, text="Dentro de un Frame").pack()

# Scale
scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
scale.pack(pady=5)

# Progressbar
pb = ttk.Progressbar(root, length=200, mode="determinate")
pb.pack(pady=5)
pb["value"] = 70

# Notebook (pestañas)
notebook = ttk.Notebook(root)
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")
tk.Label(tab1, text="Contenido de Tab 1").pack(pady=10)
tk.Label(tab2, text="Contenido de Tab 2").pack(pady=10)
notebook.pack(pady=5)

# Menú
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Salir", command=root.quit)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

# Scrollbar con Text
scroll_frame = tk.Frame(root)
scroll_frame.pack(pady=5)
scrollbar = tk.Scrollbar(scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_scroll = tk.Text(scroll_frame, height=4, width=40, yscrollcommand=scrollbar.set)
text_scroll.pack(side=tk.LEFT)
scrollbar.config(command=text_scroll.yview)

# Treeview (tabla)
tree = ttk.Treeview(root, columns=("col1", "col2"), show="headings")
tree.heading("col1", text="Columna 1")
tree.heading("col2", text="Columna 2")
tree.insert("", tk.END, values=("Dato 1", "Valor 1"))
tree.insert("", tk.END, values=("Dato 2", "Valor 2"))
tree.pack(pady=10)

# Button
btn = tk.Button(root, text="Mostrar información", command=mostrar_info)
btn.pack(pady=10)

#messabox
import tkinter as tk
from tkinter import messagebox

def saludar():
    messagebox.showinfo("Saludo", "¡Hola! Has presionado el botón.")

btn = tk.Button(root, text="Haz clic aquí", command=saludar)
btn.pack(pady=50)

root.mainloop()
