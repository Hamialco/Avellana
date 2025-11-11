"""
sintaxis
"""

from avllexico import *

ERR_NO_SINTAX_ERROR = 0
ERR_IDENTIFICADOR = 1
ERR_EOLN = 2
ERR_CLASE = 3
ERR_FIN_CLASE = 4
ERR_FIN_METODO = 5
ERR_PARENTESIS_ABRIR = 6
ERR_PARENTESIS_CERRAR = 7
ERR_OP_LOGICO = 8
ERR_FIN_MIENTRAS = 9
ERR_CONDICION = 10
ERR_FIN_SI = 11
ERR_FIN_PARA = 12
ERR_LLAVE_ABRIR = 13
ERR_LLAVE_CERRAR = 14

ERR_SEMANTICA_NO_ERROR = 0
ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE = 101
ERR_SEMANTICA_IDENTIFICADOR_NO_DECL = 102
ERR_SEMANTICA_METODO_NO_DECL = 103
ERR_SEMANTICA_IDENTIFICADOR_NO_ENTERO = 104
ERR_SEMANTICA_IDENT_METODO_MAL_USO = 105
ERR_SEMANTICA_TIPO_NO_COINCIDE = 106

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.funciones = {}
        
    def agregar_variable(self, nombre, tipo, valor=None):
        if nombre in self.simbolos:
            return False
        self.simbolos[nombre] = {
            'tipo': tipo,
            'valor': valor,
            'es_funcion': False
        }
        return True
        
    def agregar_funcion(self, nombre, tipo_retorno=None):
        if nombre in self.funciones:
            return False
        self.funciones[nombre] = {
            'tipo_retorno': tipo_retorno,
            'parametros': []
        }
        return True

    def agregar_identificador(self, iden, tipo, linea, tipo_retorno=None):
        for elemento in self.tabla_simbolos:
            if elemento[0] == iden:
                return ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE
        # Guardar tipo de retorno para métodos
        self.tabla_simbolos.append([iden, tipo, linea, tipo_retorno])
        return ERR_SEMANTICA_NO_ERROR
        
    def existe_variable(self, nombre):
        return nombre in self.simbolos
        
    def existe_funcion(self, nombre):
        return nombre in self.funciones
        
    def obtener_tipo_variable(self, nombre):
        if nombre in self.simbolos:
            return self.simbolos[nombre]['tipo']
        return None
        
    def obtener_tipo_funcion(self, nombre):
        if nombre in self.funciones:
            return self.funciones[nombre]['tipo_retorno']
        return None
    
    def obtener_tipo_retorno_metodo(self, iden):
        for elemento in self.tabla_simbolos:
            if elemento[0] == iden and elemento[1] == RES_METODO:
                return elemento[3]  # tipo_retorno
        return None

class Sintaxis:
    def __init__(self, lex):
        self.lexico = lex
        self.lst_tokens = lex.get()
        self.i_token = 0
        self.tok_actual = ("", LIN_SINTIPO)
        self.tabla_simbolos = []
        self.clase_actual = ""
        self.arbol_sintactico = {
            'tipo': 'programa',
            'instrucciones': [],
            'tabla_simbolos': []
        }
        self.contexto_actual = 'global'  # 'global', 'clase', 'metodo'
       
    def genera_sintaxis(self):
        error = self.proc_principal()
        return error
    
    def sig_token(self):
        self.tok_actual = self.lst_tokens[self.i_token]
        if self.tok_actual[1] == LIN_EOLN:
            i_aux = self.i_token + 1
            while self.lst_tokens[i_aux][1] == LIN_EOLN:
                i_aux += 1
            self.i_token = i_aux
        elif self.tok_actual[1] != LIN_EOF:
            self.i_token += 1

    def proc_principal(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()

        while error == ERR_NO_SINTAX_ERROR and not self.tok_actual[1] in (RES_CLASE, LIN_EOF):
            if self.tok_actual[1] in (RES_ENTERO, RES_FLOTANTE, RES_CADENA, RES_BOOLEANO):
                error = self.proc_declaracion_variable()
            elif self.tok_actual[1] == LIN_EOLN:
                self.sig_token()
            else:
                error = ERR_CLASE
        
        if error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] == RES_CLASE:
            error = self.proc_definicion_clase()

        return error
    
    def proc_declaracion_variable(self):
        error = ERR_NO_SINTAX_ERROR
        tipo_dato = self.tok_actual[1]
        linea_actual = self.lexico.get_lineas()
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            ident = self.tok_actual[0]
            self.sig_token()
            
            # Agregar al árbol sintáctico
            declaracion = self._agregar_instruccion_arbol('declaracion', 
                variable=ident, 
                tipo_dato=tipo_dato,
                valor=None
            )
            
            # Si hay asignación,  verificar tipos
            if self.tok_actual[0] == '=':
                self.sig_token()
                expresion = self.proc_def_expresion()
                declaracion['valor'] = expresion

                # VERIFICACIÓN DE TIPOS - NUEVO
                if hasattr(self, 'analizar_tipo_expresion'):
                    error_tipo = self.verificar_tipo_asignacion(ident, expresion, linea_actual)
                    if error_tipo != ERR_SEMANTICA_NO_ERROR:
                        return error_tipo
        
            error = self.agregar_identificador(ident, tipo_dato, linea_actual)
            self._agregar_simbolo_arbol(ident, tipo_dato)
                
            error = self.agregar_identificador(ident, tipo_dato, 0)
            self._agregar_simbolo_arbol(ident, tipo_dato)
            
            if error == ERR_SEMANTICA_NO_ERROR and self.tok_actual[1] == LIN_EOLN:
                self.sig_token()
            else:
                error = ERR_EOLN
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_declaracion_arreglo(self):
        """Procesa declaración de arreglos: arreglo entero nombres[5]"""
        error = ERR_NO_SINTAX_ERROR
        linea_actual = self.lexico.get_lineas()
        
        # Consumir 'arreglo'
        self.sig_token()
        
        # Obtener tipo del arreglo
        if self.tok_actual[1] in (RES_ENTERO, RES_FLOTANTE, RES_CADENA, RES_BOOLEANO):
            tipo_elemento = self.tok_actual[1]
            self.sig_token()
            
            if self.tok_actual[1] == LIN_IDENTIFICADOR:
                nombre_arreglo = self.tok_actual[0]
                self.sig_token()
                
                if self.tok_actual[0] == "[":
                    self.sig_token()
                    
                    # Obtener tamaño del arreglo
                    if self.tok_actual[1] in (LIN_NUM_ENTERO, LIN_NUMERO):
                        tamanio = int(self.tok_actual[0])
                        self.sig_token()
                        
                        if self.tok_actual[0] == "]":
                            self.sig_token()
                            
                            # Agregar a tabla de símbolos
                            tipo_arreglo = self._obtener_tipo_arreglo(tipo_elemento)
                            error = self.agregar_identificador(nombre_arreglo, RES_ARREGLO, linea_actual, tipo_arreglo, tamanio)
                            
                            if error == ERR_SEMANTICA_NO_ERROR:
                                # Agregar al árbol sintáctico
                                declaracion = self._agregar_instruccion_arbol('declaracion_arreglo',
                                    nombre=nombre_arreglo,
                                    tipo_elemento=tipo_elemento,
                                    tamanio=tamanio
                                )
                                
                                if self.tok_actual[1] == LIN_EOLN:
                                    self.sig_token()
                                else:
                                    error = ERR_EOLN
                            else:
                                error = ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE
                        else:
                            error = ERR_PARENTESIS_CERRAR
                    else:
                        error = ERR_IDENTIFICADOR
                else:
                    error = ERR_PARENTESIS_ABRIR
            else:
                error = ERR_IDENTIFICADOR
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_definicion_clase(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            self.clase_actual = self.tok_actual[0]
            self.sig_token()
            
            if self.tok_actual[1] == RES_HEREDA:
                self.sig_token()
                if self.tok_actual[1] == LIN_IDENTIFICADOR:
                    self.sig_token()
            
            if self.tok_actual[1] == LIN_EOLN:
                self.sig_token()
                
                while error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] != RES_FIN_CLASE:
                    if self.tok_actual[1] in (RES_ENTERO, RES_FLOTANTE, RES_CADENA, RES_BOOLEANO):
                        error = self.proc_declaracion_variable()
                    elif self.tok_actual[1] == RES_CONSTRUCTOR:
                        error = self.proc_definicion_constructor()
                    elif self.tok_actual[1] == RES_METODO:
                        error = self.proc_definicion_metodo()
                    elif self.tok_actual[1] == LIN_EOLN:
                        self.sig_token()
                    else:
                        error = ERR_FIN_CLASE
                
                if error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] == RES_FIN_CLASE:
                    self.sig_token()
            else:
                error = ERR_EOLN
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_definicion_constructor(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            ident = self.tok_actual[0]
            self.sig_token()
            
            if self.tok_actual[1] == LIN_EOLN:
                error = self.agregar_identificador(ident, RES_METODO, 0)
                if error == ERR_SEMANTICA_NO_ERROR:
                    self.sig_token()
                    error = self.proc_instrucciones()
                    
                    if error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] == RES_FIN_CONSTRUCTOR:
                        self.sig_token()
                    else:
                        error = ERR_FIN_METODO
            else:
                error = ERR_EOLN
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_definicion_metodo(self):
        error = ERR_NO_SINTAX_ERROR
        tipo_retorno = self.tok_actual[1]  # Guardar tipo de retorno
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            ident = self.tok_actual[0]
            self.metodo_actual = ident  # Guardar método actual para verificación
            self.sig_token()
            
            if self.tok_actual[1] == LIN_EOLN:
                # Agregar con tipo de retorno
                error = self.agregar_identificador(ident, RES_METODO, 0, tipo_retorno)
                if error == ERR_SEMANTICA_NO_ERROR:
                    self.sig_token()
                    error = self.proc_instrucciones()
                    
                    if error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] == RES_FIN_METODO:
                        self.sig_token()
                        self.metodo_actual = None  # Limpiar método actual
                    else:
                        error = ERR_FIN_METODO
            else:
                error = ERR_EOLN
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_definicion_funcion(self):
        """Procesa definición de funciones sin parámetros"""
        error = ERR_NO_SINTAX_ERROR
    
        # Esperar tipo de retorno o 'metodo'
        if self.tok_actual[1] in (RES_ENTERO, RES_FLOTANTE, RES_CADENA, RES_BOOLEANO, RES_VOID, RES_METODO):
            tipo_retorno = self.tok_actual[1]
            self.sig_token()
            
            if self.tok_actual[1] == LIN_IDENTIFICADOR:
                nombre_funcion = self.tok_actual[0]
                
                # Agregar a tabla de símbolos
                error_sem = self.agregar_identificador(nombre_funcion, RES_METODO, 0)
                if error_sem != ERR_SEMANTICA_NO_ERROR:
                    return error_sem
                    
                self.sig_token()
                
                if self.tok_actual[1] == LIN_EOLN:
                    self.sig_token()
                    
                    # Procesar cuerpo de la función
                    error = self.proc_instrucciones()
                    if error != ERR_NO_SINTAX_ERROR:
                        return error
                    
                    # Verificar fin de función
                    if self.tok_actual[1] == RES_FIN_METODO:
                        self.sig_token()
                    else:
                        error = ERR_FIN_METODO
                else:
                    error = ERR_EOLN
            else:
                error = ERR_IDENTIFICADOR
        else:
            error = ERR_IDENTIFICADOR
            
        return error

    def proc_def_llamada_funcion(self):
            """Procesa llamada a función sin parámetros"""
            error = ERR_NO_SINTAX_ERROR
            
            if self.tok_actual[1] == LIN_IDENTIFICADOR:
                nombre_funcion = self.tok_actual[0]
                
                # Verificar que existe como función
                tipo_id = self.get_tipo_identificador(nombre_funcion)
                if tipo_id != RES_METODO:
                    return ERR_SEMANTICA_METODO_NO_DECL
                    
                self.sig_token()
                
                if self.tok_actual[0] == "(":
                    self.sig_token()
                    
                    # Verificar paréntesis de cierre (sin parámetros)
                    if self.tok_actual[0] == ")":
                        self.sig_token()
                    else:
                        error = ERR_PARENTESIS_CERRAR
                else:
                    error = ERR_PARENTESIS_ABRIR
            else:
                error = ERR_IDENTIFICADOR
                
            return error

    def proc_instrucciones(self):
        error = ERR_NO_SINTAX_ERROR

        while error == ERR_NO_SINTAX_ERROR and not self.tok_actual[1] in (RES_FIN_METODO, RES_FIN_CONSTRUCTOR, RES_FIN_CLASE, RES_FIN_SI, RES_FIN_MIENTRAS, RES_FIN_PARA, RES_SINO):
            if self.tok_actual[1] == RES_ARREGLO:
                error = self.proc_declaracion_arreglo()
            elif self.tok_actual[1] == RES_SI:
                error = self.proc_def_si()
            elif self.tok_actual[1] == RES_PARA:
                error = self.proc_def_para()
            elif self.tok_actual[1] == RES_MIENTRAS:
                error = self.proc_def_mientras()
            elif self.tok_actual[1] == RES_IMPRIMIR:
                error = self.proc_def_imprimir()
            elif self.tok_actual[1] == RES_LEER:
                error = self.proc_def_leer()
            elif self.tok_actual[1] == RES_RETORNAR:
                error = self.proc_def_retornar()
            elif self.tok_actual[1] == LIN_IDENTIFICADOR:
                siguiente_token = self.lst_tokens[self.i_token + 1] if self.i_token + 1 < len(self.lst_tokens) else None
                if siguiente_token and siguiente_token[0] == "(":
                    error = self.proc_def_llamada_funcion()
                else:
                    error = self.proc_def_identificador()
            elif self.tok_actual[1] in (RES_ENTERO, RES_FLOTANTE, RES_CADENA, RES_BOOLEANO, RES_METODO):
                error = self.proc_declaracion_variable()

            if error == ERR_NO_SINTAX_ERROR:
                if self.tok_actual[1] == LIN_EOLN:
                    self.sig_token()
                else:
                    if self.tok_actual[1] in (RES_FIN_SI, RES_FIN_MIENTRAS, RES_FIN_PARA, RES_SINO): 
                        break
                    error = ERR_EOLN
                
        return error
    
    def proc_def_si(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()  # Consumir 'si'
    
        # Procesar condición
        error = self.proc_def_condicion()
        if error != ERR_NO_SINTAX_ERROR:
            return error
        
        if self.tok_actual[1] == LIN_EOLN:
            self.sig_token()
            
            # Procesar cuerpo del SI
            error = self.proc_instrucciones()
            if error != ERR_NO_SINTAX_ERROR:
                return error
            
            # Verificar si hay SINO
            if self.tok_actual[1] == RES_SINO:
                self.sig_token()
                if self.tok_actual[1] == LIN_EOLN:
                    self.sig_token()
                    # Procesar cuerpo del SINO
                    error = self.proc_instrucciones()
                    if error != ERR_NO_SINTAX_ERROR:
                        return error
            
            # Verificar FIN_SI
            if self.tok_actual[1] == RES_FIN_SI:
                self.sig_token()
            else:
                error = ERR_FIN_SI
        else:
            error = ERR_EOLN
            
        return error

    def proc_def_mientras(self):
        """Procesa estructura MIENTRAS (while)"""
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()  # Consumir 'mientras'
            
        # Procesar condición
        error = self.proc_def_condicion()
        if error != ERR_NO_SINTAX_ERROR:
            return error
            
        if self.tok_actual[1] == LIN_EOLN:
            self.sig_token()
                
            # Procesar cuerpo del MIENTRAS
            error = self.proc_instrucciones()
            if error != ERR_NO_SINTAX_ERROR:
                return error
                
            # Verificar FIN_MIENTRAS
            if self.tok_actual[1] == RES_FIN_MIENTRAS:
                self.sig_token()
            else:
                error = ERR_FIN_MIENTRAS
        else:
            error = ERR_EOLN
                
        return error

    def proc_def_para(self):
        """Procesa estructura PARA (for)"""
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()  # Consumir 'para'
            
        # Esperar asignación inicial
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            error = self.proc_def_asignacion()
            if error != ERR_NO_SINTAX_ERROR:
                return error
            
        if self.tok_actual[1] == LIN_EOLN:
            self.sig_token()
                
            # Procesar cuerpo del PARA
            error = self.proc_instrucciones()
            if error != ERR_NO_SINTAX_ERROR:
                return error
                
            # Verificar FIN_PARA
            if self.tok_actual[1] == RES_FIN_PARA:
                self.sig_token()
            else:
                error = ERR_FIN_PARA
        else:
            error = ERR_EOLN
                
        return error

    def proc_def_imprimir(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        if self.tok_actual[0] == "(":
            self.sig_token()
            error = self.proc_def_expresion()
            
            if error == ERR_NO_SINTAX_ERROR and self.tok_actual[0] == ")":
                self.sig_token()
            else:
                error = ERR_PARENTESIS_CERRAR
        else:
            error = ERR_PARENTESIS_ABRIR
            
        return error
    
    def proc_def_leer(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        if self.tok_actual[0] == "(":
            self.sig_token()
            if self.tok_actual[1] == LIN_IDENTIFICADOR:
                tipo_id = self.get_tipo_identificador(self.tok_actual[0])
                if tipo_id in (RES_NO_DECL, RES_METODO):
                    return ERR_SEMANTICA_IDENT_METODO_MAL_USO
                
                self.sig_token()
                if self.tok_actual[0] == ")":
                    self.sig_token()
                else:
                    error = ERR_PARENTESIS_CERRAR
            else:
                error = ERR_IDENTIFICADOR
        else:
            error = ERR_PARENTESIS_ABRIR
            
        return error
    
    def proc_def_retornar(self):
        """Procesa instrucción retornar con valor"""
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        # Verificar si hay expresión para retornar
        if self.tok_actual[1] != LIN_EOLN:
            expresion = self.proc_def_expresion()
            
            # Agregar al árbol sintáctico
            instruccion_retorno = self._agregar_instruccion_arbol('retornar', 
                expresion=expresion,
                tipo_retorno=self.analizar_tipo_expresion(expresion) if hasattr(self, 'analizar_tipo_expresion') else TIPO_VOID
            )
            
            # Verificar compatibilidad con tipo de retorno del método
            if hasattr(self, 'metodo_actual') and self.metodo_actual:
                tipo_metodo = self.get_tipo_identificador(self.metodo_actual)
                tipo_expresion = self.analizar_tipo_expresion(expresion)
                
                if not self.son_tipos_compatibles(tipo_metodo, tipo_expresion):
                    self.agregar_error_semantico(
                        f"Tipo de retorno no coincide con el tipo del método {self.metodo_actual}", 
                        self.lexico.get_lineas()
                    )
                    return ERR_SEMANTICA_TIPO_NO_COINCIDE
        else:
            # Retorno sin valor
            self._agregar_instruccion_arbol('retornar', expresion=None, tipo_retorno=TIPO_VOID)
        
        return error

    def son_tipos_compatibles(self, tipo_esperado, tipo_actual):
        """Verifica si los tipos son compatibles para retorno"""
        if tipo_esperado == RES_VOID and tipo_actual == TIPO_VOID:
            return True
        elif tipo_esperado == RES_ENTERO and tipo_actual in [TIPO_ENTERO, TIPO_FLOTANTE]:
            return True
        elif tipo_esperado == RES_FLOTANTE and tipo_actual in [TIPO_ENTERO, TIPO_FLOTANTE]:
            return True
        elif tipo_esperado == RES_CADENA and tipo_actual == TIPO_CADENA:
            return True
        elif tipo_esperado == RES_BOOLEANO and tipo_actual == TIPO_BOOLEANO:
            return True
        return False
    
    def proc_def_condicion(self):
        error = ERR_NO_SINTAX_ERROR
        linea_actual = self.lexico.get_lineas()
        
        # Analizar primera expresión
        expr1 = self.proc_def_expresion()
        tipo1 = self.analizar_tipo_expresion(expr1)
        
        if error == ERR_NO_SINTAX_ERROR:
            if self.tok_actual[0] in ("==", ">=", "<=", "<>", ">", "<"):
                operador = self.tok_actual[0]
                self.sig_token()
                
                # Analizar segunda expresión
                expr2 = self.proc_def_expresion()
                tipo2 = self.analizar_tipo_expresion(expr2)
                
                # Verificar compatibilidad en comparación
                tipo_resultado = self.verificar_compatibilidad_tipos(tipo1, tipo2, operador, linea_actual)
                if tipo_resultado == TIPO_ERROR:
                    return ERR_SEMANTICA_TIPO_NO_COINCIDE
                    
                # Las condiciones deben ser booleanas
                if tipo_resultado != TIPO_BOOLEANO:
                    self.agregar_error_semantico(
                        f"La condición debe ser booleana, no {self.tipo_a_texto(tipo_resultado)}", 
                        linea_actual
                    )
                    return ERR_SEMANTICA_TIPO_NO_COINCIDE
            else:
                # Condición simple (solo expresión)
                if tipo1 != TIPO_BOOLEANO:
                    self.agregar_error_semantico(
                        f"La condición debe ser booleana, no {self.tipo_a_texto(tipo1)}", 
                        linea_actual
                    )
                    return ERR_SEMANTICA_TIPO_NO_COINCIDE
                    
        return error
    
    def proc_def_asignacion(self):
        error = ERR_NO_SINTAX_ERROR
        linea_actual = self.lexico.get_lineas()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            variable = self.tok_actual[0]
            tipo_variable = self.get_tipo_identificador(variable)
            
            if tipo_variable == RES_NO_DECL:
                self.agregar_error_semantico(f"Variable '{variable}' no declarada", linea_actual)
                return ERR_SEMANTICA_IDENTIFICADOR_NO_DECL
                
            self.sig_token()
            if self.tok_actual[0] == "=":
                self.sig_token()
                
                # Analizar la expresión del lado derecho
                expresion = self.proc_def_expresion()
                tipo_expresion = self.analizar_tipo_expresion(expresion)
                
                # Verificar compatibilidad de tipos en la asignación
                error_tipo = self.verificar_tipo_asignacion(variable, tipo_variable, tipo_expresion, linea_actual)
                if error_tipo != ERR_SEMANTICA_NO_ERROR:
                    return error_tipo
                    
        return error
    
    def proc_def_identificador(self):
        error = ERR_NO_SINTAX_ERROR
        nombre = self.tok_actual[0]
        tipo_id = self.get_tipo_identificador(nombre)
        
        if tipo_id == RES_NO_DECL:
            return ERR_SEMANTICA_IDENTIFICADOR_NO_DECL
        
        self.sig_token()
        
        # Verificar si es acceso a arreglo
        if self.tok_actual[0] == "[":
            error = self.proc_def_acceso_arreglo(nombre)
        elif self.tok_actual[0] == "=":
            error = self.proc_def_asignacion()
        elif self.tok_actual[0] == "(":
            error = self.proc_def_llamada_metodo()
        elif tipo_id == RES_METODO:
            error = ERR_SEMANTICA_METODO_NO_DECL
            
        return error
    
    def proc_def_llamada_metodo(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        
        if self.tok_actual[0] == ")":
            self.sig_token()
        else:
            error = self.proc_def_expresion()
            while error == ERR_NO_SINTAX_ERROR and self.tok_actual[0] == ",":
                self.sig_token()
                error = self.proc_def_expresion()
                
            if error == ERR_NO_SINTAX_ERROR and self.tok_actual[0] == ")":
                self.sig_token()
            else:
                error = ERR_PARENTESIS_CERRAR
                
        return error
    
    def proc_def_expresion(self):
        error = ERR_NO_SINTAX_ERROR

        while True:
            if self.tok_actual[1] in (LIN_CADENA, LIN_NUMERO, LIN_NUM_ENTERO, LIN_NUM_FLOTANTE, LIN_IDENTIFICADOR, RES_VERDADERO, RES_FALSO):
                if self.tok_actual[1] == LIN_IDENTIFICADOR:
                    tipo_id = self.get_tipo_identificador(self.tok_actual[0])
                    if tipo_id == RES_NO_DECL:
                        return ERR_SEMANTICA_IDENTIFICADOR_NO_DECL

                self.sig_token()
                if self.tok_actual[0] in ("+", "-", "/", "*"):
                    self.sig_token()
                else:
                    if not self.tok_actual[0] in (")", ",", "==", ">=", "<=", "<>", ">", "<") and self.tok_actual[1] != LIN_EOLN:
                        error = ERR_PARENTESIS_CERRAR
                    break
            elif self.tok_actual[0] == "(":
                self.sig_token()
                error = self.proc_def_expresion()

                if error != ERR_NO_SINTAX_ERROR:
                    break

                if self.tok_actual[0] == ")":
                    self.sig_token()
                    if self.tok_actual[0] in ("+", "-", "/", "*"):
                        self.sig_token()
                    else:
                        break
            else:
                error = ERR_IDENTIFICADOR
                break
       
        return self.proc_def_termino()

    def proc_def_termino(self):
        izquierda = self.proc_def_factor()
        
        while self.tok_actual[0] in ('+', '-'):
            operador = self.tok_actual[0]
            self.sig_token()
            derecha = self.proc_def_factor()
            
            izquierda = {
                'tipo': 'binaria',
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda

    def proc_def_factor(self):
        izquierda = self.proc_def_primario()
        
        while self.tok_actual[0] in ('*', '/'):
            operador = self.tok_actual[0]
            self.sig_token()
            derecha = self.proc_def_primario()
            
            izquierda = {
                'tipo': 'binaria', 
                'operador': operador,
                'izquierda': izquierda,
                'derecha': derecha
            }
        
        return izquierda

    def proc_def_primario(self):
        if self.tok_actual[1] in (LIN_NUM_ENTERO, LIN_NUM_FLOTANTE):
            # Literal numérico
            expresion = {
                'tipo': 'literal',
                'valor': self.tok_actual[0],
                'tipo_dato': TIPO_ENTERO if self.tok_actual[1] == LIN_NUM_ENTERO else TIPO_FLOTANTE
            }
            self.sig_token()
            return expresion
            
        elif self.tok_actual[1] == LIN_CADENA:
            # Literal cadena
            expresion = {
                'tipo': 'literal',
                'valor': self.tok_actual[0],
                'tipo_dato': TIPO_CADENA
            }
            self.sig_token()
            return expresion
            
        elif self.tok_actual[1] == LIN_IDENTIFICADOR:
            # Variable
            expresion = {
                'tipo': 'variable',
                'nombre': self.tok_actual[0]
            }
            self.sig_token()
            return expresion
            
        elif self.tok_actual[0] == '(':
            self.sig_token()
            expresion = self.proc_def_expresion()
            if self.tok_actual[0] == ')':
                self.sig_token()
                return expresion
            else:
                return {'tipo': 'error', 'mensaje': 'Paréntesis no cerrado'}
        
        else:
            return {'tipo': 'error', 'mensaje': 'Expresión inválida'}
    
    def mensaje_error(self, err):
        s = ""
        if err == ERR_NO_SINTAX_ERROR:
            s = "no se encontraron errores de sintaxis"
        elif err == ERR_IDENTIFICADOR:
            s = "error de sintaxis: se esperaba un identificador"
        elif err == ERR_EOLN:
            s = "error de sintaxis: se esperaba un eoln"
        elif err == ERR_CLASE:
            s = "error de sintaxis: se esperaba [clase]"
        elif err == ERR_FIN_CLASE:
            s = "error de sintaxis: se esperaba [fin_clase]"
        elif err == ERR_FIN_METODO:
            s = "error de sintaxis: se esperaba [fin_metodo]"
        elif err == ERR_PARENTESIS_ABRIR:
            s = "error de sintaxis: se esperaba ("
        elif err == ERR_PARENTESIS_CERRAR:
            s = "error de sintaxis: se esperaba )"
        elif err == ERR_OP_LOGICO:
            s = "error de sintaxis: se esperaba operador lógico"
        elif err == ERR_FIN_MIENTRAS:
            s = "error de sintaxis: se esperaba [fin_mientras]"
        elif err == ERR_CONDICION:
            s = "error de sintaxis: error en la condición"
        elif err == ERR_FIN_SI:
            s = "error de sintaxis: se esperaba [fin_si]"
        elif err == ERR_FIN_PARA:
            s = "error de sintaxis: se esperaba [fin_para]"

        elif err == ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE:
            s = "error de semántica: identificador ya declarado"
        elif err == ERR_SEMANTICA_IDENTIFICADOR_NO_DECL:
            s = "error de semántica: identificador no declarado"
        elif err == ERR_SEMANTICA_METODO_NO_DECL:
            s = "error de semántica: método no declarado o mal uso de identificador"
        elif err == ERR_SEMANTICA_IDENTIFICADOR_NO_ENTERO:
            s = "error de semántica: identificador debe ser entero"
        elif err == ERR_SEMANTICA_IDENT_METODO_MAL_USO:
            s = "error de semántica: identificador no declarado o mal uso de método"
        elif err == ERR_SEMANTICA_TIPO_NO_COINCIDE:
            s = "error de semántica: tipos no coinciden en la operación"

        return s
    
    def agregar_identificador(self, iden, tipo, linea):
        for elemento in self.tabla_simbolos:
            if elemento[0] == iden:
                return ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE
        self.tabla_simbolos.append([iden, tipo, linea])
        return ERR_SEMANTICA_NO_ERROR

    def get_lista_identificadores(self):
        return self.tabla_simbolos
    
    def get_tipo_identificador(self, iden):
        for elemento in self.tabla_simbolos:
            if elemento[0] == iden:
                return elemento[1]
        return RES_NO_DECL

    def get_str_tipo_identificador(self, tipo):
        s = ""
        if tipo == RES_ENTERO:
            s = "entero"
        elif tipo == RES_FLOTANTE:
            s = "flotante"
        elif tipo == RES_CADENA:
            s = "cadena"
        elif tipo == RES_BOOLEANO:
            s = "booleano"
        elif tipo == RES_METODO:
            s = "metodo"

        return s

    def get_arbol_sintactico(self):
        """Retorna el árbol sintáctico generado (para byte-code)"""
        # Esto sería una implementación simplificada
        return {
            'tipo': 'programa',
            'instrucciones': self._construir_arbol()
        }

    def get_errores_semanticos(self):
        """Retorna la lista de errores semánticos encontrados"""
        return getattr(self, 'errores_semanticos', [])
    
    def _construir_arbol(self):
        """Construye el árbol sintáctico a partir de los tokens"""
        # Implementación simplificada para demostración
        arbol = []
        # Lógica para construir el árbol
        return arbol
    
    def _agregar_instruccion_arbol(self, tipo, **kwargs):
        """Agrega una instrucción al árbol sintáctico"""
        instruccion = {'tipo': tipo, **kwargs}
        self.arbol_sintactico['instrucciones'].append(instruccion)
        return instruccion

    def _agregar_simbolo_arbol(self, nombre, tipo, valor=None):
        """Agrega un símbolo a la tabla del árbol"""
        simbolo = {'nombre': nombre, 'tipo': tipo, 'valor': valor}
        self.arbol_sintactico['tabla_simbolos'].append(simbolo)

    def verificar_tipos_expresion(self, expresion):
        """Verifica la coherencia de tipos en una expresión"""
        if expresion['tipo'] == 'literal':
            return expresion['tipo_dato']
        elif expresion['tipo'] == 'variable':
            tipo_var = self.get_tipo_identificador(expresion['nombre'])
            return tipo_var
        elif expresion['tipo'] == 'binaria':
            tipo_izq = self.verificar_tipos_expresion(expresion['izquierda'])
            tipo_der = self.verificar_tipos_expresion(expresion['derecha'])
            
            # Verificar compatibilidad de tipos
            if tipo_izq != tipo_der and not (tipo_izq in [RES_ENTERO, RES_FLOTANTE] and tipo_der in [RES_ENTERO, RES_FLOTANTE]):
                return ERR_SEMANTICA_TIPO_NO_COINCIDE
                
            return tipo_izq  # Tipo resultante
        
        return RES_NO_DECL
    
    def verificar_compatibilidad_tipos(self, tipo1, tipo2, operador, linea):
        """Verifica si dos tipos son compatibles para una operación"""
        
        # Convertir tipos reservados a base
        tipo1_base = self.convertir_tipo_reservado_a_base(tipo1)
        tipo2_base = self.convertir_tipo_reservado_a_base(tipo2)
        
        # Tabla de compatibilidad de tipos extendida
        compatibilidad = {
            # Operaciones aritméticas
            '+': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_ENTERO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_FLOTANTE,
                (TIPO_CADENA, TIPO_CADENA): TIPO_CADENA,
                (TIPO_CADENA, TIPO_ENTERO): TIPO_CADENA,  # concatenación
                (TIPO_CADENA, TIPO_FLOTANTE): TIPO_CADENA, # concatenación
                (TIPO_ENTERO, TIPO_CADENA): TIPO_CADENA,   # concatenación
                (TIPO_FLOTANTE, TIPO_CADENA): TIPO_CADENA, # concatenación
                (TIPO_CADENA, TIPO_BOOLEANO): TIPO_CADENA, # concatenación
                (TIPO_BOOLEANO, TIPO_CADENA): TIPO_CADENA, # concatenación
            },
            '-': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_ENTERO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_FLOTANTE,
            },
            '*': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_ENTERO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_FLOTANTE,
            },
            '/': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_FLOTANTE,  # división puede dar decimal
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_FLOTANTE,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_FLOTANTE,
            },
            # Operaciones de comparación (siempre retornan booleano)
            '==': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_CADENA, TIPO_CADENA): TIPO_BOOLEANO,
                (TIPO_BOOLEANO, TIPO_BOOLEANO): TIPO_BOOLEANO,
            },
            '<>': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_CADENA, TIPO_CADENA): TIPO_BOOLEANO,
                (TIPO_BOOLEANO, TIPO_BOOLEANO): TIPO_BOOLEANO,
            },
            '>': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
            },
            '<': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
            },
            '>=': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
            },
            '<=': {
                (TIPO_ENTERO, TIPO_ENTERO): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_ENTERO, TIPO_FLOTANTE): TIPO_BOOLEANO,
                (TIPO_FLOTANTE, TIPO_ENTERO): TIPO_BOOLEANO,
            },
            # Operaciones lógicas
            '&&': {
                (TIPO_BOOLEANO, TIPO_BOOLEANO): TIPO_BOOLEANO,
            },
            '||': {
                (TIPO_BOOLEANO, TIPO_BOOLEANO): TIPO_BOOLEANO,
            }
        }
        
        # Buscar en la tabla de compatibilidad
        if operador in compatibilidad:
            combinacion = (tipo1_base, tipo2_base)
            if combinacion in compatibilidad[operador]:
                return compatibilidad[operador][combinacion]
            
            # Verificar compatibilidad numérica genérica
            if operador in ['+', '-', '*', '/']:
                if self.es_tipo_numerico(tipo1) and self.es_tipo_numerico(tipo2):
                    # Para operaciones numéricas, promover al tipo más general
                    if TIPO_FLOTANTE in [tipo1_base, tipo2_base]:
                        return TIPO_FLOTANTE
                    else:
                        return TIPO_ENTERO
        
        # Si no se encuentra, tipos incompatibles
        self.agregar_error_semantico(
            f"Operación '{operador}' no válida entre {self.tipo_a_texto(tipo1_base)} y {self.tipo_a_texto(tipo2_base)}", 
            linea
        )
        return TIPO_ERROR

    def verificar_tipo_asignacion(self, variable, tipo_var, tipo_expr, linea):
        """Verifica que la asignación sea tipo-segura"""
        # Conversiones permitidas en asignación
        conversiones_permitidas = {
            (RES_ENTERO, TIPO_ENTERO): True,
            (RES_ENTERO, TIPO_FLOTANTE): True,  # entero <- flotante (con pérdida)
            (RES_FLOTANTE, TIPO_FLOTANTE): True,
            (RES_FLOTANTE, TIPO_ENTERO): True,  # flotante <- entero OK
            (RES_CADENA, TIPO_CADENA): True,
            (RES_BOOLEANO, TIPO_BOOLEANO): True,
            (RES_BOOLEANO, TIPO_ENTERO): False, # booleano no acepta números
            (RES_ENTERO, TIPO_BOOLEANO): False, # entero no acepta booleanos
        }
        
        combinacion = (tipo_var, tipo_expr)
        if combinacion in conversiones_permitidas and conversiones_permitidas[combinacion]:
            return ERR_SEMANTICA_NO_ERROR
        else:
            tipo_var_texto = self.get_str_tipo_identificador(tipo_var)
            tipo_expr_texto = self.tipo_a_texto(tipo_expr)
            self.agregar_error_semantico(
                f"Asignación inválida: no se puede asignar {tipo_expr_texto} a variable '{variable}' de tipo {tipo_var_texto}", 
                linea
            )
            return ERR_SEMANTICA_TIPO_NO_COINCIDE

    def analizar_tipo_expresion(self, expresion):
        """Analiza y retorna el tipo de una expresión completa"""
        if not isinstance(expresion, dict):
            return TIPO_ERROR
            
        if expresion['tipo'] == 'acceso_arreglo':
            nombre_arreglo = expresion['nombre']
            tipo_arreglo = self.get_tipo_identificador(nombre_arreglo)
            if tipo_arreglo == RES_NO_DECL:
                self.agregar_error_semantico(f"Arreglo '{nombre_arreglo}' no declarado", 0)
                return TIPO_ERROR
            
            # Verificar que el índice sea entero
            tipo_indice = self.analizar_tipo_expresion(expresion['indice'])
            if tipo_indice != TIPO_ENTERO:
                self.agregar_error_semantico("Índice de arreglo debe ser entero", 0)
                return TIPO_ERROR
                
            # Retornar tipo del elemento del arreglo
            return self._obtener_tipo_elemento_arreglo(tipo_arreglo)
        
        if expresion['tipo'] == 'literal':
            return expresion.get('tipo_dato', TIPO_ERROR)
            
        elif expresion['tipo'] == 'variable':
            nombre_var = expresion['nombre']
            tipo_var = self.get_tipo_identificador(nombre_var)
            if tipo_var == RES_NO_DECL:
                self.agregar_error_semantico(f"Variable '{nombre_var}' no declarada", 0)
                return TIPO_ERROR
            return self.convertir_tipo_reservado_a_base(tipo_var)
            
        elif expresion['tipo'] == 'binaria':
            tipo_izq = self.analizar_tipo_expresion(expresion['izquierda'])
            tipo_der = self.analizar_tipo_expresion(expresion['derecha'])
            operador = expresion['operador']
            
            # Obtener línea actual para reportar errores
            linea_actual = self.lexico.get_lineas()
            
            tipo_resultado = self.verificar_compatibilidad_tipos(tipo_izq, tipo_der, operador, linea_actual)
            return tipo_resultado
            
        elif expresion['tipo'] == 'llamada_funcion':
            nombre_func = expresion['nombre']
            tipo_func = self.get_tipo_identificador(nombre_func)
            if tipo_func != RES_METODO:
                self.agregar_error_semantico(f"'{nombre_func}' no es una función", 0)
                return TIPO_ERROR
            # Obtener tipo de retorno de la función
            return self.obtener_tipo_retorno_metodo(nombre_func) or TIPO_VOID
            
        else:
            return TIPO_ERROR

    def convertir_tipo_reservado_a_base(self, tipo_reservado):
        """Convierte tipos RES_* a TIPO_* base"""
        if tipo_reservado == RES_ENTERO:
            return TIPO_ENTERO
        elif tipo_reservado == RES_FLOTANTE:
            return TIPO_FLOTANTE
        elif tipo_reservado == RES_CADENA:
            return TIPO_CADENA
        elif tipo_reservado == RES_BOOLEANO:
            return TIPO_BOOLEANO
        elif tipo_reservado == RES_VOID:
            return TIPO_VOID
        else:
            return TIPO_ERROR

    def tipo_a_texto(self, tipo):
        """Convierte código de tipo a texto legible"""
        tipos = {
            TIPO_ENTERO: "entero",
            TIPO_FLOTANTE: "flotante", 
            TIPO_CADENA: "cadena",
            TIPO_BOOLEANO: "booleano",
            TIPO_VOID: "void",
            TIPO_ERROR: "error",
            RES_ENTERO: "entero",
            RES_FLOTANTE: "flotante",
            RES_CADENA: "cadena", 
            RES_BOOLEANO: "booleano",
            RES_VOID: "void"
        }
        return tipos.get(tipo, "desconocido")

    def agregar_error_semantico(self, mensaje, linea):
        """Agrega un error semántico a la lista"""
        if not hasattr(self, 'errores_semanticos'):
            self.errores_semanticos = []
        self.errores_semanticos.append(f"Línea {linea}: {mensaje}")

    def obtener_tipo_retorno_metodo(self, nombre_metodo):
        """Obtiene el tipo de retorno de un método (simplificado)"""
        # Buscar en tabla de símbolos
        for simbolo in self.tabla_simbolos:
            if simbolo[0] == nombre_metodo and simbolo[1] == RES_METODO:
                return simbolo[3] if len(simbolo) > 3 else RES_VOID
        return None

    def _obtener_tipo_arreglo(self, tipo_elemento):
        """Convierte tipo de elemento a tipo de arreglo"""
        if tipo_elemento == RES_ENTERO:
            return TIPO_ARREGLO_ENTERO
        elif tipo_elemento == RES_FLOTANTE:
            return TIPO_ARREGLO_FLOTANTE
        elif tipo_elemento == RES_CADENA:
            return TIPO_ARREGLO_CADENA
        elif tipo_elemento == RES_BOOLEANO:
            return TIPO_ARREGLO_BOOLEANO
        return TIPO_ERROR

    def proc_def_acceso_arreglo(self, nombre_arreglo):
        """Procesa acceso a elemento de arreglo: nombres[0]"""
        error = ERR_NO_SINTAX_ERROR
        
        if self.tok_actual[0] == "[":
            self.sig_token()
            
            # Procesar expresión del índice
            expresion_indice = self.proc_def_expresion()
            tipo_indice = self.analizar_tipo_expresion(expresion_indice)
            
            # Verificar que el índice sea entero
            if tipo_indice != TIPO_ENTERO:
                self.agregar_error_semantico("Índice de arreglo debe ser entero", self.lexico.get_lineas())
                return ERR_SEMANTICA_TIPO_NO_COINCIDE
            
            if self.tok_actual[0] == "]":
                self.sig_token()
                
                # Agregar al árbol sintáctico
                acceso = self._agregar_instruccion_arbol('acceso_arreglo',
                    nombre=nombre_arreglo,
                    indice=expresion_indice
                )
                
                # Verificar si es asignación o lectura
                if self.tok_actual[0] == "=":
                    self.sig_token()
                    expresion_valor = self.proc_def_expresion()
                    
                    # Verificar tipos
                    tipo_arreglo = self.get_tipo_identificador(nombre_arreglo)
                    tipo_elemento_esperado = self._obtener_tipo_elemento_arreglo(tipo_arreglo)
                    tipo_valor = self.analizar_tipo_expresion(expresion_valor)
                    
                    if not self._son_tipos_compatibles_arreglo(tipo_elemento_esperado, tipo_valor):
                        self.agregar_error_semantico(
                            f"Tipo incompatible para arreglo '{nombre_arreglo}'", 
                            self.lexico.get_lineas()
                        )
                        return ERR_SEMANTICA_TIPO_NO_COINCIDE
                    
                    # Agregar asignación
                    asignacion = self._agregar_instruccion_arbol('asignacion_arreglo',
                        nombre=nombre_arreglo,
                        indice=expresion_indice,
                        valor=expresion_valor
                    )
            else:
                error = ERR_PARENTESIS_CERRAR
        else:
            error = ERR_PARENTESIS_ABRIR
            
        return error

    def _obtener_tipo_elemento_arreglo(self, tipo_arreglo):
        """Obtiene el tipo de elemento a partir del tipo de arreglo"""
        if tipo_arreglo == TIPO_ARREGLO_ENTERO:
            return RES_ENTERO
        elif tipo_arreglo == TIPO_ARREGLO_FLOTANTE:
            return RES_FLOTANTE
        elif tipo_arreglo == TIPO_ARREGLO_CADENA:
            return RES_CADENA
        elif tipo_arreglo == TIPO_ARREGLO_BOOLEANO:
            return RES_BOOLEANO
        return TIPO_ERROR

    def _son_tipos_compatibles_arreglo(self, tipo_arreglo, tipo_valor):
        """Verifica compatibilidad para asignación a arreglo"""
        conversiones = {
            (RES_ENTERO, TIPO_ENTERO): True,
            (RES_ENTERO, TIPO_FLOTANTE): True,
            (RES_FLOTANTE, TIPO_FLOTANTE): True,
            (RES_FLOTANTE, TIPO_ENTERO): True,
            (RES_CADENA, TIPO_CADENA): True,
            (RES_BOOLEANO, TIPO_BOOLEANO): True,
        }
        return conversiones.get((tipo_arreglo, tipo_valor), False)

    def agregar_identificador(self, iden, tipo, linea, tipo_retorno=None, tamanio=None):
        for elemento in self.tabla_simbolos:
            if elemento[0] == iden:
                return ERR_SEMANTICA_IDENTIFICADOR_YA_EXISTE
        
        # Para arreglos, guardar tamaño adicional
        if tipo == RES_ARREGLO:
            self.tabla_simbolos.append([iden, tipo, linea, tipo_retorno, tamanio])
        else:
            self.tabla_simbolos.append([iden, tipo, linea, tipo_retorno])
        return ERR_SEMANTICA_NO_ERROR

    def obtener_tamanio_arreglo(self, nombre_arreglo):
        """Obtiene el tamaño de un arreglo"""
        for elemento in self.tabla_simbolos:
            if elemento[0] == nombre_arreglo and elemento[1] == RES_ARREGLO:
                return elemento[4] if len(elemento) > 4 else 0
        return 0