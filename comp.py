"""
compilador
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

from lexico import *
from sintaxis import *
from bytecod import ByteCodeGenerator
from machin import MaquinaVirtual

class FlujoCompilacion:
    """Clase para manejar el flujo completo de compilación"""
    
    def __init__(self):
        self.lexico = None
        self.sintaxis = None
        self.generador = None
        self.maquina = None
    
    def compilar_y_ejecutar(self, codigo_fuente):
        """Ejecuta todo el flujo de compilación"""
        try:
            # 1. Análisis Léxico
            self.lexico = Lexico(codigo_fuente)
            error_lex, token = self.lexico.genera_lexico(False)
            
            if error_lex != ERR_NOERROR:
                return False, f"Error léxico: {self.lexico.mensaje_error(error_lex)}"
            
            # 2. Análisis Sintáctico
            self.sintaxis = Sintaxis(self.lexico)
            error_sintax = self.sintaxis.genera_sintaxis()
            
            if error_sintax != ERR_NO_SINTAX_ERROR:
                return False, f"Error sintáctico: {self.sintaxis.mensaje_error(error_sintax)}"
            
            # 3. Generación de Bytecode
            self.generador = ByteCodeGenerator()
            arbol = self.sintaxis.get_arbol_sintactico()
            tabla_simbolos = self.sintaxis.get_tabla_simbolos()
            
            bytecode = self.generador.generar_bytecode(arbol, tabla_simbolos)
            
            # 4. Ejecución
            if not self.maquina:
                self.maquina = MaquinaVirtual()
            
            self.maquina.cargar_codigo(bytecode)
            self.maquina.ejecutar()
            
            return True, "Ejecución completada exitosamente"
            
        except Exception as e:
            return False, f"Error en compilación: {str(e)}"

class Notepad:
    def _apply_editor_colors(self, event=None):
        for child in self.notebook.winfo_children():
            if isinstance(child, tk.Text):
                child.config(bg="#f5f5f5", fg="black", insertbackground="black")
    
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador AVL")
        self.root.geometry("1200x900")

        self.editor_font = font.Font(family="Consolas", size=12)
        self.bytecode_font = font.Font(family="Courier New", size=10)

        # Frame principal con paneles
        self.main_frame = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel izquierdo: Editor y consola
        self.left_panel = ttk.Panedwindow(self.main_frame, orient=tk.VERTICAL)
        self.main_frame.add(self.left_panel, weight=2)

        # Editor
        self.notebook = ttk.Notebook(self.left_panel)
        self.left_panel.add(self.notebook, weight=3)

        # Consola
        self.console_frame = ttk.LabelFrame(self.left_panel, text="Consola de Salida")
        self.left_panel.add(self.console_frame, weight=1)
        
        self.console = tk.Text(self.console_frame, height=8, bg="#1e1e1e", fg="#ffffff",
                               insertbackground="white", wrap="word", font=self.editor_font)
        self.console.config(state="disabled")
        
        scrollbar_console = ttk.Scrollbar(self.console_frame, orient="vertical", 
                                         command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar_console.set)
        
        self.console.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar_console.pack(side="right", fill="y")

        # Panel derecho: Byte-code y estado
        self.right_panel = ttk.Panedwindow(self.main_frame, orient=tk.VERTICAL)
        self.main_frame.add(self.right_panel, weight=1)

        # Byte-code
        self.bytecode_frame = ttk.LabelFrame(self.right_panel, text="Byte-Code Generado")
        self.right_panel.add(self.bytecode_frame, weight=2)

        self.bytecode_text = tk.Text(self.bytecode_frame, bg="#f0f0f0", wrap="none", 
                                    font=self.bytecode_font, height=15)
        scrollbar_bytecode = ttk.Scrollbar(self.bytecode_frame, orient="vertical", 
                                         command=self.bytecode_text.yview)
        self.bytecode_text.configure(yscrollcommand=scrollbar_bytecode.set)
        
        self.bytecode_text.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar_bytecode.pack(side="right", fill="y")

        # Estado de ejecución
        self.estado_frame = ttk.LabelFrame(self.right_panel, text="Estado de Ejecución")
        self.right_panel.add(self.estado_frame, weight=1)

        self.estado_text = tk.Text(self.estado_frame, bg="#e8f4f8", wrap="word", 
                                  font=self.bytecode_font, height=8)
        self.estado_text.pack(fill="both", expand=True, padx=2, pady=2)

        self.archivos = {}
        self.maquina_virtual = MaquinaVirtual()
        self.generador_bytecode = ByteCodeGenerator()
        self.flujo_compilacion = FlujoCompilacion()

        self._apply_editor_colors()
        self.crear_menu()
        self.crear_barra_herramientas()
        self.nuevo_archivo()

    def crear_barra_herramientas(self):
        """Crea una barra de herramientas para acciones rápidas"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(toolbar, text="Compilar", command=self.compilar_todo).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Ejecutar", command=self.ejecutar).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Limpiar", command=self.limpiar_consola).pack(side="left", padx=2)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(toolbar, text="Nuevo", command=self.nuevo_archivo).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Abrir", command=self.abrir_archivo).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Guardar", command=self.guardar_archivo).pack(side="left", padx=2)

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
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

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
        """Ejecuta todas las fases de compilación mostrando cada paso en consola"""
        self.log("\n" + "="*50)
        self.log("INICIANDO COMPILACIÓN COMPLETA")
        self.log("="*50)
        
        try:
            text_area = self.editor_actual()
            codigo_fuente = text_area.get("1.0", tk.END)
            
            # 1. ANÁLISIS LÉXICO
            self.log("\n--- ANÁLISIS LÉXICO ---")
            lex = Lexico(codigo_fuente)
            error_lex, token = lex.genera_lexico(False)
            
            if error_lex != ERR_NOERROR:
                self.log(f"✗ Error léxico: {lex.mensaje_error(error_lex)}")
                return
            else:
                self.log("✓ Análisis léxico completado exitosamente")
                # Mostrar tokens encontrados
                tokens = lex.get()
                self.log(f"✓ Se encontraron {len(tokens)} tokens")
                for i, (valor, tipo) in enumerate(tokens[:10]):  # Mostrar primeros 10 tokens
                    descripcion = lex.get_tipo_token_str(tipo, valor)
                    self.log(f"  {i+1}: '{valor}' -> {descripcion}")
                if len(tokens) > 10:
                    self.log(f"  ... y {len(tokens) - 10} tokens más")
            
            # 2. ANÁLISIS SINTÁCTICO
            self.log("\n--- ANÁLISIS SINTÁCTICO ---")
            sintaxis = Sintaxis(lex)
            error_sintax = sintaxis.genera_sintaxis()
            
            if error_sintax != ERR_NO_SINTAX_ERROR:
                self.log(f"✗ Error sintáctico: {sintaxis.mensaje_error(error_sintax)}")
                return
            else:
                self.log("✓ Análisis sintáctico completado exitosamente")
                arbol = sintaxis.get_arbol_sintactico()
                self.log(f"✓ Árbol sintáctico generado con {len(arbol['instrucciones'])} instrucciones")
            
            # 3. ANÁLISIS SEMÁNTICO
            self.log("\n--- ANÁLISIS SEMÁNTICO ---")
            errores_semanticos = sintaxis.get_errores_semanticos()
            if errores_semanticos:
                self.log("✗ Se encontraron errores semánticos:")
                for error in errores_semanticos:
                    self.log(f"  - {error}")
            else:
                self.log("✓ No se encontraron errores semánticos")
                
            # Mostrar tabla de símbolos
            lst_semantica = sintaxis.get_lista_identificadores()
            self.log(f"✓ Tabla de símbolos: {len(lst_semantica)} identificadores")
            for id_info in lst_semantica:
                tipo_str = sintaxis.get_str_tipo_identificador(id_info[1])
                self.log(f"  - {id_info[0]} :: {tipo_str} (línea {id_info[2]})")
            
            # 4. GENERACIÓN DE BYTECODE
            self.log("\n--- GENERACIÓN DE BYTECODE ---")
            arbol = sintaxis.get_arbol_sintactico()
            tabla_simbolos = sintaxis.get_tabla_simbolos()
            
            self.generador_bytecode = ByteCodeGenerator()
            bytecode = self.generador_bytecode.generar_bytecode(arbol, tabla_simbolos)
            
            # Mostrar bytecode generado
            bytecode_str = self.generador_bytecode.mostrar_bytecode()
            self.bytecode_text.delete("1.0", tk.END)
            self.bytecode_text.insert("1.0", bytecode_str)
            self.log("✓ Bytecode generado exitosamente")
            self.log(f"✓ Se generaron {len(bytecode)} instrucciones de bytecode")
            
            # 5. EJECUCIÓN
            self.log("\n--- EJECUCIÓN ---")
            self.configurar_entrada_interactiva()
            
            self.maquina_virtual.cargar_codigo(bytecode)
            self.maquina_virtual.ejecutar()
            
            # Mostrar resultados
            salida = self.maquina_virtual.obtener_salida()
            self.log("✓ Ejecución completada exitosamente")
            self.log("\n--- SALIDA DEL PROGRAMA ---")
            if salida:
                for linea in salida:
                    self.log(linea)
            else:
                self.log("(El programa no generó salida)")
            
            # Mostrar estado final
            self.log("\n--- ESTADO FINAL ---")
            estado = self.maquina_virtual.obtener_estado()
            self.log(f"Puntero: {estado['puntero']}")
            self.log(f"Pila: {estado['pila']}")
            self.log(f"Memoria: {estado['memoria']}")
            
            self.log("\n" + "="*50)
            self.log("COMPILACIÓN COMPLETADA EXITOSAMENTE")
            self.log("="*50)
            
        except Exception as e:
            self.log(f"✗ Error en compilación: {str(e)}")
            import traceback
            self.log(f"Detalle: {traceback.format_exc()}")

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
            text_area = self.editor_actual()
            codigo_fuente = text_area.get("1.0", tk.END)
            
            # Configurar entrada interactiva
            self.configurar_entrada_interactiva()
            
            # Análisis léxico
            lex = Lexico(codigo_fuente)
            error_lex, token = lex.genera_lexico(False)
            
            if error_lex != ERR_NOERROR:
                self.log(f"✗ Error léxico: {lex.mensaje_error(error_lex)}")
                return
            
            # Análisis sintáctico
            sintax = Sintaxis(lex)
            error_sintax = sintax.genera_sintaxis()
            
            if error_sintax != ERR_NO_SINTAX_ERROR:
                self.log(f"✗ Error sintáctico: {sintax.mensaje_error(error_sintax)}")
                return
            
            # Generar byte-code 
            arbol = sintax.get_arbol_sintactico()
            print("DEBUG - Árbol sintáctico completo:")
            for i, inst in enumerate(arbol['instrucciones']):
                print(f"  {i}: {inst}")
            tabla_simbolos = sintax.get_tabla_simbolos()
            
            self.generador_bytecode = ByteCodeGenerator()
            bytecode = self.generador_bytecode.generar_bytecode(arbol, tabla_simbolos)
            
            # Mostrar byte-code
            bytecode_str = self.generador_bytecode.mostrar_bytecode()
            self.bytecode_text.delete("1.0", tk.END)
            self.bytecode_text.insert("1.0", bytecode_str)
            
            # Ejecutar
            self.maquina_virtual.cargar_codigo(bytecode)
            self.maquina_virtual.ejecutar()
            
            # Mostrar resultados
            salida = self.maquina_virtual.obtener_salida()
            self.log("✓ Ejecución completada exitosamente")
            self.log("\n--- RESULTADOS ---")
            for linea in salida:
                self.log(linea)
            
            # Mostrar estado final
            self.mostrar_estado()
            
        except Exception as e:
            self.log(f"✗ Error en ejecución: {str(e)}")
            import traceback
            self.log(f"Detalle: {traceback.format_exc()}")

    def configurar_entrada_interactiva(self):
        """Configura callback para entrada de datos"""
        def callback_entrada(mensaje):
            # Crear ventana de diálogo para entrada
            from tkinter import simpledialog
            valor = simpledialog.askstring("Entrada de datos", mensaje)
            return valor if valor is not None else "0"
        
        self.maquina_virtual.configurar_entrada_interactiva(callback_entrada)

    def ejecutar_paso_a_paso(self):
        """Ejecuta el programa paso a paso"""
        self.log("\n--- EJECUCIÓN PASO A PASO ---")
        
        if self.maquina_virtual.ejecutar_paso_a_paso():
            estado = self.maquina_virtual.obtener_estado()
            self.log(f"✓ Instrucción ejecutada. Puntero: {estado['puntero']}")
            self.mostrar_estado()
        else:
            self.log("✓ Ejecución completada")

    def mostrar_estado(self):
        """Muestra el estado actual de la máquina virtual"""
        estado = self.maquina_virtual.obtener_estado()
        self.estado_text.delete("1.0", tk.END)
        
        estado_str = f"PUNTERO: {estado['puntero']}\n\n"
        estado_str += f"PILA: {estado['pila']}\n\n"
        estado_str += f"MEMORIA: {estado['memoria']}\n\n"
        estado_str += f"SALIDA: {estado.get('salida', [])}"
        
        self.estado_text.insert("1.0", estado_str)

    def reiniciar_ejecucion(self):
        """Reinicia la ejecución del programa"""
        self.maquina_virtual = MaquinaVirtual()
        self.estado_text.delete("1.0", tk.END)
        self.log("✓ Ejecución reiniciada")

    def editor_actual(self):
        tab = self.notebook.select()
        return self.notebook.nametowidget(tab)

    def nuevo_archivo(self):
        text_area = tk.Text(self.notebook, wrap="word", undo=True, font=self.editor_font)
        self.notebook.add(text_area, text="sin_título.avl")
        self.notebook.select(text_area)
        self.archivos[text_area] = None
        self.log("Nuevo archivo creado.")

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos avl", "*.avl"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
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
            defaultextension=".avl",
            filetypes=[("Archivos .avl", "*.avl"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", tk.END))
            nombre = file_path.split("/")[-1]
            self.notebook.tab(text_area, text=nombre)
            self.archivos[text_area] = file_path
            self.log(f"Archivo guardado como: {file_path}")

    def log(self, mensaje):
        self.console.config(state="normal")
        self.console.insert(tk.END, mensaje + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def limpiar_consola(self):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")
        self.log("Consola limpiada.")
        
    def examen_lexico(self):
        self.log("\n--- ANÁLISIS LÉXICO ---")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))

        error, token = lex.genera_lexico(True)
        msg_error = lex.mensaje_error(error)

        if error == ERR_NOERROR: 
            lst = lex.get()
            for c in lst:
                s = str(c[1]) + " - " + lex.get_tipo_token_str(c[1], c[0])
                self.log(c[0] + " \t:: " + s)
        else:
            self.log(f"Error: {error} :: {token} :: {msg_error}")
        self.log("Total de líneas procesadas: " + str(lex.get_lineas()))
        
    def examen_sintaxis(self):
        self.log("\n--- ANÁLISIS SINTÁCTICO ---")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))
        error, token = lex.genera_lexico(False)
        msg_error_lex = lex.mensaje_error(error)
        
        if error == ERR_NOERROR: 
            sintax = Sintaxis(lex)
            error = sintax.genera_sintaxis()
            msg_error_sintax = sintax.mensaje_error(error)
            
            if error == ERR_NO_SINTAX_ERROR:
                self.log("✓ Análisis sintáctico exitoso")
            else:
                self.log(f"✗ Error de sintaxis: {error} :: {msg_error_sintax}")
        else:
            self.log(f"✗ Error de léxico: {error} :: {token} :: {msg_error_lex}")
        
    def examen_semantico(self):
        self.log("\n--- ANÁLISIS SEMÁNTICO ---")
        text_area = self.editor_actual()
        lex = Lexico(text_area.get("1.0", tk.END))
        error, token = lex.genera_lexico(False)
        
        if error == ERR_NOERROR: 
            sintax = Sintaxis(lex)
            error = sintax.genera_sintaxis()
            
            if error == ERR_NO_SINTAX_ERROR:
                # Mostrar errores semánticos
                errores_semanticos = sintax.get_errores_semanticos()
                if errores_semanticos:
                    self.log("--- ERRORES SEMÁNTICOS ENCONTRADOS ---")
                    for error_sem in errores_semanticos:
                        self.log(f"✗ {error_sem}")
                else:
                    self.log("✓ No se encontraron errores semánticos")
                
                # Mostrar tabla de símbolos
                lst_semantica = sintax.get_lista_identificadores()
                self.log("\n--- TABLA DE SÍMBOLOS ---")
                for id in lst_semantica:
                    s = f"{id[0]} :: {sintax.get_str_tipo_identificador(id[1])}"
                    self.log("   " + s)
            else:
                self.log("✗ No se puede realizar análisis semántico debido a errores sintácticos")
        else:
            self.log(f"✗ Error de léxico: {error} :: {token} :: {lex.mensaje_error(error)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()