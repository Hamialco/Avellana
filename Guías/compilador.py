"""
compilador.py

"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font

import configparser
import os


from lexico import *
from sintaxis_v2 import *


class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloc de Notas en Python")
        self.root.geometry("800x800")

        # Fuente Consolas 12
        self.editor_font = font.Font(family="Consolas", size=16)

        # Frame principal dividido en editor y consola
        self.main_frame = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.main_frame.pack(fill="both", expand=True)

        # Notebook para pestañas de archivos
        self.notebook = ttk.Notebook(self.main_frame)
        self.main_frame.add(self.notebook, weight=4)

        # Consola en parte baja
        self.console = tk.Text(self.main_frame, height=8, bg="#1e1e1e", fg="white",
                               insertbackground="white", wrap="word")
        self.console.config(state="disabled")
        self.main_frame.add(self.console, weight=1)

        self.archivos = {}  # Para manejar archivos por pestaña

        # Crear menús
        self.crear_menu()

        #------------------------------------------------- Crear primera pestaña por defecto

        #----------------------------------- archivo INI <--------------------------------- (4)
        ini = configparser.ConfigParser()
        ini.read('compilador.ini')
        archivoAnterior = ini.get("compilador", "archivo")
   
        if os.path.exists(archivoAnterior):
            with open(archivoAnterior, "r", encoding="utf-8") as file:
                contenido = file.read()
            text_area = tk.Text(self.notebook, wrap="word", undo=True, font=self.editor_font)
            text_area.insert("1.0", contenido)
            nombre = archivoAnterior.split("/")[-1]
            self.notebook.add(text_area, text=nombre)
            self.notebook.select(text_area)
            self.archivos[text_area] = archivoAnterior
            self.log(f"Archivo abierto: {archivoAnterior}")
        else :
            self.nuevo_archivo()
        #-------------------------------------------------------------------------------------



    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir...", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar como...", command=self.guardar_como)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        # Menú Edición
        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="Cortar", command=lambda: self.editor_actual().event_generate("<<Cut>>"))
        edicion_menu.add_command(label="Copiar", command=lambda: self.editor_actual().event_generate("<<Copy>>"))
        edicion_menu.add_command(label="Pegar", command=lambda: self.editor_actual().event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edición", menu=edicion_menu)

        # Menú Ver/Consola
        consola_menu = tk.Menu(menubar, tearoff=0)
        consola_menu.add_command(label="Limpiar consola", command=self.limpiar_consola)
        menubar.add_cascade(label="Consola", menu=consola_menu)
        
        # Menú Fases de Compilación
        fases_menu = tk.Menu(menubar, tearoff=0)
        fases_menu.add_command(label="Lexico", command=self.examen_lexico)
        fases_menu.add_command(label="Sintaxis", command=self.examen_sintaxis)
        fases_menu.add_command(label="Semantica", command=self.examen_semantico)
        fases_menu.add_command(label="generación byte-code", command=self.genByteCode)
        fases_menu.add_command(label="Ejecución de programa", command=self.ejecutar)
        menubar.add_cascade(label="Fases", menu=fases_menu)   

    def editor_actual(self):
        tab = self.notebook.select()
        return self.notebook.nametowidget(tab)

    def nuevo_archivo(self):
        text_area = tk.Text(self.notebook, wrap="word", undo=True, font=self.editor_font)
        self.notebook.add(text_area, text="Sin título")
        self.notebook.select(text_area)
        self.archivos[text_area] = None  # Aún no tiene archivo asignado
        self.log("Nuevo archivo creado.")

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                contenido = file.read()
            text_area = tk.Text(self.notebook, wrap="word", undo=True, font=self.editor_font)
            text_area.insert("1.0", contenido)
            nombre = file_path.split("/")[-1]
            self.notebook.add(text_area, text=nombre)
            self.notebook.select(text_area)
            self.archivos[text_area] = file_path
            self.log(f"Archivo abierto: {file_path}")

    def guardar_archivo(self):
        text_area = self.editor_actual()
        file_path = self.archivos.get(text_area)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", tk.END))
            self.log(f"Archivo guardado: {file_path}")
        else:
            self.guardar_como()

    def guardar_como(self):
        text_area = self.editor_actual()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", tk.END))
            nombre = file_path.split("/")[-1]
            self.notebook.tab(text_area, text=nombre)
            self.archivos[text_area] = file_path
            self.log(f"Archivo guardado como: {file_path}")

    def log(self, mensaje):
        """Imprime en la consola inferior"""
        self.console.config(state="normal")
        self.console.insert(tk.END, mensaje + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def limpiar_consola(self):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")
        self.log("Consola limpiada.")
        
    def examen_lexico(self) :
        self.log("\n\nInicia Lexico")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))

        error, token = lex.generaLexico(True) # <----------------------------------- (1)
        msgError = lex.mensajeError(error)  # <------------------------------------- (1)

        if error == ERR_NOERROR : 
            lst = lex.get()
            for c in lst :
                s = str(c[1]) + "-" + lex.getTipoTokenStr(c[1], c[0])
                self.log(c[0] + " \t\t\t\t\t:: " + s)
        else :
            self.log(f"ERROR: {error} :: {token} :: {msgError}")
        self.log("Total de lineas procesadas: " + str(lex.getLineas()))
        
    def examen_sintaxis(self) :   # <-------------------------------------------- función SINTAXIS (es llamada del menu principal)
        self.log("\n\nInicia Sintaxis")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))
        error, token = lex.generaLexico(False) # <------------------------- (LEXICO) (2)
        msgErrorLex = lex.mensajeError(error)
        if error == ERR_NOERROR : 
            """
            lst = lex.get()
            for c in lst :
                s = str(c[1]) + "-" + lex.getTipoTokenStr(c[1], c[0])
                self.log(c[0] + " \t\t\t\t\t:: " + s)
            """
            sintax = Sintaxis(lex)   # <--------------------------------- (SINTAXIS) (3)
            error = sintax.generaSintaxis()
            msgErrorSintax = sintax.mensajeError(error)
            self.log(f"ERROR DE SINTAXIS: {error} :: {msgErrorSintax}")
        else :
            self.log(f"ERROR DE LEXICO: {error} :: {token} :: {msgErrorLex}")
        self.log("Total de lineas procesadas: " + str(lex.getLineas()))
        
    def examen_semantico(self) :
        messagebox.showinfo("Mensaje", "Examen Semantico")

    def genByteCode(self) :
        messagebox.showinfo("Mensaje", "Generacion Byte-code")

    def ejecutar(self) :
        messagebox.showinfo("Mensaje", "Ejecucion de Codigo")




if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()


"""
(1) En LEXICO agregue una funcion (mensajeError()) para mostrar de manera un poco mas descriptiva el error
    mando como parámetro el error generado por generaLexico()

(2) Ya en SINTAXIS, antes de empezar con sintaxis, ejecuto lexico, para obtener la lista de tokens válidos
    nota: notarán que generaLexico() lleva un parámetro booleano. Cuando ejecuto LEXICO es True (significa 
    que tome en cuenta los comentarios y los aguegue a la lista, para presentarlos como parte de LEXICO ). 
    Si es False (en SINTAXIS), es para que los comentarios encontrados no los tome en  cuenta y no los 
    agregue a la lista de tokens válidos. Esto para "no perder tiempo" en sintaxis con algo que, para 
    sintaxis "no sirve para nada!!"

    nota 2: RECUERDEN, para el momento de SINTAXIS los token que llegan ya son válidos SI ó SI. Ahi no deben 
    entrar tokens inválidos. SINTAXIS solo verifica que los tokens estén en el orden adecuado

(3) Sintaxis recibe la tabla de Token que hizo Lexico para con ella empezar a revisar que todo este en el 
    orden que se especifica en el lenguaje (segunlos diagramas de sintaxis)

(4) Esta parte es para  no tener que estar abriendo un archvio de codigo cada vez que corro de nuevo el programa
    verificar el archivo compilador.ini. Ahí hay una variable (archivo) con el nombre de archivo (y su ruta)
    para que se abra en automatico. 

"""