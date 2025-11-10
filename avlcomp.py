"""
compilador.py
compilador para lenguaje orientado a objetos en español
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

from avllexico import *
from avlsintaxis import *

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("compilador - lenguaje oo español")
        self.root.geometry("1000x800")

        self.editor_font = font.Font(family="Consolas", size=12)

        self.main_frame = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.main_frame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.main_frame)
        self.main_frame.add(self.notebook, weight=4)

        self.console = tk.Text(self.main_frame, height=8, bg="#1e1e1e", fg="white",
                               insertbackground="white", wrap="word")
        self.console.config(state="disabled")
        self.main_frame.add(self.console, weight=1)

        self.archivos = {}

        self.crear_menu()
        self.nuevo_archivo()

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="abrir...", command=self.abrir_archivo)
        archivo_menu.add_command(label="guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="guardar como...", command=self.guardar_como)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="salir", command=self.root.quit)
        menubar.add_cascade(label="archivo", menu=archivo_menu)

        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="cortar", command=lambda: self.editor_actual().event_generate("<<Cut>>"))
        edicion_menu.add_command(label="copiar", command=lambda: self.editor_actual().event_generate("<<Copy>>"))
        edicion_menu.add_command(label="pegar", command=lambda: self.editor_actual().event_generate("<<Paste>>"))
        menubar.add_cascade(label="edición", menu=edicion_menu)

        consola_menu = tk.Menu(menubar, tearoff=0)
        consola_menu.add_command(label="limpiar consola", command=self.limpiar_consola)
        menubar.add_cascade(label="consola", menu=consola_menu)
        
        fases_menu = tk.Menu(menubar, tearoff=0)
        fases_menu.add_command(label="análisis léxico", command=self.examen_lexico)
        fases_menu.add_command(label="análisis sintáctico", command=self.examen_sintaxis)
        fases_menu.add_command(label="análisis semántico", command=self.examen_semantico)
        fases_menu.add_command(label="generación byte-code", command=self.gen_bytecode)
        fases_menu.add_command(label="ejecución de programa", command=self.ejecutar)
        menubar.add_cascade(label="fases de compilación", menu=fases_menu)

    def editor_actual(self):
        tab = self.notebook.select()
        return self.notebook.nametowidget(tab)

    def nuevo_archivo(self):
        text_area = tk.Text(self.notebook, wrap="word", undo=True, font=self.editor_font)
        self.notebook.add(text_area, text="sin_título.oo")
        self.notebook.select(text_area)
        self.archivos[text_area] = None
        self.log("nuevo archivo creado.")

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("archivos oo", "*.oo"), ("archivos de texto", "*.txt"), ("todos los archivos", "*.*")]
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
            self.log(f"archivo abierto: {file_path}")

    def guardar_archivo(self):
        text_area = self.editor_actual()
        file_path = self.archivos.get(text_area)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", tk.END))
            self.log(f"archivo guardado: {file_path}")
        else:
            self.guardar_como()

    def guardar_como(self):
        text_area = self.editor_actual()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".oo",
            filetypes=[("archivos oo", "*.oo"), ("archivos de texto", "*.txt"), ("todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", tk.END))
            nombre = file_path.split("/")[-1]
            self.notebook.tab(text_area, text=nombre)
            self.archivos[text_area] = file_path
            self.log(f"archivo guardado como: {file_path}")

    def log(self, mensaje):
        self.console.config(state="normal")
        self.console.insert(tk.END, mensaje + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def limpiar_consola(self):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")
        self.log("consola limpiada.")
        
    def examen_lexico(self):
        self.log("\n\niniciando análisis léxico")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))

        error, token = lex.genera_lexico(True)
        msg_error = lex.mensaje_error(error)

        if error == ERR_NOERROR: 
            lst = lex.get()
            for c in lst:
                s = str(c[1]) + "-" + lex.get_tipo_token_str(c[1], c[0])
                self.log(c[0] + " \t\t\t\t\t:: " + s)
        else:
            self.log(f"error: {error} :: {token} :: {msg_error}")
        self.log("total de líneas procesadas: " + str(lex.get_lineas()))
        
    def examen_sintaxis(self):
        self.log("\n\niniciando análisis sintáctico")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))
        error, token = lex.genera_lexico(False)
        msg_error_lex = lex.mensaje_error(error)
        
        if error == ERR_NOERROR: 
            sintax = Sintaxis(lex)
            error = sintax.genera_sintaxis()
            msg_error_sintax = sintax.mensaje_error(error)
            self.log(f"error de sintaxis: {error} :: {msg_error_sintax}")
        else:
            self.log(f"error de léxico: {error} :: {token} :: {msg_error_lex}")
        self.log("total de líneas procesadas: " + str(lex.get_lineas()))
        
    def examen_semantico(self):
        self.log("\n\niniciando análisis semántico")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))
        error, token = lex.genera_lexico(False)
        msg_error_lex = lex.mensaje_error(error)
        
        if error == ERR_NOERROR: 
            sintax = Sintaxis(lex)
            error = sintax.genera_sintaxis()
            msg_error_sintax = sintax.mensaje_error(error)
            self.log(f"{error} :: {msg_error_sintax}")

            if error == ERR_NO_SINTAX_ERROR:
                lst_semantica = sintax.get_lista_identificadores()
                self.log("lista de identificadores")
                for id in lst_semantica:
                    s = f"{id[0]} :: " + sintax.get_str_tipo_identificador(id[1])
                    self.log("   " + s)
        else:
            self.log(f"error de léxico: {error} :: {token} :: {msg_error_lex}")
        self.log("total de líneas procesadas: " + str(lex.get_lineas()))

    def gen_bytecode(self):
        messagebox.showinfo("mensaje", "generación de byte-code")

    def ejecutar(self):
        messagebox.showinfo("mensaje", "ejecución de código")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()