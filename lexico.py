"""
Módulo de Análisis Léxico
"""



class Tipos:
    ENTERO = 1
    FLOTANTE = 2
    CADENA = 3
    BOOLEANO = 4
    VOID = 5
    ERROR = -1
    
    
    ARREGLO_ENTERO = 100
    ARREGLO_FLOTANTE = 101
    ARREGLO_CADENA = 102
    ARREGLO_BOOLEANO = 103
    
    
    LEX_CLASE = 3000
    LEX_FIN_CLASE = 3001
    LEX_METODO = 3002
    LEX_FIN_METODO = 3003
    LEX_CONSTRUCTOR = 3004
    LEX_FIN_CONSTRUCTOR = 3005
    LEX_HEREDA = 3006
    
    LEX_SI = 3010
    LEX_FIN_SI = 3011
    LEX_SINO = 3012
    LEX_PARA = 3013
    LEX_FIN_PARA = 3014
    LEX_MIENTRAS = 3015
    LEX_FIN_MIENTRAS = 3016
    
    LEX_IMPRIMIR = 3020
    LEX_LEER = 3021
    LEX_RETORNAR = 3022
    LEX_NUEVO = 3023
    LEX_HASTA = 3030
    LEX_FUNCION = 3050
    LEX_FIN_FUNCION = 3051
    LEX_LLAMAR = 3052
    
    LEX_ENTERO = 4000
    LEX_FLOTANTE = 4001
    LEX_CADENA = 4002
    LEX_BOOLEANO = 4003
    LEX_VOID = 4004
    LEX_VERDADERO = 4005
    LEX_FALSO = 4006
    LEX_NULO = 4007
    
    LEX_ARREGLO = 5000
    LEX_TAMANIO = 5001
    LEX_ELEMENTO = 5002
    
 
    LEX_AND = 6000  
    LEX_OR = 6001   
    LEX_NOT = 6002  
    
 
    LIN_SINTIPO = -1
    LIN_ESPACIO = 0
    LIN_IDENTIFICADOR = 1
    LIN_CADENA = 3
    LIN_NUMERO = 5
    LIN_SIMBOLO = 9
    LIN_MAS = 10
    LIN_HASH = 13
    LIN_MENOS = 15
    LIN_COMENTARIO = 18
    LIN_EOLN = 21
    LIN_EOF = 22
    LIN_SIN_TIPO = 23
    LIN_PUNTO = 24
    LIN_IGUAL = 25
    LIN_MAYOR = 28
    LIN_MENOR = 31
    
 
    LIN_NUM_ENTERO = 100
    LIN_NUM_FLOTANTE = 101
    
    LIN_AMPERSAND = 40
    LIN_PIPE = 41
    LIN_EXCLAMACION = 42
    LIN_AND = 43  
    LIN_OR = 44  
    LIN_NOT = 45 
    
    NO_DECLARADO = 5000
    
    ERROR_NINGUNO = 0
    ERROR_CADENA = -1000
    ERROR_NUMERO = -1001
    ERROR_COMENTARIO = -1002
    ERROR_CARACTER_INVALIDO = -1003
    
    COL_ESPACIO = 0
    COL_LETRAS = 1
    COL_NUMEROS = 2
    COL_PUNTO = 3
    COL_UNITARIOS = 4
    COL_IGUAL = 5
    COL_MAYOR = 6
    COL_MENOR = 7
    COL_MAS = 8
    COL_MENOS = 9
    COL_COMILLAS = 10
    COL_OTROS = 11
    COL_EOLN = 12
    COL_EOF = 13
    COL_HASH = 14
    COL_LLAVE_ABRIR = 15
    COL_LLAVE_CERRAR = 16
    COL_AMPERSAND = 17
    COL_PIPE = 18
    COL_EXCLAMACION = 19
    
    @classmethod
    def es_tipo_numerico(cls, tipo):
        return tipo in [cls.ENTERO, cls.FLOTANTE, cls.LEX_ENTERO, cls.LEX_FLOTANTE, 
                       cls.LIN_NUM_ENTERO, cls.LIN_NUM_FLOTANTE]
    
    @classmethod
    def es_tipo_escalar(cls, tipo):
        tipos_escalares = [
            cls.ENTERO, cls.FLOTANTE, cls.CADENA, cls.BOOLEANO,
            cls.LEX_ENTERO, cls.LEX_FLOTANTE, cls.LEX_CADENA, cls.LEX_BOOLEANO,
            cls.LIN_NUM_ENTERO, cls.LIN_NUM_FLOTANTE, cls.LIN_CADENA
        ]
        return tipo in tipos_escalares
    
    @classmethod
    def convertir_reservado_a_base(cls, tipo_reservado):
        conversiones = {
            cls.LEX_ENTERO: cls.ENTERO,
            cls.LEX_FLOTANTE: cls.FLOTANTE,
            cls.LEX_CADENA: cls.CADENA,
            cls.LEX_BOOLEANO: cls.BOOLEANO,
            cls.LEX_VOID: cls.VOID,
            cls.LIN_NUM_ENTERO: cls.ENTERO,
            cls.LIN_NUM_FLOTANTE: cls.FLOTANTE,
            cls.LIN_CADENA: cls.CADENA
        }
        return conversiones.get(tipo_reservado, cls.ERROR)
    
    @classmethod
    def obtener_tipo_literal(cls, token, tipo_token):
        if tipo_token in [cls.LIN_NUM_ENTERO, cls.LEX_ENTERO]:
            return cls.ENTERO
        elif tipo_token in [cls.LIN_NUM_FLOTANTE, cls.LEX_FLOTANTE]:
            return cls.FLOTANTE
        elif tipo_token in [cls.LIN_CADENA, cls.LEX_CADENA]:
            return cls.CADENA
        elif tipo_token in [cls.LEX_BOOLEANO, cls.LEX_VERDADERO, cls.LEX_FALSO]:
            return cls.BOOLEANO
        elif tipo_token == cls.LEX_VOID:
            return cls.VOID
        elif tipo_token == cls.LIN_IDENTIFICADOR:
            return cls.ERROR  
        else:
            return cls.ERROR



matriz_lexico = [
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, -1, 4, Tipos.ERROR_CADENA, Tipos.ERROR_CADENA, 4, 4, 4, 4, 4, 4],
    [0, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, 8, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO, Tipos.ERROR_NUMERO],
    [-1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0],
    [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, -1, -1, 14, 14, 14, 14, 14, 14],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0],
    [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, Tipos.ERROR_COMENTARIO, 19, 19, -1, 19, 19, 19],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Tipos.ERROR_CARACTER_INVALIDO, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, Tipos.ERROR_CARACTER_INVALIDO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, 30, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0],  
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1],  
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0], 
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1],  
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39], 
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  
]

lista_palabras_reservadas = (
    ("clase", Tipos.LEX_CLASE), ("fin_clase", Tipos.LEX_FIN_CLASE),
    ("metodo", Tipos.LEX_METODO), ("hasta", Tipos.LEX_HASTA),
    ("constructor", Tipos.LEX_CONSTRUCTOR), ("fin_constructor", Tipos.LEX_FIN_CONSTRUCTOR),
    ("hereda", Tipos.LEX_HEREDA),
    ("si", Tipos.LEX_SI), ("fin_si", Tipos.LEX_FIN_SI), ("sino", Tipos.LEX_SINO),
    ("para", Tipos.LEX_PARA), ("fin_para", Tipos.LEX_FIN_PARA),
    ("mientras", Tipos.LEX_MIENTRAS), ("fin_mientras", Tipos.LEX_FIN_MIENTRAS),
    ("imprimir", Tipos.LEX_IMPRIMIR), ("leer", Tipos.LEX_LEER),
    ("retornar", Tipos.LEX_RETORNAR), ("nuevo", Tipos.LEX_NUEVO),
    ("entero", Tipos.LEX_ENTERO), ("flotante", Tipos.LEX_FLOTANTE),
    ("cadena", Tipos.LEX_CADENA), ("booleano", Tipos.LEX_BOOLEANO),
    ("void", Tipos.LEX_VOID), ("verdadero", Tipos.LEX_VERDADERO),
    ("falso", Tipos.LEX_FALSO), ("nulo", Tipos.LEX_NULO),
    ("arreglo", Tipos.LEX_ARREGLO),
    ("tamanio", Tipos.LEX_TAMANIO), 
    ("funcion", Tipos.LEX_FUNCION),
    ("fin_funcion", Tipos.LEX_FIN_FUNCION),
    ("llamar", Tipos.LEX_LLAMAR),
    ("elemento", Tipos.LEX_ELEMENTO),
    ("&&", Tipos.LEX_AND),
    ("||", Tipos.LEX_OR), 
    ("!", Tipos.LEX_NOT)
)

class Lexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = list(codigo_fuente)
        self.numero_lineas = 0
        self.lista_tokens = []
        self.tipos = Tipos 
        
    def analizar(self, incluir_comentarios=False):
        self.numero_lineas = 0
        self.lista_tokens = []
        
        codigo_error = Tipos.ERROR_NINGUNO
        token_actual = ""
        tipo_token = Tipos.LIN_SIN_TIPO
        indice_token = 0
        linea_automata = 0
        
        while indice_token < len(self.codigo_fuente):
            caracter = self.codigo_fuente[indice_token]
            
            columna = self._clasificar_caracter(caracter)
            if tipo_token == Tipos.LIN_SIN_TIPO:
                tipo_token = self._obtener_tipo_token(columna)
                linea_automata = tipo_token
            
            transicion = matriz_lexico[linea_automata][columna]
            
    
            if transicion == Tipos.ERROR_CADENA:
                codigo_error = Tipos.ERROR_CADENA
                break
            elif transicion == Tipos.ERROR_NUMERO:
                codigo_error = Tipos.ERROR_NUMERO
                break
            elif transicion == Tipos.ERROR_COMENTARIO:
                codigo_error = Tipos.ERROR_COMENTARIO
                break
            elif transicion == Tipos.ERROR_CARACTER_INVALIDO:
                token_actual = caracter
                codigo_error = Tipos.ERROR_CARACTER_INVALIDO
                break
            elif transicion > 0:
    
                token_actual += caracter
                linea_automata = transicion
                indice_token += 1
                
            elif transicion == -1:
    
                if tipo_token == Tipos.LIN_IDENTIFICADOR:
                    tipo_final = self._clasificar_identificador(token_actual.lower())
                    self.lista_tokens.append((token_actual.lower(), tipo_final))
                elif tipo_token == Tipos.LIN_NUMERO:
    
                    tipo_final = Tipos.LIN_NUM_FLOTANTE if "." in token_actual else Tipos.LIN_NUM_ENTERO
                    self.lista_tokens.append((token_actual, tipo_final))
                elif tipo_token in (Tipos.LIN_MAS, Tipos.LIN_MENOS, Tipos.LIN_IGUAL, 
                                  Tipos.LIN_MAYOR, Tipos.LIN_MENOR, Tipos.LIN_AND, 
                                  Tipos.LIN_OR, Tipos.LIN_NOT):
                    self.lista_tokens.append((token_actual, tipo_token))
                elif tipo_token == Tipos.LIN_ESPACIO:
    
                    indice_token += 1
                elif tipo_token == Tipos.LIN_EOLN:
                    self.lista_tokens.append(("[EOLN]", tipo_token))
                    self.numero_lineas += 1
                    indice_token += 1
                elif tipo_token in (Tipos.LIN_COMENTARIO, Tipos.LIN_HASH):
                    token_actual += caracter
                    indice_token += 1
                    
                    if incluir_comentarios:
                        self.lista_tokens.append((token_actual, tipo_token))
                else:
                    token_actual += caracter
                    indice_token += 1
                    self.lista_tokens.append((token_actual, tipo_token))

                token_actual = ""
                tipo_token = Tipos.LIN_SIN_TIPO
                linea_automata = 0
            
    
        self.lista_tokens.append(("[EOF]", Tipos.LIN_EOF))
        
        return codigo_error, token_actual
    
    def _clasificar_caracter(self, caracter):
    
        if caracter == " ":
            return Tipos.COL_ESPACIO
        elif (caracter >= 'A' and caracter <= 'Z') or (caracter >= 'a' and caracter <= 'z') or (caracter == '_'):
            return Tipos.COL_LETRAS
        elif (caracter >= '0' and caracter <= '9'):
            return Tipos.COL_NUMEROS
        elif caracter == '.':
            return Tipos.COL_PUNTO
        elif caracter in '()[]*/,:;':
            return Tipos.COL_UNITARIOS
        elif caracter == '=':
            return Tipos.COL_IGUAL
        elif caracter == '>':
            return Tipos.COL_MAYOR
        elif caracter == '<':
            return Tipos.COL_MENOR
        elif caracter == '+':
            return Tipos.COL_MAS
        elif caracter == '-':
            return Tipos.COL_MENOS
        elif caracter == '"':
            return Tipos.COL_COMILLAS
        elif caracter == '\n':
            return Tipos.COL_EOLN
        elif caracter == '#':
            return Tipos.COL_HASH
        elif caracter == '{':
            return Tipos.COL_LLAVE_ABRIR
        elif caracter == '}':
            return Tipos.COL_LLAVE_CERRAR
        elif caracter == '&':
            return Tipos.COL_AMPERSAND
        elif caracter == '|':
            return Tipos.COL_PIPE
        elif caracter == '!':
            return Tipos.COL_EXCLAMACION
        elif caracter == "":
            return Tipos.COL_EOF
        else:
            return Tipos.COL_OTROS
    
    def _obtener_tipo_token(self, columna):
    
        if columna == Tipos.COL_ESPACIO:
            return Tipos.LIN_ESPACIO
        elif columna == Tipos.COL_EOLN:
            return Tipos.LIN_EOLN
        elif columna == Tipos.COL_EOF:
            return Tipos.LIN_EOF
        elif columna == Tipos.COL_LETRAS:
            return Tipos.LIN_IDENTIFICADOR
        elif columna == Tipos.COL_COMILLAS:
            return Tipos.LIN_CADENA
        elif columna == Tipos.COL_NUMEROS:
            return Tipos.LIN_NUMERO
        elif columna == Tipos.COL_UNITARIOS:
            return Tipos.LIN_SIMBOLO
        elif columna == Tipos.COL_MAS:
            return Tipos.LIN_MAS
        elif columna == Tipos.COL_HASH:
            return Tipos.LIN_HASH
        elif columna == Tipos.COL_MENOS:
            return Tipos.LIN_MENOS
        elif columna == Tipos.COL_LLAVE_ABRIR:
            return Tipos.LIN_COMENTARIO
        elif columna == Tipos.COL_PUNTO:
            return Tipos.LIN_PUNTO
        elif columna == Tipos.COL_IGUAL:
            return Tipos.LIN_IGUAL
        elif columna == Tipos.COL_MAYOR:
            return Tipos.LIN_MAYOR
        elif columna == Tipos.COL_MENOR:
            return Tipos.LIN_MENOR
        elif columna == Tipos.COL_AMPERSAND:
            return Tipos.LIN_AMPERSAND
        elif columna == Tipos.COL_PIPE:
            return Tipos.LIN_PIPE
        elif columna == Tipos.COL_EXCLAMACION:
            return Tipos.LIN_EXCLAMACION
        else:
            return Tipos.LIN_SIN_TIPO
    
    def _clasificar_identificador(self, identificador):
    
        for palabra, tipo in lista_palabras_reservadas:
            if identificador == palabra:
                return tipo
        return Tipos.LIN_IDENTIFICADOR
    
    def obtener_descripcion_token(self, tipo_token, valor_token):
    
        descripciones = {
            Tipos.LIN_ESPACIO: "espacio",
            Tipos.LIN_IDENTIFICADOR: f"identificador [{valor_token.upper()}]",
            Tipos.LIN_CADENA: "constante cadena",
            Tipos.LIN_NUMERO: "constante numero",
            Tipos.LIN_SIMBOLO: "simbolo",
            Tipos.LIN_MAS: "operador suma",
            Tipos.LIN_HASH: "comentario corto",
            Tipos.LIN_MENOS: "operador resta",
            Tipos.LIN_COMENTARIO: "comentario largo",
            Tipos.LIN_EOLN: "fin de linea",
            Tipos.LIN_EOF: "fin de archivo",
            Tipos.LIN_SIN_TIPO: "sin tipo definido",
            Tipos.LIN_PUNTO: "punto",
            Tipos.LIN_IGUAL: "operador igual",
            Tipos.LIN_MAYOR: "operador mayor",
            Tipos.LIN_MENOR: "operador menor",
            Tipos.LIN_NUM_ENTERO: "constante numero entero",
            Tipos.LIN_NUM_FLOTANTE: "constante numero flotante",
            Tipos.LIN_AMPERSAND: "operador and",
            Tipos.LIN_PIPE: "operador or", 
            Tipos.LIN_EXCLAMACION: "operador not",
            Tipos.LIN_AND: "operador and (&&)",
            Tipos.LIN_OR: "operador or (||)",
            Tipos.LIN_NOT: "operador not (!)",
        }
        
    
        if tipo_token >= Tipos.LEX_CLASE and tipo_token <= Tipos.LEX_NOT:
            return f"palabra reservada [{valor_token}]"
        
        return descripciones.get(tipo_token, "no definido")
    
    def obtener_tipo_dato(self, token, tipo_token):
    
        return Tipos.obtener_tipo_literal(token, tipo_token)
    
    
    def genera_lexico(self, con_comentarios=False):
    
        return self.analizar(incluir_comentarios=con_comentarios)
    
    def get(self):
    
        return self.lista_tokens
    
    def get_lineas(self):
    
        return self.numero_lineas
    
    def get_tipo_token_str(self, tipo_token, valor_token):
    
        return self.obtener_descripcion_token(tipo_token, valor_token)
    
    def tipo_identificador(self, identificador):
    
        return self._clasificar_identificador(identificador)
    
    def mensaje_error(self, codigo_error):
    
        mensajes = {
            Tipos.ERROR_NINGUNO: "no se encontraron errores de léxico",
            Tipos.ERROR_CADENA: "cadena con errores",
            Tipos.ERROR_NUMERO: "numero mal construido",
            Tipos.ERROR_COMENTARIO: "comentario mal cerrado",
            Tipos.ERROR_CARACTER_INVALIDO: "token inválido",
        }
        return mensajes.get(codigo_error, "error desconocido")
        
    def convertir_tipo_reservado_a_base(self, tipo_reservado):

        return Tipos.convertir_reservado_a_base(tipo_reservado)
    
    def es_tipo_numerico(self, tipo):

        return Tipos.es_tipo_numerico(tipo)
    
    def es_tipo_escalar(self, tipo):
        return Tipos.es_tipo_escalar(tipo)



TIPO_ENTERO = Tipos.ENTERO
TIPO_FLOTANTE = Tipos.FLOTANTE
TIPO_CADENA = Tipos.CADENA
TIPO_BOOLEANO = Tipos.BOOLEANO
TIPO_VOID = Tipos.VOID
TIPO_ERROR = Tipos.ERROR

TIPO_ARREGLO_ENTERO = Tipos.ARREGLO_ENTERO
TIPO_ARREGLO_FLOTANTE = Tipos.ARREGLO_FLOTANTE
TIPO_ARREGLO_CADENA = Tipos.ARREGLO_CADENA
TIPO_ARREGLO_BOOLEANO = Tipos.ARREGLO_BOOLEANO


RES_CLASE = Tipos.LEX_CLASE
RES_FIN_CLASE = Tipos.LEX_FIN_CLASE
RES_METODO = Tipos.LEX_METODO
RES_FIN_METODO = Tipos.LEX_FIN_METODO
RES_CONSTRUCTOR = Tipos.LEX_CONSTRUCTOR
RES_FIN_CONSTRUCTOR = Tipos.LEX_FIN_CONSTRUCTOR
RES_HEREDA = Tipos.LEX_HEREDA

RES_SI = Tipos.LEX_SI
RES_FIN_SI = Tipos.LEX_FIN_SI
RES_SINO = Tipos.LEX_SINO
RES_PARA = Tipos.LEX_PARA
RES_FIN_PARA = Tipos.LEX_FIN_PARA
RES_MIENTRAS = Tipos.LEX_MIENTRAS
RES_FIN_MIENTRAS = Tipos.LEX_FIN_MIENTRAS

RES_IMPRIMIR = Tipos.LEX_IMPRIMIR
RES_LEER = Tipos.LEX_LEER
RES_RETORNAR = Tipos.LEX_RETORNAR
RES_NUEVO = Tipos.LEX_NUEVO

RES_ENTERO = Tipos.LEX_ENTERO
RES_FLOTANTE = Tipos.LEX_FLOTANTE
RES_CADENA = Tipos.LEX_CADENA
RES_BOOLEANO = Tipos.LEX_BOOLEANO
RES_VOID = Tipos.LEX_VOID
RES_VERDADERO = Tipos.LEX_VERDADERO
RES_FALSO = Tipos.LEX_FALSO
RES_NULO = Tipos.LEX_NULO

RES_ARREGLO = Tipos.LEX_ARREGLO
RES_TAMANIO = Tipos.LEX_TAMANIO
RES_ELEMENTO = Tipos.LEX_ELEMENTO


RES_AND = Tipos.LEX_AND
RES_OR = Tipos.LEX_OR
RES_NOT = Tipos.LEX_NOT

RES_NO_DECL = Tipos.NO_DECLARADO

ERR_NOERROR = Tipos.ERROR_NINGUNO
ERR_CADENA = Tipos.ERROR_CADENA
ERR_NUMERO = Tipos.ERROR_NUMERO
ERR_COMENTARIO = Tipos.ERROR_COMENTARIO
ERR_CAR_INVALIDO = Tipos.ERROR_CARACTER_INVALIDO

lst_reservadas = lista_palabras_reservadas


LIN_SINTIPO = Tipos.LIN_SINTIPO
LIN_ESPACIO = Tipos.LIN_ESPACIO
LIN_IDENTIFICADOR = Tipos.LIN_IDENTIFICADOR
LIN_CADENA = Tipos.LIN_CADENA
LIN_NUMERO = Tipos.LIN_NUMERO
LIN_SIMBOLO = Tipos.LIN_SIMBOLO
LIN_MAS = Tipos.LIN_MAS
LIN_HASH = Tipos.LIN_HASH
LIN_MENOS = Tipos.LIN_MENOS
LIN_COMENTARIO = Tipos.LIN_COMENTARIO
LIN_EOLN = Tipos.LIN_EOLN
LIN_EOF = Tipos.LIN_EOF
LIN_SIN_TIPO = Tipos.LIN_SIN_TIPO
LIN_PUNTO = Tipos.LIN_PUNTO
LIN_IGUAL = Tipos.LIN_IGUAL
LIN_MAYOR = Tipos.LIN_MAYOR
LIN_MENOR = Tipos.LIN_MENOR

LIN_NUM_ENTERO = Tipos.LIN_NUM_ENTERO
LIN_NUM_FLOTANTE = Tipos.LIN_NUM_FLOTANTE

LIN_AMPERSAND = Tipos.LIN_AMPERSAND
LIN_PIPE = Tipos.LIN_PIPE
LIN_EXCLAMACION = Tipos.LIN_EXCLAMACION
LIN_AND = Tipos.LIN_AND
LIN_OR = Tipos.LIN_OR
LIN_NOT = Tipos.LIN_NOT