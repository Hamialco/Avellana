"""
Compilador Avellana
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, simpledialog
from avllexico import *

# --- PARSER v4 ---
class ParserAvellana:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.error = None
        self.mensaje = ""
        self.ast = []
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = (None, None, None)
        return self.current_token

    def peek_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None, None)

    def match(self, expected_type):
        if self.current_token[1] == expected_type:
            token = self.current_token
            self.next_token()
            return token
        return None

    def error_sintaxis(self, mensaje):
        self.error = self.current_token[2] if self.current_token else 0
        self.mensaje = f"Error sintáctico: {mensaje}. Encontrado: {self.current_token[0]}"
        return None

def parse(self):
    """Analiza el programa completo"""
    while self.current_token[0] is not None:
        # Ignorar comentarios y saltos de línea
        if self.current_token[1] in [LIN_HASH, LIN_EOLN]:
            self.next_token()
            continue
            
        # Declaraciones globales
        if self.current_token[1] in [RES_SEA, RES_SEAN]:
            decl = self.parse_declaracion()
            if decl:
                self.ast.append(decl)
            else:
                return False
        elif self.current_token[1] == RES_DEFINE:
            decl = self.parse_definicion()
            if decl:
                self.ast.append(decl)
            else:
                return False
        elif self.current_token[1] in [RES_IMPRIMIR, RES_LEER]:
            # Llamadas a funciones de E/S
            llamada = self.parse_llamada_especial()
            if llamada:
                self.ast.append(llamada)
            else:
                return False
        elif self.current_token[1] == LIN_HASH:
            # Ignorar comentarios
            self.next_token()
        else:
            # Expresión o statement
            expr = self.parse_statement()
            if expr:
                self.ast.append(expr)
            else:
                return False
    return True

    def parse_llamada_especial(self):
        """Parse para imprimir y leer"""
        inicio_linea = self.current_token[2]
        
        if self.current_token[1] == RES_IMPRIMIR:
            if not self.match(RES_IMPRIMIR):
                return self.error_sintaxis("Se esperaba 'imprimir'")
            
            # Parsear argumentos
            argumentos = []
            if self.match(LIN_PAREN_ABRE):
                while not self.match(LIN_PAREN_CIERRA):
                    expr = self.parse_expresion()
                    if expr:
                        argumentos.append(expr)
                    if not self.match(LIN_COMA):
                        break
            
            return {
                'tipo': 'llamada_imprimir',
                'argumentos': argumentos,
                'linea': inicio_linea
            }
            
        elif self.current_token[1] == RES_LEER:
            if not self.match(RES_LEER):
                return self.error_sintaxis("Se esperaba 'leer'")
            
            # Parsear parámetro opcional (mensaje)
            mensaje = None
            if self.match(LIN_PAREN_ABRE):
                if self.peek_token()[1] != LIN_PAREN_CIERRA:
                    mensaje = self.parse_expresion()
                if not self.match(LIN_PAREN_CIERRA):
                    return self.error_sintaxis("Se esperaba ')'")
            
            return {
                'tipo': 'llamada_leer',
                'mensaje': mensaje,
                'linea': inicio_linea
            }
        
        return None

    # [Los demás métodos del parser permanecen igual...]
    def parse_declaracion(self):
        """sea|sean <identificador> [= <expresion>]"""
        inicio_linea = self.current_token[2]
        tipo_decl = self.current_token[1]
        
        if not self.match(tipo_decl):
            return self.error_sintaxis(f"Se esperaba '{'sea' if tipo_decl == RES_SEA else 'sean'}'")

        # Lista de identificadores
        identificadores = []
        while True:
            token_ident = self.match(LIN_IDENTIFICADOR)
            if token_ident:
                identificadores.append(token_ident[0])
            else:
                return self.error_sintaxis("Se esperaba identificador")

            # Verificar si hay más identificadores
            if self.match(LIN_COMA):
                continue
            else:
                break

        # Asignación opcional
        asignaciones = []
        if self.match(LIN_IGUAL):
            for ident in identificadores:
                expr = self.parse_expresion()
                if not expr:
                    return self.error_sintaxis("Se esperaba expresión después de '='")
                asignaciones.append({'variable': ident, 'valor': expr})

        return {
            'tipo': 'declaracion',
            'tipo_decl': tipo_decl,
            'identificadores': identificadores,
            'asignaciones': asignaciones,
            'linea': inicio_linea
        }

    def parse_definicion(self):
        """define <nombre> como_clase|como_funcion ..."""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_DEFINE):
            return self.error_sintaxis("Se esperaba 'define'")

        if not self.match(LIN_IDENTIFICADOR):
            return self.error_sintaxis("Se esperaba nombre después de 'define'")
        nombre = self.current_token[0]

        # Definición de clase
        if self.match(RES_COMO_CLASE):
            return self.parse_clase(nombre, inicio_linea)
        # Definición de función
        elif self.match(RES_COMO):
            if not self.match(LIN_IDENTIFICADOR):  # 'funcion' o tipo
                return self.error_sintaxis("Se esperaba 'funcion' o tipo después de 'como'")
            return self.parse_funcion(nombre, inicio_linea)
        else:
            return self.error_sintaxis("Se esperaba 'como_clase' o 'como funcion'")

    def parse_clase(self, nombre, linea):
        """define <nombre> como_clase ... fin"""
        propiedades = []
        metodos = []

        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            if self.match(RES_PROPIEDAD):
                if self.match(LIN_IDENTIFICADOR):
                    propiedades.append(self.current_token[0])
                else:
                    return self.error_sintaxis("Se esperaba nombre de propiedad")
            elif self.match(RES_HACE):
                metodo = self.parse_metodo()
                if metodo:
                    metodos.append(metodo)
                else:
                    return None
            elif self.match(LIN_EOLN):
                continue  # Ignorar saltos de línea
            else:
                return self.error_sintaxis("Se esperaba 'propiedad', 'hace' o 'fin'")

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar la clase")

        return {
            'tipo': 'clase',
            'nombre': nombre,
            'propiedades': propiedades,
            'metodos': metodos,
            'linea': linea
        }

    def parse_funcion(self, nombre, linea):
        """define <nombre> como funcion ... fin"""
        parametros = []
        cuerpo = []

        # Parámetros opcionales
        if self.match(LIN_PAREN_ABRE):
            while not self.match(LIN_PAREN_CIERRA):
                token_param = self.match(LIN_IDENTIFICADOR)
                if token_param:
                    parametros.append(token_param[0])
                if not self.match(LIN_COMA):
                    break

        # Cuerpo de la función
        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            stmt = self.parse_statement()
            if stmt:
                cuerpo.append(stmt)
            elif self.match(LIN_EOLN):
                continue
            else:
                return self.error_sintaxis("Error en cuerpo de función")

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar la función")

        return {
            'tipo': 'funcion',
            'nombre': nombre,
            'parametros': parametros,
            'cuerpo': cuerpo,
            'linea': linea
        }

    def parse_metodo(self):
        """hace <nombre> ... fin"""
        if not self.match(LIN_IDENTIFICADOR):
            return self.error_sintaxis("Se esperaba nombre del método")
        nombre = self.current_token[0]

        cuerpo = []
        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            stmt = self.parse_statement()
            if stmt:
                cuerpo.append(stmt)
            elif self.match(LIN_EOLN):
                continue
            else:
                return None

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar el método")

        return {
            'tipo': 'metodo',
            'nombre': nombre,
            'cuerpo': cuerpo
        }

    def parse_statement(self):
        """Statement: asignación, si, mientras, por_cada, etc."""
        if self.current_token[1] == RES_SI:
            return self.parse_si()
        elif self.current_token[1] == RES_MIENTRAS:
            return self.parse_mientras()
        elif self.current_token[1] == RES_POR_CADA:
            return self.parse_por_cada()
        elif self.current_token[1] == RES_REPETIR:
            return self.parse_repetir()
        elif self.current_token[1] == LIN_IDENTIFICADOR:
            # Asignación o llamada de función
            return self.parse_asignacion_o_llamada()
        elif self.current_token[1] == RES_RETORNA:
            return self.parse_retorna()
        elif self.current_token[1] in [RES_IMPRIMIR, RES_LEER]:
            return self.parse_llamada_especial()
        elif self.match(LIN_EOLN):
            return None  # Statement vacío
        else:
            return self.error_sintaxis("Statement no válido")

    def parse_si(self):
        """si <condicion> entonces ... [si_no ...] fin"""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_SI):
            return self.error_sintaxis("Se esperaba 'si'")

        condicion = self.parse_expresion()
        if not condicion:
            return self.error_sintaxis("Se esperaba condición después de 'si'")

        if not self.match(RES_ENTONCES):
            return self.error_sintaxis("Se esperaba 'entonces'")

        cuerpo_si = []
        cuerpo_si_no = []

        # Cuerpo del SI
        while (self.current_token[0] is not None and 
               self.current_token[1] not in [RES_SI_NO, RES_FIN, RES_O_SI]):
            stmt = self.parse_statement()
            if stmt:
                cuerpo_si.append(stmt)
            elif not self.match(LIN_EOLN):
                break

        # O_SI (else if) opcional
        o_sis = []
        while self.match(RES_O_SI):
            cond_o_si = self.parse_expresion()
            if not cond_o_si:
                return self.error_sintaxis("Se esperaba condición después de 'o_si'")
            if not self.match(RES_ENTONCES):
                return self.error_sintaxis("Se esperaba 'entonces' después de condición")

            cuerpo_o_si = []
            while (self.current_token[0] is not None and 
                   self.current_token[1] not in [RES_SI_NO, RES_FIN, RES_O_SI]):
                stmt = self.parse_statement()
                if stmt:
                    cuerpo_o_si.append(stmt)
                elif not self.match(LIN_EOLN):
                    break

            o_sis.append({'condicion': cond_o_si, 'cuerpo': cuerpo_o_si})

        # SI_NO opcional
        if self.match(RES_SI_NO):
            while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
                stmt = self.parse_statement()
                if stmt:
                    cuerpo_si_no.append(stmt)
                elif not self.match(LIN_EOLN):
                    break

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar el 'si'")

        return {
            'tipo': 'si',
            'condicion': condicion,
            'cuerpo_si': cuerpo_si,
            'o_sis': o_sis,
            'cuerpo_si_no': cuerpo_si_no,
            'linea': inicio_linea
        }

    def parse_mientras(self):
        """mientras <condicion> hace ... fin"""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_MIENTRAS):
            return self.error_sintaxis("Se esperaba 'mientras'")

        condicion = self.parse_expresion()
        if not condicion:
            return self.error_sintaxis("Se esperaba condición después de 'mientras'")

        if not self.match(RES_HACE):
            return self.error_sintaxis("Se esperaba 'hace'")

        cuerpo = []
        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            stmt = self.parse_statement()
            if stmt:
                cuerpo.append(stmt)
            elif not self.match(LIN_EOLN):
                break

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar el 'mientras'")

        return {
            'tipo': 'mientras',
            'condicion': condicion,
            'cuerpo': cuerpo,
            'linea': inicio_linea
        }

    def parse_por_cada(self):
        """por_cada <variable> en <expresion> hace ... fin"""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_POR_CADA):
            return self.error_sintaxis("Se esperaba 'por_cada'")

        if not self.match(LIN_IDENTIFICADOR):
            return self.error_sintaxis("Se esperaba variable después de 'por_cada'")
        variable = self.current_token[0]

        if not self.match(RES_EN):
            return self.error_sintaxis("Se esperaba 'en'")

        expresion = self.parse_expresion()
        if not expresion:
            return self.error_sintaxis("Se esperaba expresión después de 'en'")

        if not self.match(RES_HACE):
            return self.error_sintaxis("Se esperaba 'hace'")

        cuerpo = []
        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            stmt = self.parse_statement()
            if stmt:
                cuerpo.append(stmt)
            elif not self.match(LIN_EOLN):
                break

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar el 'por_cada'")

        return {
            'tipo': 'por_cada',
            'variable': variable,
            'coleccion': expresion,
            'cuerpo': cuerpo,
            'linea': inicio_linea
        }

    def parse_repetir(self):
        """repetir <veces> hace ... fin"""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_REPETIR):
            return self.error_sintaxis("Se esperaba 'repetir'")

        veces = self.parse_expresion()
        if not veces:
            return self.error_sintaxis("Se esperaba expresión después de 'repetir'")

        if not self.match(RES_HACE):
            return self.error_sintaxis("Se esperaba 'hace'")

        cuerpo = []
        while self.current_token[0] is not None and self.current_token[1] != RES_FIN:
            stmt = self.parse_statement()
            if stmt:
                cuerpo.append(stmt)
            elif not self.match(LIN_EOLN):
                break

        if not self.match(RES_FIN):
            return self.error_sintaxis("Se esperaba 'fin' para cerrar el 'repetir'")

        return {
            'tipo': 'repetir',
            'veces': veces,
            'cuerpo': cuerpo,
            'linea': inicio_linea
        }

    def parse_asignacion_o_llamada(self):
        """<identificador> = <expresion> | <identificador>(<argumentos>)"""
        inicio_linea = self.current_token[2]
        identificador = self.current_token[0]
        
        if not self.match(LIN_IDENTIFICADOR):
            return self.error_sintaxis("Se esperaba identificador")

        # Asignación
        if self.match(LIN_IGUAL):
            expresion = self.parse_expresion()
            if not expresion:
                return self.error_sintaxis("Se esperaba expresión después de '='")
            return {
                'tipo': 'asignacion',
                'variable': identificador,
                'valor': expresion,
                'linea': inicio_linea
            }
        # Llamada a función
        elif self.match(LIN_PAREN_ABRE):
            argumentos = []
            while not self.match(LIN_PAREN_CIERRA):
                expr = self.parse_expresion()
                if expr:
                    argumentos.append(expr)
                if not self.match(LIN_COMA):
                    break
            return {
                'tipo': 'llamada_funcion',
                'nombre': identificador,
                'argumentos': argumentos,
                'linea': inicio_linea
            }
        else:
            return self.error_sintaxis("Se esperaba '=' o '(' después del identificador")

    def parse_retorna(self):
        """retorna <expresion>"""
        inicio_linea = self.current_token[2]
        
        if not self.match(RES_RETORNA):
            return self.error_sintaxis("Se esperaba 'retorna'")

        expresion = self.parse_expresion()
        if not expresion:
            return self.error_sintaxis("Se esperaba expresión después de 'retorna'")

        return {
            'tipo': 'retorna',
            'valor': expresion,
            'linea': inicio_linea
        }

    def parse_expresion(self):
        """Expresión: lógica O (||)"""
        return self.parse_expresion_logica()

    def parse_expresion_logica(self):
        """Expresión lógica: AND (&&)"""
        izquierda = self.parse_expresion_comparacion()
        if not izquierda:
            return None

        while self.current_token[1] in [RES_Y, RES_O]:
            operador = self.current_token[1]
            self.next_token()
            derecha = self.parse_expresion_comparacion()
            if not derecha:
                return self.error_sintaxis("Se esperaba expresión después del operador lógico")
            izquierda = {
                'tipo': 'operacion_logica',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }

        return izquierda

    def parse_expresion_comparacion(self):
        """Expresión de comparación: ==, !=, >, <, >=, <="""
        izquierda = self.parse_expresion_aritmetica()
        if not izquierda:
            return None

        operadores_comparacion = [
            LIN_IGUAL, RES_ES, RES_NO_ES,
            COL_MAYOR, COL_MENOR
        ]

        if self.current_token[1] in operadores_comparacion:
            operador = self.current_token[1]
            self.next_token()
            derecha = self.parse_expresion_aritmetica()
            if not derecha:
                return self.error_sintaxis("Se esperaba expresión después del operador de comparación")
            return {
                'tipo': 'comparacion',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }

        return izquierda

    def parse_expresion_aritmetica(self):
        """Expresión aritmética: +, -"""
        izquierda = self.parse_termino()
        if not izquierda:
            return None

        while self.current_token[1] in [COL_MAS, COL_MENOS]:
            operador = self.current_token[1]
            self.next_token()
            derecha = self.parse_termino()
            if not derecha:
                return self.error_sintaxis("Se esperaba término después del operador")
            izquierda = {
                'tipo': 'operacion_aritmetica',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }

        return izquierda

    def parse_termino(self):
        """Término: *, /"""
        izquierda = self.parse_factor()
        if not izquierda:
            return None

        while self.current_token[1] in [LIN_MULTIPLICACION, LIN_DIVISION]:
            operador = self.current_token[1]
            self.next_token()
            derecha = self.parse_factor()
            if not derecha:
                return self.error_sintaxis("Se esperaba factor después del operador")
            izquierda = {
                'tipo': 'operacion_aritmetica',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }

        return izquierda

    def parse_factor(self):
        """Factor: número, cadena, identificador, expresión entre paréntesis"""
        if self.match(LIN_NUMERO):
            return {'tipo': 'numero', 'valor': self.current_token[0]}
        elif self.match(LIN_CADENA):
            return {'tipo': 'cadena', 'valor': self.current_token[0]}
        elif self.match(LIN_IDENTIFICADOR):
            return {'tipo': 'variable', 'nombre': self.current_token[0]}
        elif self.match(LIN_PAREN_ABRE):
            expresion = self.parse_expresion()
            if not expresion:
                return self.error_sintaxis("Se esperaba expresión dentro de paréntesis")
            if not self.match(LIN_PAREN_CIERRA):
                return self.error_sintaxis("Se esperaba ')'")
            return expresion
        elif self.current_token[1] in [RES_VERDAD, RES_FALSO]:
            valor = self.current_token[1] == RES_VERDAD
            self.next_token()
            return {'tipo': 'booleano', 'valor': valor}
        else:
            return self.error_sintaxis("Se esperaba número, cadena, identificador o expresión entre paréntesis")

# --- INTÉRPRETE ---
class InterpreterAvellana:
    def __init__(self, ast, compilador):
        self.ast = ast
        self.vars = {}  # Variables globales
        self.clases = {}  # Definiciones de clases
        self.output = []
        self.compilador = compilador  # Referencia al compilador para mostrar salida

    def run(self):
        """Ejecuta el programa completo"""
        try:
            for nodo in self.ast:
                self.ejecutar_nodo(nodo)
            return self.output
        except Exception as e:
            self.compilador.log(f"Error durante ejecución: {str(e)}")
            return self.output

    def ejecutar_nodo(self, nodo):
        """Ejecuta un nodo del AST"""
        if not isinstance(nodo, dict):
            return None

        tipo = nodo.get('tipo')
        
        if tipo == 'declaracion':
            self.ejecutar_declaracion(nodo)
        elif tipo == 'asignacion':
            self.ejecutar_asignacion(nodo)
        elif tipo == 'llamada_imprimir':
            self.ejecutar_imprimir(nodo)
        elif tipo == 'llamada_leer':
            return self.ejecutar_leer(nodo)
        elif tipo == 'si':
            self.ejecutar_si(nodo)
        elif tipo == 'mientras':
            self.ejecutar_mientras(nodo)
        elif tipo == 'retorna':
            return self.evaluar_expresion(nodo['valor'])
        else:
            # Para otros tipos de nodos, solo evaluar si son expresiones
            return self.evaluar_expresion(nodo)

    def ejecutar_declaracion(self, nodo):
        """Ejecuta una declaración de variables"""
        for ident in nodo['identificadores']:
            self.vars[ident] = None  # Inicializar variable
            
        # Procesar asignaciones si las hay
        for asignacion in nodo['asignaciones']:
            variable = asignacion['variable']
            valor = self.evaluar_expresion(asignacion['valor'])
            self.vars[variable] = valor

    def ejecutar_asignacion(self, nodo):
        """Ejecuta una asignación de variable"""
        variable = nodo['variable']
        valor = self.evaluar_expresion(nodo['valor'])
        self.vars[variable] = valor
        return valor

    def ejecutar_imprimir(self, nodo):
        """Ejecuta la función imprimir"""
        textos = []
        for arg in nodo['argumentos']:
            valor = self.evaluar_expresion(arg)
            textos.append(str(valor))
        
        mensaje = " ".join(textos)
        self.output.append(mensaje)
        self.compilador.log(f"Salida: {mensaje}")
        return mensaje

    def ejecutar_leer(self, nodo):
        """Ejecuta la función leer"""
        mensaje = ""
        if nodo['mensaje']:
            mensaje = str(self.evaluar_expresion(nodo['mensaje']))
            self.compilador.log(f"Prompt: {mensaje}")
        
        # Usar un diálogo simple para entrada
        entrada = simpledialog.askstring("Entrada Avellana", mensaje)
        if entrada is None:
            entrada = ""
            
        self.compilador.log(f"Entrada: {entrada}")
        return entrada

    def ejecutar_si(self, nodo):
        """Ejecuta una estructura si"""
        condicion = self.evaluar_expresion(nodo['condicion'])
        
        if condicion:
            for stmt in nodo['cuerpo_si']:
                self.ejecutar_nodo(stmt)
        else:
            # Verificar o_si
            ejecutado = False
            for o_si in nodo['o_sis']:
                if self.evaluar_expresion(o_si['condicion']):
                    for stmt in o_si['cuerpo']:
                        self.ejecutar_nodo(stmt)
                    ejecutado = True
                    break
            
            # Si no se ejecutó ningún o_si, ejecutar si_no
            if not ejecutado and nodo['cuerpo_si_no']:
                for stmt in nodo['cuerpo_si_no']:
                    self.ejecutar_nodo(stmt)

    def ejecutar_mientras(self, nodo):
        """Ejecuta un bucle mientras"""
        while self.evaluar_expresion(nodo['condicion']):
            for stmt in nodo['cuerpo']:
                self.ejecutar_nodo(stmt)

    def evaluar_expresion(self, expr):
        """Evalúa una expresión y retorna su valor"""
        if not isinstance(expr, dict):
            return expr

        tipo = expr.get('tipo')
        
        if tipo == 'numero':
            try:
                return float(expr['valor']) if '.' in expr['valor'] else int(expr['valor'])
            except ValueError:
                return 0
        elif tipo == 'cadena':
            return expr['valor'].strip('"\'')
        elif tipo == 'booleano':
            return expr['valor']
        elif tipo == 'variable':
            return self.vars.get(expr['nombre'])
        elif tipo == 'operacion_aritmetica':
            izquierda = self.evaluar_expresion(expr['izquierda'])
            derecha = self.evaluar_expresion(expr['derecha'])
            
            if expr['operador'] == COL_MAS:
                return izquierda + derecha
            elif expr['operador'] == COL_MENOS:
                return izquierda - derecha
            elif expr['operador'] == LIN_MULTIPLICACION:
                return izquierda * derecha
            elif expr['operador'] == LIN_DIVISION:
                return izquierda / derecha if derecha != 0 else 0
        elif tipo == 'comparacion':
            izquierda = self.evaluar_expresion(expr['izquierda'])
            derecha = self.evaluar_expresion(expr['derecha'])
            
            if expr['operador'] in [LIN_IGUAL, RES_ES]:
                return izquierda == derecha
            elif expr['operador'] == RES_NO_ES:
                return izquierda != derecha
            elif expr['operador'] == COL_MAYOR:
                return izquierda > derecha
            elif expr['operador'] == COL_MENOR:
                return izquierda < derecha
        elif tipo == 'operacion_logica':
            izquierda = self.evaluar_expresion(expr['izquierda'])
            derecha = self.evaluar_expresion(expr['derecha'])
            
            if expr['operador'] == RES_Y:
                return izquierda and derecha
            elif expr['operador'] == RES_O:
                return izquierda or derecha
        
        return None

# --- COMPILADOR v3 ---
class CompiladorAvellanaV3:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Avellana v3")
        self.root.geometry("900x700")
        self.color_bg = "#FFFFFF"
        self.color_editor = "#F39CFF"
        self.color_consola = "#000000"
        self.color_acento = "#B602CE"
        self.color_texto_consola = "#FF9900"
        self.editor_font = font.Font(family="Consolas", size=16)
        self.main_frame = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.main_frame.pack(fill="both", expand=True)
        self.notebook = ttk.Notebook(self.main_frame)
        self.main_frame.add(self.notebook, weight=4)
        self.console = tk.Text(self.main_frame, height=10, 
                               bg=self.color_consola, 
                               fg=self.color_texto_consola,
                               insertbackground=self.color_acento, 
                               wrap="word")
        self.console.config(state="disabled")
        self.main_frame.add(self.console, weight=1)
        self.archivos = {}
        self.crear_menu()
        self.nuevo_archivo()

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir...", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar como...", command=self.guardar_como)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="Cortar", command=lambda: self.editor_actual().event_generate("<<Cut>>"))
        edicion_menu.add_command(label="Copiar", command=lambda: self.editor_actual().event_generate("<<Copy>>"))
        edicion_menu.add_command(label="Pegar", command=lambda: self.editor_actual().event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edicion", menu=edicion_menu)
        consola_menu = tk.Menu(menubar, tearoff=0)
        consola_menu.add_command(label="Limpiar consola", command=self.limpiar_consola)
        menubar.add_cascade(label="Consola", menu=consola_menu)
        fases_menu = tk.Menu(menubar, tearoff=0)
        fases_menu.add_command(label="Lexico", command=self.examen_lexico)
        fases_menu.add_command(label="Sintaxis", command=self.examen_sintaxis)
        fases_menu.add_command(label="Ejecutar", command=self.ejecutar)
        menubar.add_cascade(label="Fases", menu=fases_menu)

    def editor_actual(self):
        tab = self.notebook.select()
        return self.notebook.nametowidget(tab)

    def nuevo_archivo(self):
        text_area = tk.Text(self.notebook, wrap="word", undo=True, 
                           font=self.editor_font,
                           bg=self.color_editor,
                           insertbackground=self.color_acento)
        self.notebook.add(text_area, text="Sin titulo")
        self.notebook.select(text_area)
        self.archivos[text_area] = None
        self.log("Nuevo archivo creado.")

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), 
                      ("Archivos Avellana", "*.avl"),
                      ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                contenido = file.read()
            text_area = tk.Text(self.notebook, wrap="word", undo=True, 
                               font=self.editor_font,
                               bg=self.color_editor,
                               insertbackground=self.color_acento)
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
            filetypes=[("Archivos de texto", "*.txt"),
                      ("Archivos Avellana", "*.avl"), 
                      ("Todos los archivos", "*.*")]
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
        self.log("\n\nInicia Lexico")
        text_area = self.editor_actual()
        lex = LexicoAvellana(text_area.get("1.0", tk.END))
        error, token, mensaje = lex.generaLexico()
        if error == ERR_NOERROR:
            lst = lex.get()
            for c in lst:
                s = str(c[1]) + "-" + lex.getTipoTokenStr(c[1], c[0])
                self.log(c[0] + " \t\t\t\t\t:: " + s)
        else:
            self.log(f"ERROR: {error} :: {token}")
            if mensaje:
                self.log(f"Mensaje: {mensaje}")
        self.log("Total de lineas procesadas: " + str(lex.getLineas()))

    def examen_sintaxis(self):
        self.log("\n\nInicia Sintaxis")
        text_area = self.editor_actual()
        lex = LexicoAvellana(text_area.get("1.0", tk.END))
        error, token, mensaje = lex.generaLexico()
        if error == ERR_NOERROR:
            tokens = lex.get()
            parser = ParserAvellana(tokens)
            if parser.parse():
                self.log("Análisis sintáctico exitoso. El código es válido.")
            else:
                self.log(f"Error de sintaxis en línea {parser.error}: {parser.mensaje}")
        else:
            self.log(f"ERROR: {error} :: {token}")
            if mensaje:
                self.log(f"Mensaje: {mensaje}")
        self.log("Total de lineas procesadas: " + str(lex.getLineas()))

    def ejecutar(self):
        self.log("\n\nEjecución del programa")
        text_area = self.editor_actual()
        lex = LexicoAvellana(text_area.get("1.0", tk.END))
        error, token, mensaje = lex.generaLexico()
        if error == ERR_NOERROR:
            tokens = lex.get()
            parser = ParserAvellana(tokens)
            if parser.parse():
                interpreter = InterpreterAvellana(parser.ast, self)
                output = interpreter.run()
                self.log("\n".join(output))
            else:
                self.log(f"Error de sintaxis en línea {parser.error}: {parser.mensaje}")
        else:
            self.log(f"ERROR: {error} :: {token}")
            if mensaje:
                self.log(f"Mensaje: {mensaje}")
        self.log("Total de lineas procesadas: " + str(lex.getLineas()))

if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorAvellanaV3(root)
    root.mainloop()
# aqui termina