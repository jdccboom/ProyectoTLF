import AnalizadorDeLenguaje,automata,abrirArchivo

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tabulate import tabulate

def seleccionar_archivo():
    global ruta_archivo, analizador
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.jdd")])
    if ruta:
        ruta_archivo=ruta
        modificar_archivo(ruta_archivo)
        buttonAnalizar.pack(side=tk.BOTTOM)
        buttonAutomatas.pack_forget()
        print(tabulate(analizador.categorized_text, tablefmt="grid"))

  
def imprimirTablaPantalla():
    
    limpiar_frame(frame_table)
    
    analizador.analizar(ruta_archivo)
    buttonAutomatas.pack(side=tk.BOTTOM)
    buttonAnalizar.pack_forget()
    btn_seleccionar_archivo.pack_forget()
    buttonModificar.pack(side=tk.BOTTOM)
    # Create a treeview widget for the table
    tree = ttk.Treeview(frame_table, columns=("category", "subcategory","type","value","fila","columna"), show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure the table columns
    tree.heading("category", text="Categoría")
    tree.heading("subcategory", text="Subcategoría")
    tree.heading("type", text="Tipo")
    tree.heading("value", text="Valor")
    tree.heading("fila", text="Fila")
    tree.heading("columna", text="Columna")
        
    for item in analizador.tabla:
        category= item["category"]
        subcategory = item["subcategory"]
        type= item["type"]
        value = item["value"]
        fila = item["fila"]
        columna= item["columna"]
        tree.insert("", tk.END, values= (category,subcategory,type,value,fila,columna))
    
def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def modificar_archivo(ruta_archivo):
    buttonModificar.pack_forget()
    buttonAutomatas.pack_forget()
    buttonAnalizar.pack(side=tk.BOTTOM)
    btn_seleccionar_archivo.pack(side=tk.BOTTOM)
    abrirArchivo.mostrar_archivo(ruta_archivo,frame_table)
    
if __name__ == '__main__':
    # Crear la ventana principal
    ventana = tk.Tk()
    ruta_archivo ='codigo/codigo.jdd'
    analizador = AnalizadorDeLenguaje.AnalizadorDeLenguaje(ruta_archivo)

    ventana.title("Aplicación principal")
    
    frame_button_selecionar = ttk.Frame(ventana)
    frame_button_selecionar.pack(side=tk.BOTTOM, fill=tk.X)

    # Botón para seleccionar archivo
    btn_seleccionar_archivo = tk.Button(frame_button_selecionar, text="Seleccionar Archivo", command=seleccionar_archivo)
    btn_seleccionar_archivo.pack(pady=10)
    # Create a frame for the button
    frame_button = ttk.Frame(ventana)
    frame_button.pack(side=tk.BOTTOM, fill=tk.X)
    
    buttonAnalizar = ttk.Button(frame_button, text="Analizar",command=imprimirTablaPantalla)
    buttonAnalizar.pack(side=tk.BOTTOM)
    
    buttonAutomatas = ttk.Button(frame_button, text="Automatas",command=lambda:automata.crear_automatas_para_palabras(analizador.tabla))
    buttonAutomatas.pack(side=tk.BOTTOM)
    buttonAutomatas.pack_forget()
    
    buttonModificar = ttk.Button(frame_button, text="Modificar archivo",command=lambda:modificar_archivo(ruta_archivo))
    buttonModificar.pack(side=tk.BOTTOM)
    buttonModificar.pack_forget()
    
    frame_table = ttk.Frame(ventana)
    frame_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    abrirArchivo.mostrar_archivo(ruta_archivo,frame_table)
    ventana.mainloop()
    

