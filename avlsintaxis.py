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

class Sintaxis:
    def __init__(self, lex):
        self.lexico = lex
        self.lst_tokens = lex.get()
        self.i_token = 0
        self.tok_actual = ("", LIN_SINTIPO)
        self.tabla_simbolos = []
        self.clase_actual = ""
       
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
        tipo_ident = self.tok_actual[1]
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            ident = self.tok_actual[0]
            self.sig_token()
            if self.tok_actual[1] == LIN_EOLN:
                error = self.agregar_identificador(ident, tipo_ident, 0)
                if error == ERR_SEMANTICA_NO_ERROR:
                    self.sig_token()
            else:
                error = ERR_EOLN
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
        tipo_retorno = self.tok_actual[1]
        self.sig_token()
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            ident = self.tok_actual[0]
            self.sig_token()
            
            if self.tok_actual[1] == LIN_EOLN:
                error = self.agregar_identificador(ident, RES_METODO, 0)
                if error == ERR_SEMANTICA_NO_ERROR:
                    self.sig_token()
                    error = self.proc_instrucciones()
                    
                    if error == ERR_NO_SINTAX_ERROR and self.tok_actual[1] == RES_FIN_METODO:
                        self.sig_token()
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
            if self.tok_actual[1] == RES_SI:
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
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        error = self.proc_def_expresion()
        return error
    
    def proc_def_condicion(self):
        error = ERR_NO_SINTAX_ERROR
        self.sig_token()
        error = self.proc_def_expresion()
        
        if error == ERR_NO_SINTAX_ERROR:
            if self.tok_actual[0] in ("==", ">=", "<=", "<>", ">", "<"):
                self.sig_token()
                error = self.proc_def_expresion()
            else:
                error = ERR_OP_LOGICO
                
        return error
    
    def proc_def_asignacion(self):
        error = ERR_NO_SINTAX_ERROR
        
        if self.tok_actual[1] == LIN_IDENTIFICADOR:
            tipo_id = self.get_tipo_identificador(self.tok_actual[0])
            if tipo_id == RES_NO_DECL:
                return ERR_SEMANTICA_IDENTIFICADOR_NO_DECL
                
            self.sig_token()
            if self.tok_actual[0] == "=":
                self.sig_token()
                error = self.proc_def_expresion()
                
        return error
    
    def proc_def_identificador(self):
        error = ERR_NO_SINTAX_ERROR
        tipo_id = self.get_tipo_identificador(self.tok_actual[0])
        
        if tipo_id == RES_NO_DECL:
            return ERR_SEMANTICA_IDENTIFICADOR_NO_DECL
        
        self.sig_token()
        
        if self.tok_actual[0] == "=":
            error = self.proc_def_asignacion()
        elif self.tok_actual[0] == "(":
            error = self.proc_def_llamada_metodo()
        elif tipo_id != RES_METODO:
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
       
        return error
    
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
    
    def _construir_arbol(self):
        """Construye el árbol sintáctico a partir de los tokens"""
        # Implementación simplificada para demostración
        arbol = []
        # Lógica para construir el árbol
        return arbol