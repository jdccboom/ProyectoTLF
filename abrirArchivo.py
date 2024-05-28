import os
import tkinter as tk
from tkinter import scrolledtext

def mostrar_archivo(file_path,ventana_texto):
        # Verificar si el archivo existe antes de intentar abrirlo
    if os.path.exists(file_path):
        # Función para guardar los cambios al archivo
        for widget in ventana_texto.winfo_children():
            widget.destroy()
            
        def guardar_cambios():
            with open(file_path, "w") as file:
                nuevo_contenido = texto_archivo.get("1.0", tk.END)
                file.write(nuevo_contenido)
            estado_texto.set("Cambios guardados")
            

        # Crear un widget de texto desplazable para mostrar y editar el contenido del archivo
        texto_archivo = scrolledtext.ScrolledText(ventana_texto, wrap=tk.WORD, state=tk.NORMAL)
        texto_archivo.pack(expand=True, fill="both")

        # Botón para guardar los cambios
        boton_guardar = tk.Button(ventana_texto, text="Guardar Cambios", command=guardar_cambios)
        boton_guardar.pack()

        # Variable de estado para mostrar mensajes
        estado_texto = tk.StringVar()
        estado_label = tk.Label(ventana_texto, textvariable=estado_texto)
        estado_label.pack
        # Abrir el archivo de texto en modo de lectura
        with open(file_path, "r") as file:
            # Leer y mostrar el contenido del archivo de texto
            contenido = file.read()
            texto_archivo.insert(tk.END, contenido)

        # Iniciar el bucle principal de la ventana
    else:
        print("El archivo no existe.")