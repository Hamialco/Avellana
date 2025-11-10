"""
compilador
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

from avllexico import *
from avlsintaxis import *
from avlbytec import ByteCodeGenerator
from avlmach import MaquinaVirtual

class Notepad:
    def _apply_editor_colors(self, event=None):
        for child in self.notebook.winfo_children():
            if isinstance(child, tk.Text):
                child.config(bg="#c85cfa", fg="black", insertbackground="black")
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador")
        self.root.geometry("1200x900")

        self.editor_font = font.Font(family="Consolas", size=12)
        self.bytecode_font = font.Font(family="Courier New", size=10)

        # Frame principal con paneles
        self.main_frame = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill="both", expand=True)

        # Panel izquierdo: Editor y consola
        self.left_panel = ttk.Panedwindow(self.main_frame, orient=tk.VERTICAL)
        self.main_frame.add(self.left_panel, weight=2)

        # Editor
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.bind("<<NotebookTabChanged>>", self._apply_editor_colors)
        self.left_panel.add(self.notebook, weight=3)

        # Consola
        self.console = tk.Text(self.left_panel, height=8, bg="#1e1e1e", fg="#c85cfa",
                               insertbackground="white", wrap="word", font=self.editor_font)
        self.console.config(state="disabled")
        self.left_panel.add(self.console, weight=1)

        # Panel derecho: Byte-code y estado
        self.right_panel = ttk.Panedwindow(self.main_frame, orient=tk.VERTICAL)
        self.main_frame.add(self.right_panel, weight=1)

        # Byte-code
        self.bytecode_frame = ttk.LabelFrame(self.right_panel, text="Byte-Code Generado")
        self.right_panel.add(self.bytecode_frame, weight=2)

        self.bytecode_text = tk.Text(self.bytecode_frame, bg="#f0f0f0", wrap="word", 
                                    font=self.bytecode_font, height=15)
        scrollbar_bytecode = ttk.Scrollbar(self.bytecode_frame, orient="vertical", 
                                         command=self.bytecode_text.yview)
        self.bytecode_text.configure(yscrollcommand=scrollbar_bytecode.set)
        
        self.bytecode_text.pack(side="left", fill="both", expand=True)
        scrollbar_bytecode.pack(side="right", fill="y")

        # Estado de ejecución
        self.estado_frame = ttk.LabelFrame(self.right_panel, text="Estado de Ejecución")
        self.right_panel.add(self.estado_frame, weight=1)

        self.estado_text = tk.Text(self.estado_frame, bg="#e8f4f8", wrap="word", 
                                  font=self.bytecode_font, height=8)
        self.estado_text.pack(fill="both", expand=True)

        self.archivos = {}
        self.maquina_virtual = MaquinaVirtual()
        self.generador_bytecode = ByteCodeGenerator()

        self._apply_editor_colors()
        self.crear_menu()
        self.nuevo_archivo()
        self.cargar_ejemplos()

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Ctrl+N")
        archivo_menu.add_command(label="Abrir...", command=self.abrir_archivo, accelerator="Ctrl+O")
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Ctrl+S")
        archivo_menu.add_command(label="Guardar como...", command=self.guardar_como)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Ejemplos", command=self.mostrar_ejemplos)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        # Menú Edición
        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="Cortar", command=lambda: self.editor_actual().event_generate("<<Cut>>"))
        edicion_menu.add_command(label="Copiar", command=lambda: self.editor_actual().event_generate("<<Copy>>"))
        edicion_menu.add_command(label="Pegar", command=lambda: self.editor_actual().event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edición", menu=edicion_menu)

        # Menú Compilación
        compilacion_menu = tk.Menu(menubar, tearoff=0)
        compilacion_menu.add_command(label="Compilar Todo", command=self.compilar_todo)
        compilacion_menu.add_separator()
        compilacion_menu.add_command(label="Análisis Léxico", command=self.examen_lexico)
        compilacion_menu.add_command(label="Análisis Sintáctico", command=self.examen_sintaxis)
        compilacion_menu.add_command(label="Análisis Semántico", command=self.examen_semantico)
        compilacion_menu.add_command(label="Generación Byte-Code", command=self.gen_bytecode)
        compilacion_menu.add_command(label="Ejecutar Programa", command=self.ejecutar)
        menubar.add_cascade(label="Compilación", menu=compilacion_menu)

        # Menú Depuración
        depuracion_menu = tk.Menu(menubar, tearoff=0)
        depuracion_menu.add_command(label="Paso a Paso", command=self.ejecutar_paso_a_paso)
        depuracion_menu.add_command(label="Ver Estado", command=self.mostrar_estado)
        depuracion_menu.add_command(label="Reiniciar Ejecución", command=self.reiniciar_ejecucion)
        menubar.add_cascade(label="Depuración", menu=depuracion_menu)

        # Menú Consola
        consola_menu = tk.Menu(menubar, tearoff=0)
        consola_menu.add_command(label="Limpiar Consola", command=self.limpiar_consola)
        menubar.add_cascade(label="Consola", menu=consola_menu)

        # Atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.nuevo_archivo())
        self.root.bind('<Control-o>', lambda e: self.abrir_archivo())
        self.root.bind('<Control-s>', lambda e: self.guardar_archivo())

    def compilar_todo(self):
        """Ejecuta todas las fases de compilación"""
        self.log("\n" + "="*50)
        self.log("INICIANDO COMPILACIÓN COMPLETA")
        self.log("="*50)
        
        # Fase 1: Análisis Léxico
        self.examen_lexico()
        
        # Fase 2: Análisis Sintáctico
        self.examen_sintaxis()
        
        # Fase 3: Análisis Semántico
        self.examen_semantico()
        
        # Fase 4: Generación de Byte-Code
        self.gen_bytecode()
        
        self.log("\n" + "="*50)
        self.log("COMPILACIÓN COMPLETADA")
        self.log("="*50)

    def gen_bytecode(self):
        """Genera y muestra el byte-code"""
        self.log("\n--- GENERACIÓN DE BYTE-CODE ---")
        
        text_area = self.editor_actual()
        codigo_fuente = text_area.get("1.0", tk.END)
        
        try:
            # Análisis léxico y sintáctico
            lex = Lexico(codigo_fuente)
            error_lex, token = lex.genera_lexico(False)
            
            if error_lex != ERR_NOERROR:
                self.log(f"Error léxico: {lex.mensaje_error(error_lex)}")
                return
                
            sintax = Sintaxis(lex)
            error_sintax = sintax.genera_sintaxis()
            
            if error_sintax != ERR_NO_SINTAX_ERROR:
                self.log(f"Error sintáctico: {sintax.mensaje_error(error_sintax)}")
                return
            
            # Generar byte-code (simulado por ahora)
            bytecode_simulado = self._generar_bytecode_simulado(codigo_fuente)
            
            # Mostrar en panel de byte-code
            self.bytecode_text.delete("1.0", tk.END)
            self.bytecode_text.insert("1.0", bytecode_simulado)
            
            self.log("✓ Byte-code generado exitosamente")
            self.log("✓ Revise el panel de Byte-Code para ver el resultado")
            
        except Exception as e:
            self.log(f"✗ Error en generación de byte-code: {str(e)}")

    def _generar_bytecode_simulado(self, codigo_fuente):
        """Genera byte-code simulado para demostración"""
        lineas = codigo_fuente.split('\n')
        bytecode = ";; BYTE-CODE GENERADO AUTOMÁTICAMENTE\n\n"
        
        for i, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
                
            bytecode += f";; Línea {i}: {linea}\n"
            
            if 'imprimir(' in linea:
                if '"' in linea:
                    texto = linea.split('"')[1]
                    bytecode += f'  PUSH "{texto}"\n'
                    bytecode += '  PRINT\n'
                else:
                    bytecode += '  LOAD var\n'
                    bytecode += '  PRINT\n'
                    
            elif 'entero' in linea and '=' in linea:
                var = linea.split('entero')[1].split('=')[0].strip()
                valor = linea.split('=')[1].split('#')[0].strip()
                bytecode += f'  PUSH {valor}\n'
                bytecode += f'  STORE {var}\n'
                
            elif 'mientras' in linea:
                bytecode += 'L0:\n'
                
            elif 'fin_mientras' in linea:
                bytecode += '  JMP L0\n'
                bytecode += 'L1:\n'
                
        bytecode += '\n  HALT\n'
        return bytecode

    def ejecutar(self):
        """Ejecuta el programa compilado"""
        self.log("\n--- EJECUCIÓN DEL PROGRAMA ---")
        
        try:
            # Simulación de ejecución
            codigo_fuente = self.editor_actual().get("1.0", tk.END)
            self._simular_ejecucion(codigo_fuente)
            
            self.log("✓ Ejecución completada")
            
        except Exception as e:
            self.log(f"✗ Error en ejecución: {str(e)}")

    def _simular_ejecucion(self, codigo_fuente):
        """Simula la ejecución del programa"""
        lineas = codigo_fuente.split('\n')
        variables = {}
        
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            if not linea or linea.startswith('#'):
                i += 1
                continue
                
            # Simular diferentes instrucciones
            if 'imprimir(' in linea:
                if '"' in linea:
                    texto = linea.split('"')[1]
                    self.log(f"[SALIDA] {texto}")
                else:
                    # Buscar variable entre paréntesis
                    contenido = linea.split('(')[1].split(')')[0].strip()
                    if contenido in variables:
                        self.log(f"[SALIDA] {variables[contenido]}")
            elif 'entero' in linea and '=' in linea:
                var = linea.split('entero')[1].split('=')[0].strip()
                valor = eval(linea.split('=')[1].split('#')[0].strip())
                variables[var] = valor
                self.log(f"[VARIABLE] {var} = {valor}")
            elif 'leer(' in linea:
                var = linea.split('(')[1].split(')')[0].strip()
                # Simular entrada (para demo usamos valores predefinidos)
                valores_simulados = {'nombre': '"Juan"', 'edad': '25', 'x': '10', 'y': '5'}
                if var in valores_simulados:
                    variables[var] = eval(valores_simulados[var])
                    self.log(f"[ENTRADA] {var} = {variables[var]}")
            elif 'mientras' in linea:
                # Simular ciclo while
                cond_var = linea.split('mientras')[1].split('<=')[0].strip()
                limite = int(linea.split('<=')[1].split(':')[0].strip())
                
                if cond_var in variables:
                    while variables[cond_var] <= limite:
                        # Ejecutar cuerpo del ciclo
                        j = i + 1
                        while j < len(lineas) and 'fin_mientras' not in lineas[j]:
                            linea_cuerpo = lineas[j].strip()
                            if 'imprimir(' in linea_cuerpo and cond_var in linea_cuerpo:
                                self.log(f"[SALIDA] {variables[cond_var]}")
                            elif cond_var + ' = ' in linea_cuerpo:
                                variables[cond_var] += 1
                            j += 1
                        # Actualizar contador
                        if variables[cond_var] <= limite:
                            continue
                        else:
                            break
                i = j  # Saltar al final del ciclo
                
            i += 1

    def ejecutar_paso_a_paso(self):
        """Ejecuta el programa paso a paso"""
        self.log("\n--- EJECUCIÓN PASO A PASO ---")
        self.log("(Funcionalidad en desarrollo)")
        
    def mostrar_estado(self):
        """Muestra el estado actual de la máquina virtual"""
        estado = self.maquina_virtual.obtener_estado()
        self.estado_text.delete("1.0", tk.END)
        self.estado_text.insert("1.0", 
                               f"Pila: {estado['pila']}\n"
                               f"Memoria: {estado['memoria']}\n"
                               f"Puntero: {estado['puntero']}")

    def reiniciar_ejecucion(self):
        """Reinicia la ejecución del programa"""
        self.maquina_virtual = MaquinaVirtual()
        self.estado_text.delete("1.0", tk.END)
        self.log("✓ Ejecución reiniciada")
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
        """Genera y muestra el byte-code"""
        self.log("\n--- GENERACIÓN DE BYTE-CODE ---")
        
        try:
            text_area = self.editor_actual()
            codigo_fuente = text_area.get("1.0", tk.END)
            
            # Análisis léxico
            lex = Lexico(codigo_fuente)
            error_lex, token = lex.genera_lexico(False)
            
            if error_lex != ERR_NOERROR:
                self.log(f"✗ Error léxico: {lex.mensaje_error(error_lex)}")
                return
                
            # Análisis sintáctico y semántico
            sintaxis = Sintaxis(lex)
            error_sintax = sintaxis.genera_sintaxis()
            
            if error_sintax != ERR_NO_SINTAX_ERROR:
                self.log(f"✗ Error sintáctico: {sintaxis.mensaje_error(error_sintax)}")
                return
            
            # Generar byte-code real
            arbol = sintaxis.get_arbol_sintactico()
            tabla_simbolos = sintaxis.get_tabla_simbolos()
            bytecode = self.generador_bytecode.generar_bytecode(arbol, tabla_simbolos)
            
            # Mostrar en panel
            bytecode_str = self.generador_bytecode.mostrar_bytecode()
            self.bytecode_text.delete("1.0", tk.END)
            self.bytecode_text.insert("1.0", bytecode_str)
            
            self.log("✓ Byte-code generado exitosamente")
            self.log("✓ Revise el panel de Byte-Code para ver el resultado")
            
        except Exception as e:
            self.log(f"✗ Error en generación de byte-code: {str(e)}")

    def ejecutar(self):
        """Ejecuta el programa compilado"""
        self.log("\n--- EJECUCIÓN DEL PROGRAMA ---")
        
        try:
            # Ejecutar en máquina virtual
            self.maquina_virtual.ejecutar()
            salida = self.maquina_virtual.obtener_salida()
            
            # Mostrar resultados
            self.log("✓ Ejecución completada")
            self.log("\n--- RESULTADOS ---")
            for linea in salida:
                self.log(linea)
            
            # Mostrar estado final
            estado = self.maquina_virtual.obtener_estado()
            self.estado_text.delete("1.0", tk.END)
            self.estado_text.insert("1.0", 
                                   f"Pila: {estado['pila']}\n"
                                   f"Memoria: {estado['memoria']}\n"
                                   f"Salida: {estado['salida']}")
            
        except Exception as e:
            self.log(f"✗ Error en ejecución: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()