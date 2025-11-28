"""
Módulo de Análisis Sintáctico
"""

from lexico import Lexico, Tipos


class Errores:
    
    SINTAXIS_NINGUNO = 0
    SINTAXIS_IDENTIFICADOR = 1
    SINTAXIS_EOLN = 2
    SINTAXIS_CLASE = 3
    SINTAXIS_FIN_CLASE = 4
    SINTAXIS_FIN_FUNCION = 5
    SINTAXIS_PARENTESIS_ABRIR = 6
    SINTAXIS_PARENTESIS_CERRAR = 7
    SINTAXIS_OPERADOR_LOGICO = 8
    SINTAXIS_FIN_MIENTRAS = 9
    SINTAXIS_CONDICION = 10
    SINTAXIS_FIN_SI = 11
    SINTAXIS_FIN_PARA = 12
    SINTAXIS_LLAVE_ABRIR = 13
    SINTAXIS_LLAVE_CERRAR = 14
    SINTAXIS_HASTA = 18
    
    SEMANTICA_NINGUNO = 0
    SEMANTICA_IDENTIFICADOR_DUPLICADO = 101
    SEMANTICA_IDENTIFICADOR_NO_DECLARADO = 102
    SEMANTICA_FUNCION_NO_DECLARADA = 103
    SEMANTICA_IDENTIFICADOR_NO_ENTERO = 104
    SEMANTICA_IDENTIFICADOR_MAL_USO = 105
    SEMANTICA_TIPO_INCOMPATIBLE = 106


class ErrorSintactico(Exception):
    
    def __init__(self, codigo_error, mensaje, linea, columna=None, token=None):
        self.codigo_error = codigo_error
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        self.token = token
        super().__init__(f"Línea {linea}: {mensaje}")

class TablaSimbolos:
    
    def __init__(self):
        self.simbolos = []
        self.ambito_actual = "global"
        
    def insertar(self, nombre, tipo, linea, tipo_retorno=None, tamanio=None, ambito=None):
        ambito = ambito or self.ambito_actual
        
        for simbolo in self.simbolos:
            if simbolo['nombre'] == nombre and simbolo['ambito'] == ambito:
                return Errores.SEMANTICA_IDENTIFICADOR_DUPLICADO
        
        nuevo_simbolo = {
            'nombre': nombre,
            'tipo': tipo,
            'linea': linea,
            'ambito': ambito,
            'tipo_retorno': tipo_retorno,
            'tamanio': tamanio
        }
        
        self.simbolos.append(nuevo_simbolo)
        return Errores.SEMANTICA_NINGUNO
    
    def buscar(self, nombre, ambito=None):
        if ambito:
            for simbolo in self.simbolos:
                if simbolo['nombre'] == nombre and simbolo['ambito'] == ambito:
                    return simbolo
        else:
            for simbolo in self.simbolos:
                if simbolo['nombre'] == nombre and (simbolo['ambito'] == self.ambito_actual or simbolo['ambito'] == 'global'):
                    return simbolo
        
        return None
    
    def existe(self, nombre, ambito=None):
        return self.buscar(nombre, ambito) is not None
    
    def cambiar_ambito(self, nuevo_ambito):
        self.ambito_actual = nuevo_ambito
    
    def obtener_por_ambito(self, ambito):
        return [simbolo for simbolo in self.simbolos if simbolo['ambito'] == ambito]
    
    def limpiar_ambito(self, ambito):
        self.simbolos = [simbolo for simbolo in self.simbolos if simbolo['ambito'] != ambito]

class ManejadorErrores:
    
    def __init__(self):
        self.errores_sintacticos = []
        self.errores_semanticos = []
    
    def agregar_error_sintactico(self, codigo_error, mensaje, linea, token=None):
        error = {
            'tipo': 'sintactico',
            'codigo': codigo_error,
            'mensaje': mensaje,
            'linea': linea,
            'token': token
        }
        self.errores_sintacticos.append(error)
    
    def agregar_error_semantico(self, codigo_error, mensaje, linea, simbolo=None):
        error = {
            'tipo': 'semantico',
            'codigo': codigo_error,
            'mensaje': mensaje,
            'linea': linea,
            'simbolo': simbolo
        }
        self.errores_semanticos.append(error)
    
    def hay_errores_sintacticos(self):
        return len(self.errores_sintacticos) > 0
    
    def hay_errores_semanticos(self):
        return len(self.errores_semanticos) > 0
    
    def hay_errores(self):
        return self.hay_errores_sintacticos() or self.hay_errores_semanticos()
    
    def obtener_errores(self):
        todos_errores = self.errores_sintacticos + self.errores_semanticos
        return sorted(todos_errores, key=lambda e: e['linea'])
    
    def limpiar(self):
        self.errores_sintacticos.clear()
        self.errores_semanticos.clear()

class SistemaTipos:
    
    def __init__(self, tabla_simbolos, manejador_errores):
        self.tabla_simbolos = tabla_simbolos
        self.manejador_errores = manejador_errores
        
        self.compatibilidad_operadores = {
            '+': self._compatibilidad_suma,
            '-': self._compatibilidad_resta,
            '*': self._compatibilidad_multiplicacion,
            '/': self._compatibilidad_division,
            '==': self._compatibilidad_comparacion,
            '<>': self._compatibilidad_comparacion,
            '>': self._compatibilidad_comparacion,
            '<': self._compatibilidad_comparacion,
            '>=': self._compatibilidad_comparacion,
            '<=': self._compatibilidad_comparacion,
            '&&': self._compatibilidad_and,
            '||': self._compatibilidad_or,
        }
        
        self.conversiones_asignacion = {
            (Tipos.ENTERO, Tipos.ENTERO): True,
            (Tipos.ENTERO, Tipos.FLOTANTE): True,
            (Tipos.FLOTANTE, Tipos.FLOTANTE): True,
            (Tipos.FLOTANTE, Tipos.ENTERO): True,
            (Tipos.CADENA, Tipos.CADENA): True,
            (Tipos.BOOLEANO, Tipos.BOOLEANO): True,
        }
    
    def verificar_asignacion(self, variable, tipo_destino, expresion, linea):
        tipo_expresion = self.analizar_tipo_expresion(expresion, linea)
        
        if tipo_expresion == Tipos.ERROR:
            return False
        
        combinacion = (tipo_destino, tipo_expresion)
        
        if combinacion in self.conversiones_asignacion:
            if self.conversiones_asignacion[combinacion]:
                return True
            else:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                    f"No se puede asignar {self._tipo_a_texto(tipo_expresion)} a '{variable}' de tipo {self._tipo_a_texto(tipo_destino)}",
                    linea
                )
                return False
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Asignación inválida: {self._tipo_a_texto(tipo_destino)} <- {self._tipo_a_texto(tipo_expresion)}",
                linea
            )
            return False
    
    def analizar_tipo_expresion(self, expresion, linea):
        if not isinstance(expresion, dict):
            return Tipos.ERROR
            
        tipo_nodo = expresion.get('tipo', 'desconocido')
        
        if tipo_nodo == 'literal':
            return expresion.get('tipo_dato', Tipos.ERROR)
            
        elif tipo_nodo == 'variable':
            nombre_var = expresion.get('nombre')
            simbolo = self.tabla_simbolos.buscar(nombre_var)
            
            if not simbolo:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO,
                    f"Variable '{nombre_var}' no declarada",
                    linea
                )
                return Tipos.ERROR
                
            return Tipos.convertir_reservado_a_base(simbolo['tipo'])
            
        elif tipo_nodo == 'binaria':
            tipo_izq = self.analizar_tipo_expresion(expresion.get('izquierda'), linea)
            tipo_der = self.analizar_tipo_expresion(expresion.get('derecha'), linea)
            operador = expresion.get('operador')
            
            if tipo_izq == Tipos.ERROR or tipo_der == Tipos.ERROR:
                return Tipos.ERROR
                
            if operador in self.compatibilidad_operadores:
                if operador in ['&&', '||']:
                    tipo_resultado = self.compatibilidad_operadores[operador](tipo_izq, tipo_der, linea)
                else:
                    tipo_resultado = self.compatibilidad_operadores[operador](tipo_izq, tipo_der, linea)
                return tipo_resultado
            else:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                    f"Operador '{operador}' no soportado",
                    linea
                )
                return Tipos.ERROR
                
        elif tipo_nodo == 'unaria':
            operador = expresion.get('operador')
            expresion_interna = expresion.get('expresion')
            tipo_interno = self.analizar_tipo_expresion(expresion_interna, linea)
            
            if tipo_interno == Tipos.ERROR:
                return Tipos.ERROR
                
            if operador == '!':
                return self._compatibilidad_not(tipo_interno, linea)
            else:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                    f"Operador unario '{operador}' no soportado",
                    linea
                )
                return Tipos.ERROR
                
        elif tipo_nodo == 'acceso_arreglo':
            nombre_arreglo = expresion.get('nombre')
            simbolo = self.tabla_simbolos.buscar(nombre_arreglo)
            
            if not simbolo or simbolo['tipo'] != Tipos.LEX_ARREGLO:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO,
                    f"Arreglo '{nombre_arreglo}' no declarado",
                    linea
                )
                return Tipos.ERROR
                
            tipo_indice = self.analizar_tipo_expresion(expresion.get('indice'), linea)
            if tipo_indice != Tipos.ENTERO:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                    "Índice de arreglo debe ser entero",
                    linea
                )
                return Tipos.ERROR
                
            return self._obtener_tipo_elemento_arreglo(simbolo.get('tipo_retorno'))
            
        else:
            return Tipos.ERROR
    
    def _compatibilidad_suma(self, tipo_izq, tipo_der, linea):
        if tipo_izq == Tipos.CADENA or tipo_der == Tipos.CADENA:
            return Tipos.CADENA
        elif Tipos.es_tipo_numerico(tipo_izq) and Tipos.es_tipo_numerico(tipo_der):
            return Tipos.FLOTANTE if Tipos.FLOTANTE in [tipo_izq, tipo_der] else Tipos.ENTERO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '+' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_resta(self, tipo_izq, tipo_der, linea):
        if Tipos.es_tipo_numerico(tipo_izq) and Tipos.es_tipo_numerico(tipo_der):
            return Tipos.FLOTANTE if Tipos.FLOTANTE in [tipo_izq, tipo_der] else Tipos.ENTERO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '-' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_multiplicacion(self, tipo_izq, tipo_der, linea):
        if Tipos.es_tipo_numerico(tipo_izq) and Tipos.es_tipo_numerico(tipo_der):
            return Tipos.FLOTANTE if Tipos.FLOTANTE in [tipo_izq, tipo_der] else Tipos.ENTERO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '*' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_division(self, tipo_izq, tipo_der, linea):
        if Tipos.es_tipo_numerico(tipo_izq) and Tipos.es_tipo_numerico(tipo_der):
            return Tipos.FLOTANTE
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '/' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_comparacion(self, tipo_izq, tipo_der, linea):
        if Tipos.es_tipo_numerico(tipo_izq) and Tipos.es_tipo_numerico(tipo_der):
            return Tipos.BOOLEANO
        elif tipo_izq == tipo_der and tipo_izq in [Tipos.CADENA, Tipos.BOOLEANO]:
            return Tipos.BOOLEANO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Comparación no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_and(self, tipo_izq, tipo_der, linea):
        if tipo_izq == Tipos.BOOLEANO and tipo_der == Tipos.BOOLEANO:
            return Tipos.BOOLEANO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '&&' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_or(self, tipo_izq, tipo_der, linea):
        if tipo_izq == Tipos.BOOLEANO and tipo_der == Tipos.BOOLEANO:
            return Tipos.BOOLEANO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '||' no válida entre {self._tipo_a_texto(tipo_izq)} y {self._tipo_a_texto(tipo_der)}",
                linea
            )
            return Tipos.ERROR
    
    def _compatibilidad_not(self, tipo_exp, linea):
        if tipo_exp == Tipos.BOOLEANO:
            return Tipos.BOOLEANO
        else:
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_TIPO_INCOMPATIBLE,
                f"Operación '!' no válida para {self._tipo_a_texto(tipo_exp)}",
                linea
            )
            return Tipos.ERROR
    
    def _obtener_tipo_elemento_arreglo(self, tipo_arreglo):
        conversiones = {
            Tipos.ARREGLO_ENTERO: Tipos.ENTERO,
            Tipos.ARREGLO_FLOTANTE: Tipos.FLOTANTE,
            Tipos.ARREGLO_CADENA: Tipos.CADENA,
            Tipos.ARREGLO_BOOLEANO: Tipos.BOOLEANO,
        }
        return conversiones.get(tipo_arreglo, Tipos.ERROR)
    
    def _tipo_a_texto(self, tipo):
        conversiones = {
            Tipos.ENTERO: "entero",
            Tipos.FLOTANTE: "flotante",
            Tipos.CADENA: "cadena",
            Tipos.BOOLEANO: "booleano",
            Tipos.VOID: "void",
            Tipos.ERROR: "error",
        }
        return conversiones.get(tipo, "desconocido")


class Sintaxis:
    
    def __init__(self, lexico):
        self.lexico = lexico
        self.lista_tokens = lexico.get()
        self.indice_token = 0
        self.token_actual = ("", Tipos.LIN_SINTIPO)
        
        self.tabla_simbolos = TablaSimbolos()
        self.manejador_errores = ManejadorErrores()
        self.sistema_tipos = SistemaTipos(self.tabla_simbolos, self.manejador_errores)
        
        self.clase_actual = ""
        self.funcion_actual = None
        self.arbol_sintactico = {
            'tipo': 'programa',
            'instrucciones': [],
            'tabla_simbolos': []
        }
    
    
    def analizar(self):
        self.manejador_errores.limpiar()
        self._siguiente_token()
        
        try:
            error = self._procesar_programa_principal()
            
            if error == Errores.SINTAXIS_CLASE:
                self.indice_token = 0
                self.token_actual = ("", Tipos.LIN_SINTIPO)
                self._siguiente_token()
                error = self._procesar_programa_simple()
            
            return error
            
        except ErrorSintactico as e:
            self.manejador_errores.agregar_error_sintactico(
                e.codigo_error, e.mensaje, e.linea, e.token
            )
            return e.codigo_error
    
    def _procesar_programa_principal(self):
        error = Errores.SINTAXIS_NINGUNO
        
        while error == Errores.SINTAXIS_NINGUNO and self.token_actual[1] != Tipos.LIN_EOF:
            tipo_token = self.token_actual[1]
            
            if tipo_token in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                error = self._procesar_declaracion_variable()
            elif tipo_token == Tipos.LEX_ARREGLO:
                error = self._procesar_declaracion_arreglo()  # NUEVO
            elif tipo_token == Tipos.LEX_IMPRIMIR:
                error = self._procesar_instruccion_imprimir()
            elif tipo_token == Tipos.LEX_LEER:
                error = self._procesar_instruccion_leer()
            elif tipo_token == Tipos.LEX_SI:
                error = self._procesar_estructura_si()
            elif tipo_token == Tipos.LEX_MIENTRAS:
                error = self._procesar_estructura_mientras()
            elif tipo_token == Tipos.LEX_PARA:
                error = self._procesar_estructura_para()
            elif tipo_token == Tipos.LEX_FUNCION:  
                error = self._procesar_definicion_funcion()
            elif tipo_token == Tipos.LEX_RETORNAR: 
                error = self._procesar_retornar()
            elif tipo_token == Tipos.LEX_LLAMAR:   
                error = self._procesar_llamada_funcion_simple()
            elif tipo_token == Tipos.LIN_IDENTIFICADOR:
                error = self._procesar_identificador()
            elif tipo_token == Tipos.LIN_EOLN:
                self._siguiente_token()
            else:
                break
        
        return error
    
    def _procesar_programa_simple(self):
        error = Errores.SINTAXIS_NINGUNO
        
        while error == Errores.SINTAXIS_NINGUNO and self.token_actual[1] != Tipos.LIN_EOF:
            tipo_token = self.token_actual[1]
            
            if tipo_token == Tipos.LEX_IMPRIMIR:
                error = self._procesar_instruccion_imprimir()
            elif tipo_token == Tipos.LEX_LEER:
                error = self._procesar_instruccion_leer()
            elif tipo_token in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                error = self._procesar_declaracion_variable()
            elif tipo_token == Tipos.LIN_EOLN:
                self._siguiente_token()
            else:
                break
        
        return error
    
    
    def _procesar_declaracion_variable(self):
        linea_actual = self.lexico.get_lineas()
        tipo_dato = self.token_actual[1]
        self._siguiente_token()
        
        if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            nombre_variable = self.token_actual[0]
            self._siguiente_token()
            
            error_semantico = self.tabla_simbolos.insertar(
                nombre_variable, tipo_dato, linea_actual
            )
            
            if error_semantico != Errores.SEMANTICA_NINGUNO:
                self.manejador_errores.agregar_error_semantico(
                    error_semantico,
                    f"Identificador '{nombre_variable}' ya declarado",
                    linea_actual
                )
            
            declaracion = self._agregar_instruccion_arbol('declaracion',
                variable=nombre_variable,
                tipo_dato=tipo_dato
            )
            
            if self.token_actual[0] == '=':
                self._siguiente_token()
                expresion = self._procesar_expresion()
                declaracion['valor'] = expresion
                
                if expresion:
                    self.sistema_tipos.verificar_asignacion(
                        nombre_variable, tipo_dato, expresion, linea_actual
                    )
            
            if self.token_actual[1] == Tipos.LIN_EOLN:
                self._siguiente_token()
                return Errores.SINTAXIS_NINGUNO
            else:
                return Errores.SINTAXIS_EOLN
        else:
            return Errores.SINTAXIS_IDENTIFICADOR
    
    def _procesar_instruccion_imprimir(self):
        self._siguiente_token()
        
        if self.token_actual[0] == "(":
            self._siguiente_token()
            
            # Procesar la expresión completa (puede ser simple o compleja con accesos a arreglos)
            expresion = self._procesar_expresion()
            
            self._agregar_instruccion_arbol('imprimir', expresion=expresion)
            
            if self.token_actual[0] == ")":
                self._siguiente_token()
                
                if self.token_actual[1] == Tipos.LIN_EOLN:
                    self._siguiente_token()
                    return Errores.SINTAXIS_NINGUNO
                else:
                    return Errores.SINTAXIS_EOLN
            else:
                return Errores.SINTAXIS_PARENTESIS_CERRAR
        else:
            return Errores.SINTAXIS_PARENTESIS_ABRIR
    
    def _procesar_instruccion_leer(self):
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()
        
        if self.token_actual[0] == "(":
            self._siguiente_token()
            
            # Verificar si es un acceso a arreglo
            if (self.token_actual[1] == Tipos.LIN_IDENTIFICADOR and 
                self.indice_token < len(self.lista_tokens) - 1 and
                self.lista_tokens[self.indice_token][0] == '['):
                
                # Es un acceso a arreglo: leer(arreglo[indice])
                nombre_arreglo = self.token_actual[0]
                self._siguiente_token()  # Consumir nombre del arreglo
                
                # Procesar el acceso al arreglo completo
                acceso_arreglo = self._procesar_acceso_arreglo_para_leer(nombre_arreglo)
                
                if acceso_arreglo:
                    self._agregar_instruccion_arbol('leer_arreglo',
                        arreglo=nombre_arreglo,
                        indice=acceso_arreglo['indice']
                    )
                else:
                    return Errores.SINTAXIS_NINGUNO
                    
            elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                # Es una variable simple
                nombre_variable = self.token_actual[0]
                
                if not self.tabla_simbolos.existe(nombre_variable):
                    self.tabla_simbolos.insertar(
                        nombre_variable, Tipos.LEX_ENTERO, linea_actual
                    )
                
                self._siguiente_token()
                self._agregar_instruccion_arbol('leer', variable=nombre_variable)
            else:
                return Errores.SINTAXIS_IDENTIFICADOR
            
            if self.token_actual[0] == ")":
                self._siguiente_token()
                
                if self.token_actual[1] == Tipos.LIN_EOLN:
                    self._siguiente_token()
                    return Errores.SINTAXIS_NINGUNO
                else:
                    return Errores.SINTAXIS_EOLN
            else:
                return Errores.SINTAXIS_PARENTESIS_CERRAR
        else:
            return Errores.SINTAXIS_PARENTESIS_ABRIR

    def _procesar_acceso_arreglo_para_leer(self, nombre_arreglo):
        """Procesa acceso a arreglo específicamente para instrucción LEER"""
        if self.token_actual[0] == '[':
            self._siguiente_token()  # Consumir '['
            
            indice = self._procesar_expresion()
            
            if self.token_actual[0] == ']':
                self._siguiente_token()  # Consumir ']'
                
                # Verificar que es un arreglo
                simbolo = self.tabla_simbolos.buscar(nombre_arreglo)
                if not simbolo or simbolo['tipo'] != Tipos.LEX_ARREGLO:
                    self.manejador_errores.agregar_error_semantico(
                        Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO,
                        f"Arreglo '{nombre_arreglo}' no declarado",
                        self.lexico.get_lineas()
                    )
                    return None
                
                return {
                    'nombre': nombre_arreglo,
                    'indice': indice
                }
        
        return None
    
    def _procesar_identificador(self):
        nombre = self.token_actual[0]
        
        if not self.tabla_simbolos.existe(nombre):
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO,
                f"Identificador '{nombre}' no declarado",
                self.lexico.get_lineas()
            )
        
        self._siguiente_token()
        
        if self.token_actual[0] == "=":
            return self._procesar_asignacion(nombre)
        elif self.token_actual[0] == "[":
            return self._procesar_acceso_arreglo(nombre)
        elif self.token_actual[0] == "(":
            return self._procesar_llamada_funcion(nombre)
        else:
            return Errores.SINTAXIS_NINGUNO
    
    def _procesar_asignacion(self, nombre_variable):
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()
        
        simbolo = self.tabla_simbolos.buscar(nombre_variable)
        if not simbolo:
            return Errores.SINTAXIS_NINGUNO
        
        tipo_variable = simbolo['tipo']
        
        expresion = self._procesar_expresion()
        
        if expresion:
            self.sistema_tipos.verificar_asignacion(
                nombre_variable, tipo_variable, expresion, linea_actual
            )
        
        self._agregar_instruccion_arbol('asignacion',
            variable=nombre_variable,
            expresion=expresion
        )
        
        return Errores.SINTAXIS_NINGUNO
    
    def _procesar_retornar(self):
        """Procesa instrucción retornar"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'retornar'
        
        expresion = None
        if self.token_actual[1] != Tipos.LIN_EOLN:
            expresion = self._procesar_expresion()
        
        # Verificar que estamos dentro de una función
        if self.tabla_simbolos.ambito_actual == "global":
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_IDENTIFICADOR_MAL_USO,
                "retornar solo puede usarse dentro de una función",
                linea_actual
            )
        
        self._agregar_instruccion_arbol('retornar', expresion=expresion)
        
        if self.token_actual[1] == Tipos.LIN_EOLN:
            self._siguiente_token()
            return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_EOLN
    
    def _procesar_expresion(self):
        return self._procesar_expresion_logica()
    
    def _procesar_expresion_logica(self):
        izquierda = self._procesar_expresion_and()
        
        while self.token_actual[0] == '||':
            operador = self.token_actual[0]
            self._siguiente_token()
            derecha = self._procesar_expresion_and()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda
    
    def _procesar_expresion_and(self):
        izquierda = self._procesar_expresion_comparacion()
        
        while self.token_actual[0] == '&&':
            operador = self.token_actual[0]
            self._siguiente_token()
            derecha = self._procesar_expresion_comparacion()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda
    
    def _procesar_expresion_comparacion(self):
        izquierda = self._procesar_expresion_suma()
        
        while self.token_actual[0] in ('==', '<>', '>', '<', '>=', '<='):
            operador = self.token_actual[0]
            self._siguiente_token()
            derecha = self._procesar_expresion_suma()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda
    
    def _procesar_expresion_suma(self):
        izquierda = self._procesar_expresion_termino()
        
        while self.token_actual[0] in ('+', '-'):
            operador = self.token_actual[0]
            self._siguiente_token()
            derecha = self._procesar_expresion_termino()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda
    
    def _procesar_expresion_termino(self):
        izquierda = self._procesar_expresion_factor()
        
        while self.token_actual[0] in ('*', '/'):
            operador = self.token_actual[0]
            self._siguiente_token()
            derecha = self._procesar_expresion_factor()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda
    
    def _procesar_expresion_factor(self):
        if self.token_actual[0] == '!':
            self._siguiente_token()
            expresion = self._procesar_expresion_factor()
            return {
                'tipo': 'unaria',
                'operador': '!',
                'expresion': expresion
            }
            
        elif self.token_actual[1] in [Tipos.LIN_NUM_ENTERO, Tipos.LIN_NUM_FLOTANTE]:
            expresion = {
                'tipo': 'literal',
                'valor': self.token_actual[0],
                'tipo_dato': Tipos.ENTERO if self.token_actual[1] == Tipos.LIN_NUM_ENTERO else Tipos.FLOTANTE
            }
            self._siguiente_token()
            return expresion
            
        elif self.token_actual[1] == Tipos.LIN_CADENA:
            expresion = {
                'tipo': 'literal',
                'valor': self.token_actual[0],
                'tipo_dato': Tipos.CADENA
            }
            self._siguiente_token()
            return expresion
        
        elif self.token_actual[1] == Tipos.LEX_VERDADERO:
            expresion = {
                'tipo': 'literal',
                'valor': True,
                'tipo_dato': Tipos.BOOLEANO
            }
            self._siguiente_token()
            return expresion
            
        elif self.token_actual[1] == Tipos.LEX_FALSO:
            expresion = {
                'tipo': 'literal',
                'valor': False,
                'tipo_dato': Tipos.BOOLEANO
            }
            self._siguiente_token()
            return expresion
            
        elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            nombre = self.token_actual[0]
            
            # Verificar si es un acceso a arreglo
            if (self.indice_token < len(self.lista_tokens) and 
                self.lista_tokens[self.indice_token][0] == '['):
                
                # Es un acceso a arreglo
                self._siguiente_token()  # Consumir el nombre
                return self._procesar_acceso_arreglo_en_expresion(nombre)
            else:
                # Es una variable simple
                expresion = {
                    'tipo': 'variable',
                    'nombre': nombre
                }
                self._siguiente_token()
                return expresion
                
        elif self.token_actual[0] == '(':
            self._siguiente_token()
            expresion = self._procesar_expresion()
            if self.token_actual[0] == ')':
                self._siguiente_token()
                return expresion
            else:
                return {'tipo': 'error', 'mensaje': 'Paréntesis no cerrado'}
        
        else:
            return {
                'tipo': 'literal', 
                'valor': '0',
                'tipo_dato': Tipos.ENTERO
            }

    def _procesar_acceso_arreglo_en_expresion(self, nombre_arreglo):
        """Procesa acceso a arreglo dentro de una expresión"""
        if self.token_actual[0] == '[':
            self._siguiente_token()  # Consumir '['
            
            indice = self._procesar_expresion()
            
            if self.token_actual[0] == ']':
                self._siguiente_token()  # Consumir ']'
                
                return {
                    'tipo': 'acceso_arreglo',
                    'nombre': nombre_arreglo,
                    'indice': indice
                }
        
        return {'tipo': 'error', 'mensaje': 'Acceso a arreglo mal formado'}
    
    def _procesar_lista_argumentos(self):
        """Procesa lista de argumentos en llamada a función"""
        argumentos = []
        
        while self.token_actual[1] != Tipos.LIN_EOF:
            expresion = self._procesar_expresion()
            if expresion:
                argumentos.append(expresion)
            
            if self.token_actual[0] == ',':
                self._siguiente_token()
            else:
                break
        
        return argumentos

    def _procesar_instruccion_retornar(self):
        """Procesa instrucción retornar"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'retornar'
        
        expresion = None
        if self.token_actual[1] != Tipos.LIN_EOLN:
            expresion = self._procesar_expresion()
        
        # Verificar que estamos dentro de una función
        if self.tabla_simbolos.ambito_actual == "global":
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_IDENTIFICADOR_MAL_USO,
                "retornar solo puede usarse dentro de una función",
                linea_actual
            )
        
        self._agregar_instruccion_arbol('retornar', expresion=expresion)
        
        if self.token_actual[1] == Tipos.LIN_EOLN:
            self._siguiente_token()
            return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_EOLN
    
    def _siguiente_token(self):
        if self.indice_token < len(self.lista_tokens):
            self.token_actual = self.lista_tokens[self.indice_token]
            
            if self.token_actual[1] == Tipos.LIN_EOLN:
                indice_aux = self.indice_token + 1
                while (indice_aux < len(self.lista_tokens) and 
                       self.lista_tokens[indice_aux][1] == Tipos.LIN_EOLN):
                    indice_aux += 1
                self.indice_token = indice_aux
            else:
                self.indice_token += 1
        else:
            self.token_actual = ("", Tipos.LIN_EOF)
    
    def _agregar_instruccion_arbol(self, tipo, **atributos):
        instruccion = {'tipo': tipo, **atributos}
        self.arbol_sintactico['instrucciones'].append(instruccion)
        return instruccion
    
    def _agregar_simbolo_arbol(self, nombre, tipo, valor=None):
        simbolo = {'nombre': nombre, 'tipo': tipo, 'valor': valor}
        self.arbol_sintactico['tabla_simbolos'].append(simbolo)
    
    def genera_sintaxis(self):
        return self.analizar()
    
    def get_lista_identificadores(self):
        return [[simbolo['nombre'], simbolo['tipo'], simbolo['linea']] 
                for simbolo in self.tabla_simbolos.simbolos]
    
    def get_tipo_identificador(self, nombre):
        simbolo = self.tabla_simbolos.buscar(nombre)
        return simbolo['tipo'] if simbolo else Tipos.NO_DECLARADO
    
    def get_str_tipo_identificador(self, tipo):
        conversiones = {
            Tipos.LEX_ENTERO: "entero",
            Tipos.LEX_FLOTANTE: "flotante",
            Tipos.LEX_CADENA: "cadena",
            Tipos.LEX_BOOLEANO: "booleano",
            Tipos.LEX_FUNCION: "funcion",
            Tipos.LEX_ARREGLO: "arreglo",
        }
        return conversiones.get(tipo, "desconocido")
    
    def get_arbol_sintactico(self):
        return self.arbol_sintactico
    
    def get_errores_semanticos(self):
        return [f"Línea {e['linea']}: {e['mensaje']}" 
                for e in self.manejador_errores.errores_semanticos]
    
    def get_tabla_simbolos(self):
        return self.tabla_simbolos.simbolos
    
    def mensaje_error(self, codigo_error):
        mensajes = {
            Errores.SINTAXIS_NINGUNO: "no se encontraron errores de sintaxis",
            Errores.SINTAXIS_IDENTIFICADOR: "error de sintaxis: se esperaba un identificador",
            Errores.SINTAXIS_EOLN: "error de sintaxis: se esperaba un eoln",
            Errores.SINTAXIS_CLASE: "error de sintaxis: se esperaba [clase]",
            Errores.SINTAXIS_FIN_CLASE: "error de sintaxis: se esperaba [fin_clase]",
            Errores.SINTAXIS_FIN_FUNCION: "error de sintaxis: se esperaba [fin_funcion]",
            Errores.SINTAXIS_PARENTESIS_ABRIR: "error de sintaxis: se esperaba (",
            Errores.SINTAXIS_PARENTESIS_CERRAR: "error de sintaxis: se esperaba )",
            Errores.SINTAXIS_OPERADOR_LOGICO: "error de sintaxis: se esperaba operador lógico",
            Errores.SINTAXIS_FIN_MIENTRAS: "error de sintaxis: se esperaba [fin_mientras]",
            Errores.SINTAXIS_CONDICION: "error de sintaxis: error en la condición",
            Errores.SINTAXIS_FIN_SI: "error de sintaxis: se esperaba [fin_si]",
            Errores.SINTAXIS_FIN_PARA: "error de sintaxis: se esperaba [fin_para]",
            Errores.SINTAXIS_HASTA: "error de sintaxis: se esperaba [hasta]",
            
            Errores.SEMANTICA_IDENTIFICADOR_DUPLICADO: "error de semántica: identificador ya declarado",
            Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO: "error de semántica: identificador no declarado",
            Errores.SEMANTICA_FUNCION_NO_DECLARADA: "error de semántica: función no declarado o mal uso de identificador",
            Errores.SEMANTICA_IDENTIFICADOR_NO_ENTERO: "error de semántica: identificador debe ser entero",
            Errores.SEMANTICA_IDENTIFICADOR_MAL_USO: "error de semántica: identificador no declarado o mal uso de función",
            Errores.SEMANTICA_TIPO_INCOMPATIBLE: "error de semántica: tipos no coinciden en la operación",
        }
        return mensajes.get(codigo_error, "error desconocido")
    
    def _procesar_declaracion_arreglo(self):
        """Procesa declaración de arreglos: arreglo entero numeros[10]"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'arreglo'
        
        # Tipo de elementos del arreglo
        if self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
            tipo_elemento = self.token_actual[1]
            self._siguiente_token()
        else:
            return Errores.SINTAXIS_IDENTIFICADOR
        
        # Nombre del arreglo
        if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            nombre_arreglo = self.token_actual[0]
            self._siguiente_token()
        else:
            return Errores.SINTAXIS_IDENTIFICADOR
        
        # Tamaño del arreglo entre corchetes
        if self.token_actual[0] == '[':
            self._siguiente_token()
            
            if self.token_actual[1] in [Tipos.LIN_NUM_ENTERO, Tipos.LIN_NUM_FLOTANTE]:
                tamanio = int(self.token_actual[0])
                self._siguiente_token()
            else:
                return Errores.SINTAXIS_NINGUNO
            
            if self.token_actual[0] == ']':
                self._siguiente_token()
            else:
                return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_NINGUNO
        
        # Insertar en tabla de símbolos
        tipo_arreglo = self._obtener_tipo_arreglo(tipo_elemento)
        error_semantico = self.tabla_simbolos.insertar(
            nombre_arreglo, Tipos.LEX_ARREGLO, linea_actual,
            tipo_retorno=tipo_arreglo, tamanio=tamanio
        )
        
        if error_semantico != Errores.SEMANTICA_NINGUNO:
            self.manejador_errores.agregar_error_semantico(
                error_semantico,
                f"Arreglo '{nombre_arreglo}' ya declarado",
                linea_actual
            )
        
        # Agregar al árbol sintáctico
        self._agregar_instruccion_arbol('declaracion_arreglo',
            nombre=nombre_arreglo,
            tipo_elemento=tipo_elemento,
            tamanio=tamanio
        )
        
        if self.token_actual[1] == Tipos.LIN_EOLN:
            self._siguiente_token()
        
        return Errores.SINTAXIS_NINGUNO

    def _obtener_tipo_arreglo(self, tipo_elemento):
        """Convierte tipo de elemento a tipo de arreglo"""
        conversiones = {
            Tipos.LEX_ENTERO: Tipos.ARREGLO_ENTERO,
            Tipos.LEX_FLOTANTE: Tipos.ARREGLO_FLOTANTE,
            Tipos.LEX_CADENA: Tipos.ARREGLO_CADENA,
            Tipos.LEX_BOOLEANO: Tipos.ARREGLO_BOOLEANO,
        }
        return conversiones.get(tipo_elemento, Tipos.ERROR)

    def _procesar_acceso_arreglo(self, nombre):
        """Procesa acceso a arreglo: numeros[5] o numeros[i]"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir '['
        
        indice = self._procesar_expresion()
        
        if self.token_actual[0] == ']':
            self._siguiente_token()
            
            # Verificar que es un arreglo
            simbolo = self.tabla_simbolos.buscar(nombre)
            if not simbolo or simbolo['tipo'] != Tipos.LEX_ARREGLO:
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO,
                    f"Arreglo '{nombre}' no declarado",
                    linea_actual
                )
            
            # Crear nodo de acceso
            acceso = {
                'tipo': 'acceso_arreglo',
                'nombre': nombre,
                'indice': indice
            }
            
            # Si sigue '=', es asignación a arreglo
            if self.token_actual[0] == '=':
                self._siguiente_token()
                valor = self._procesar_expresion()
                
                self._agregar_instruccion_arbol('asignacion_arreglo',
                    nombre=nombre,
                    indice=indice,
                    valor=valor
                )
                
                if self.token_actual[1] == Tipos.LIN_EOLN:
                    self._siguiente_token()
            else:
                # Es solo acceso (en una expresión)
                return acceso
            
        return Errores.SINTAXIS_NINGUNO

    def _procesar_lista_parametros(self):
        """Procesa lista de parámetros: (entero x, cadena nombre)"""
        parametros = []
        
        while self.token_actual[1] != Tipos.LIN_EOF:
            if self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE,
                                    Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                tipo_param = self.token_actual[1]
                self._siguiente_token()
                
                if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                    nombre_param = self.token_actual[0]
                    self._siguiente_token()
                    
                    parametros.append({
                        'nombre': nombre_param,
                        'tipo': tipo_param
                    })
                    
                    # Verificar si hay más parámetros
                    if self.token_actual[0] == ',':
                        self._siguiente_token()
                    else:
                        break
                else:
                    break
            else:
                break
        
        return parametros

    def _procesar_estructura_para(self):
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'para'
        
        if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            variable = self.token_actual[0]
            self._siguiente_token()
        else:
            return Errores.SINTAXIS_IDENTIFICADOR
        
        if self.token_actual[0] == '=':
            self._siguiente_token()
            inicio = self._procesar_expresion()
        else:
            return Errores.SINTAXIS_OPERADOR_LOGICO
        
        if self.token_actual[1] == Tipos.LEX_HASTA:  
            self._siguiente_token()
            fin = self._procesar_expresion()
        else:
            return Errores.SINTAXIS_OPERADOR_LOGICO
        
        # Crear nodo PARA con cuerpo vacío
        nodo_para = {
            'tipo': 'para',
            'variable': variable,
            'inicio': inicio,
            'condicion': {
                'tipo': 'binaria',
                'operador': '<=',
                'izquierda': {'tipo': 'variable', 'nombre': variable},
                'derecha': fin
            },
            'cuerpo': []
        }
        
        # Procesar cuerpo del bucle
        while (self.token_actual[1] != Tipos.LEX_FIN_PARA and
            self.token_actual[1] != Tipos.LIN_EOF):
            
            if self.token_actual[1] == Tipos.LEX_IMPRIMIR:
                error = self._procesar_instruccion_imprimir()
                if error == Errores.SINTAXIS_NINGUNO:
                    # Agregar la instrucción al cuerpo del PARA
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_para['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LEX_LEER:
                error = self._procesar_instruccion_leer()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_para['cuerpo'].append(instruccion)
            elif self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                error = self._procesar_declaracion_variable()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_para['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                error = self._procesar_identificador()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_para['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_EOLN:
                self._siguiente_token()
            else:
                break
        
        # Agregar el nodo PARA completo al árbol
        self.arbol_sintactico['instrucciones'].append(nodo_para)
        
        if self.token_actual[1] == Tipos.LEX_FIN_PARA:
            self._siguiente_token()
            return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_FIN_PARA
        
    def _procesar_estructura_si(self):
        """Procesa estructura SI - SI ENTONCES - SINO - FIN_SI"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'si'
        
        # Procesar condición
        condicion = self._procesar_expresion()
        
        # Verificar 'entonces' (opcional en nuestro lenguaje)
        if self.token_actual[0].lower() == 'entonces':
            self._siguiente_token()
        
        # Crear nodo SI con cuerpo vacío
        nodo_si = {
            'tipo': 'si',
            'condicion': condicion,
            'cuerpo': [],
            'sino': []
        }
        
        # Procesar cuerpo del SI (instrucciones cuando condición es verdadera)
        while (self.token_actual[1] not in [Tipos.LEX_SINO, Tipos.LEX_FIN_SI] and
               self.token_actual[1] != Tipos.LIN_EOF):
            
            if self.token_actual[1] == Tipos.LEX_IMPRIMIR:
                error = self._procesar_instruccion_imprimir()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_si['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LEX_LEER:
                error = self._procesar_instruccion_leer()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_si['cuerpo'].append(instruccion)
            elif self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                        Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                error = self._procesar_declaracion_variable()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_si['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                error = self._procesar_identificador()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_si['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_EOLN:
                self._siguiente_token()
            else:
                break
        
        # Procesar bloque SINO si existe
        if self.token_actual[1] == Tipos.LEX_SINO:
            self._siguiente_token()  # Consumir 'sino'
            
            # Procesar cuerpo del SINO (instrucciones cuando condición es falsa)
            while (self.token_actual[1] != Tipos.LEX_FIN_SI and
                   self.token_actual[1] != Tipos.LIN_EOF):
                
                if self.token_actual[1] == Tipos.LEX_IMPRIMIR:
                    error = self._procesar_instruccion_imprimir()
                    if error == Errores.SINTAXIS_NINGUNO:
                        if self.arbol_sintactico['instrucciones']:
                            instruccion = self.arbol_sintactico['instrucciones'].pop()
                            nodo_si['sino'].append(instruccion)
                elif self.token_actual[1] == Tipos.LEX_LEER:
                    error = self._procesar_instruccion_leer()
                    if error == Errores.SINTAXIS_NINGUNO:
                        if self.arbol_sintactico['instrucciones']:
                            instruccion = self.arbol_sintactico['instrucciones'].pop()
                            nodo_si['sino'].append(instruccion)
                elif self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                            Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                    error = self._procesar_declaracion_variable()
                    if error == Errores.SINTAXIS_NINGUNO:
                        if self.arbol_sintactico['instrucciones']:
                            instruccion = self.arbol_sintactico['instrucciones'].pop()
                            nodo_si['sino'].append(instruccion)
                elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                    error = self._procesar_identificador()
                    if error == Errores.SINTAXIS_NINGUNO:
                        if self.arbol_sintactico['instrucciones']:
                            instruccion = self.arbol_sintactico['instrucciones'].pop()
                            nodo_si['sino'].append(instruccion)
                elif self.token_actual[1] == Tipos.LIN_EOLN:
                    self._siguiente_token()
                else:
                    break
        
        # Agregar el nodo SI completo al árbol
        self.arbol_sintactico['instrucciones'].append(nodo_si)
        
        if self.token_actual[1] == Tipos.LEX_FIN_SI:
            self._siguiente_token()
            return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_FIN_SI
        
    def _procesar_estructura_mientras(self):
        """Procesa estructura MIENTRAS - FIN_MIENTRAS"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'mientras'
        
        # Procesar condición
        condicion = self._procesar_expresion()
        
        # Crear nodo MIENTRAS con cuerpo vacío
        nodo_mientras = {
            'tipo': 'mientras',
            'condicion': condicion,
            'cuerpo': []
        }
        
        # Procesar cuerpo del bucle
        while (self.token_actual[1] != Tipos.LEX_FIN_MIENTRAS and
               self.token_actual[1] != Tipos.LIN_EOF):
            
            if self.token_actual[1] == Tipos.LEX_IMPRIMIR:
                error = self._procesar_instruccion_imprimir()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_mientras['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LEX_LEER:
                error = self._procesar_instruccion_leer()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_mientras['cuerpo'].append(instruccion)
            elif self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                        Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                error = self._procesar_declaracion_variable()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_mientras['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                error = self._procesar_identificador()
                if error == Errores.SINTAXIS_NINGUNO:
                    if self.arbol_sintactico['instrucciones']:
                        instruccion = self.arbol_sintactico['instrucciones'].pop()
                        nodo_mientras['cuerpo'].append(instruccion)
            elif self.token_actual[1] == Tipos.LIN_EOLN:
                self._siguiente_token()
            else:
                break
        
        # Agregar el nodo MIENTRAS completo al árbol
        self.arbol_sintactico['instrucciones'].append(nodo_mientras)
        
        if self.token_actual[1] == Tipos.LEX_FIN_MIENTRAS:
            self._siguiente_token()
            return Errores.SINTAXIS_NINGUNO
        else:
            return Errores.SINTAXIS_FIN_MIENTRAS
    
    def _procesar_definicion_clase(self):
        return Errores.SINTAXIS_NINGUNO
    
    def _procesar_definicion_funcion(self):
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'funcion'
        
        if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            nombre_funcion = self.token_actual[0]
            
            # Guardar ámbito anterior
            ambito_anterior = self.tabla_simbolos.ambito_actual
            self.tabla_simbolos.cambiar_ambito(nombre_funcion)
            
            self._siguiente_token()  # Consumir nombre
            
            # Procesar parámetros
            parametros = []
            if self.token_actual[0] == '(':
                self._siguiente_token()
                parametros = self._procesar_lista_parametros()
                if self.token_actual[0] == ')':
                    self._siguiente_token()
                else:
                    self.tabla_simbolos.cambiar_ambito(ambito_anterior)
                    return Errores.SINTAXIS_PARENTESIS_CERRAR
            
            # Tipo de retorno
            tipo_retorno = Tipos.LEX_VOID
            if self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                    Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                tipo_retorno = self.token_actual[1]
                self._siguiente_token()
            
            # Insertar función en tabla global
            error_semantico = self.tabla_simbolos.insertar(
                nombre_funcion, Tipos.LEX_FUNCION, linea_actual,
                tipo_retorno=tipo_retorno, ambito='global'
            )
            
            if error_semantico != Errores.SEMANTICA_NINGUNO:
                self.manejador_errores.agregar_error_semantico(
                    error_semantico,
                    f"Función '{nombre_funcion}' ya declarada",
                    linea_actual
                )
            
            # Agregar parámetros a tabla local
            for param in parametros:
                self.tabla_simbolos.insertar(
                    param['nombre'], param['tipo'], linea_actual
                )
            
            nodo_funcion = self._agregar_instruccion_arbol('definicion_funcion',
                nombre=nombre_funcion,
                parametros=parametros,
                tipo_retorno=tipo_retorno,
                cuerpo=[]
            )
            
            # Procesar cuerpo de la función
            cuerpo_funcion = []
            instrucciones_arbol_original = self.arbol_sintactico['instrucciones']
            
            # Cambiar temporalmente el árbol para capturar solo el cuerpo de la función
            self.arbol_sintactico['instrucciones'] = cuerpo_funcion
            
            while (self.token_actual[1] != Tipos.LEX_FIN_FUNCION and
                self.token_actual[1] != Tipos.LIN_EOF):
                
                if self.token_actual[1] == Tipos.LEX_IMPRIMIR:
                    error = self._procesar_instruccion_imprimir()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_LEER:
                    error = self._procesar_instruccion_leer()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] in [Tipos.LEX_ENTERO, Tipos.LEX_FLOTANTE, 
                                            Tipos.LEX_CADENA, Tipos.LEX_BOOLEANO]:
                    error = self._procesar_declaracion_variable()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_ARREGLO:
                    error = self._procesar_declaracion_arreglo()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
                    error = self._procesar_identificador()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_LLAMAR:
                    error = self._procesar_llamada_funcion_simple()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_RETORNAR:
                    error = self._procesar_retornar()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_SI:
                    error = self._procesar_estructura_si()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_MIENTRAS:
                    error = self._procesar_estructura_mientras()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LEX_PARA:
                    error = self._procesar_estructura_para()
                    if error != Errores.SINTAXIS_NINGUNO:
                        break
                elif self.token_actual[1] == Tipos.LIN_EOLN:
                    self._siguiente_token()
                else:
                    # Token inesperado, salir del bucle
                    break
            
            # Restaurar el árbol original y asignar el cuerpo capturado
            self.arbol_sintactico['instrucciones'] = instrucciones_arbol_original
            nodo_funcion['cuerpo'] = cuerpo_funcion
            
            self.tabla_simbolos.cambiar_ambito(ambito_anterior)
            
            if self.token_actual[1] == Tipos.LEX_FIN_FUNCION:
                self._siguiente_token()
                return Errores.SINTAXIS_NINGUNO
            else:
                self.manejador_errores.agregar_error_sintactico(
                    Errores.SINTAXIS_FIN_FUNCION, 
                    f"Se esperaba 'fin_funcion' para la función '{nombre_funcion}'",
                    linea_actual,
                    self.token_actual[0]
                )
                return Errores.SINTAXIS_FIN_FUNCION
        else:
            return Errores.SINTAXIS_IDENTIFICADOR
    
    def _procesar_llamada_funcion(self, nombre_funcion):
        linea_actual = self.lexico.get_lineas()
        
        if not self.tabla_simbolos.existe(nombre_funcion, 'global'):
            self.manejador_errores.agregar_error_semantico(
                Errores.SEMANTICA_FUNCION_NO_DECLARADA,
                f"Función '{nombre_funcion}' no declarada",
                linea_actual
            )
        
        self._siguiente_token()
        
        argumentos = []
        if self.token_actual[0] != ")":
            argumentos = self._procesar_lista_argumentos()
        
        if self.token_actual[0] == ")":
            self._siguiente_token()
            
            return self._agregar_instruccion_arbol('llamada_funcion',
                nombre=nombre_funcion,
                argumentos=argumentos
            )
        else:
            return Errores.SINTAXIS_PARENTESIS_CERRAR
        
    def _procesar_llamada_funcion_simple(self):
        """Procesa llamada a función sin parámetros usando 'llamar'"""
        linea_actual = self.lexico.get_lineas()
        self._siguiente_token()  # Consumir 'llamar'
        
        if self.token_actual[1] == Tipos.LIN_IDENTIFICADOR:
            nombre_funcion = self.token_actual[0]
            
            # Verificar que la función existe
            if not self.tabla_simbolos.existe(nombre_funcion, 'global'):
                self.manejador_errores.agregar_error_semantico(
                    Errores.SEMANTICA_FUNCION_NO_DECLARADA,
                    f"Función '{nombre_funcion}' no declarada",
                    linea_actual
                )
            
            self._siguiente_token()  # Consumir nombre función
            
            # Agregar al árbol sintáctico
            self._agregar_instruccion_arbol('llamada_funcion',
                nombre=nombre_funcion,
                argumentos=[]
            )
            
            if self.token_actual[1] == Tipos.LIN_EOLN:
                self._siguiente_token()
                return Errores.SINTAXIS_NINGUNO
            else:
                return Errores.SINTAXIS_EOLN
        
        return Errores.SINTAXIS_IDENTIFICADOR

ERR_NO_SINTAX_ERROR = Errores.SINTAXIS_NINGUNO
ERR_IDENTIFICADOR = Errores.SINTAXIS_IDENTIFICADOR
ERR_EOLN = Errores.SINTAXIS_EOLN
ERR_CLASE = Errores.SINTAXIS_CLASE
ERR_FIN_CLASE = Errores.SINTAXIS_FIN_CLASE
ERR_FIN_FUNCION = Errores.SINTAXIS_FIN_FUNCION
ERR_PARENTESIS_ABRIR = Errores.SINTAXIS_PARENTESIS_ABRIR
ERR_PARENTESIS_CERRAR = Errores.SINTAXIS_PARENTESIS_CERRAR
ERR_OP_LOGICO = Errores.SINTAXIS_OPERADOR_LOGICO
ERR_FIN_MIENTRAS = Errores.SINTAXIS_FIN_MIENTRAS
ERR_CONDICION = Errores.SINTAXIS_CONDICION
ERR_FIN_SI = Errores.SINTAXIS_FIN_SI
ERR_FIN_PARA = Errores.SINTAXIS_FIN_PARA
ERR_LLAVE_ABRIR = Errores.SINTAXIS_LLAVE_ABRIR
ERR_LLAVE_CERRAR = Errores.SINTAXIS_LLAVE_CERRAR
ERR_HASTA = Errores.SINTAXIS_HASTA

ERR_SEMANTICA_NO_ERROR = Errores.SEMANTICA_NINGUNO
ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE = Errores.SEMANTICA_IDENTIFICADOR_DUPLICADO
ERR_SEMANTICA_IDENTIFICADOR_NO_DECL = Errores.SEMANTICA_IDENTIFICADOR_NO_DECLARADO
ERR_SEMANTICA_FUNCION_NO_DECL = Errores.SEMANTICA_FUNCION_NO_DECLARADA
ERR_SEMANTICA_IDENTIFICADOR_NO_ENTERO = Errores.SEMANTICA_IDENTIFICADOR_NO_ENTERO
ERR_SEMANTICA_IDENT_FUNCION_MAL_USO = Errores.SEMANTICA_IDENTIFICADOR_MAL_USO
ERR_SEMANTICA_TIPO_NO_COINCIDE = Errores.SEMANTICA_TIPO_INCOMPATIBLE