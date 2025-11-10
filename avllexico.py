"""
lexico
"""


matriz_lexico = [
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, -1, 4, -1000, -1000, 4, 4, 4],
    [0, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # LIN_NUMERO - CORREGIDO: columna 3 va a estado 7
    [-1, -1, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # CORREGIDO: columna 3 va a estado 7
    [-1001, -1001, 8, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001, -1001],
    [-1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0],
    [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, -1, -1, 14, 14, 14],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0],
    [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, -1002, 19, 19, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1003, 0, 0, 0, 0, 0],
    [0, 0, 0, -1003, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, 30, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]

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

RES_CLASE = 3000
RES_FIN_CLASE = 3001
RES_METODO = 3002
RES_FIN_METODO = 3003
RES_CONSTRUCTOR = 3004
RES_FIN_CONSTRUCTOR = 3005
RES_HEREDA = 3006

RES_SI = 3010
RES_FIN_SI = 3011
RES_SINO = 3012
RES_PARA = 3013
RES_FIN_PARA = 3014
RES_MIENTRAS = 3015
RES_FIN_MIENTRAS = 3016

RES_IMPRIMIR = 3020
RES_LEER = 3021
RES_RETORNAR = 3022
RES_NUEVO = 3023

RES_ENTERO = 4000
RES_FLOTANTE = 4001
RES_CADENA = 4002
RES_BOOLEANO = 4003
RES_VOID = 4004
RES_VERDADERO = 4005
RES_FALSO = 4006
RES_NULO = 4007

RES_NO_DECL = 5000

lst_reservadas = (
    ("clase", RES_CLASE), ("fin_clase", RES_FIN_CLASE),
    ("metodo", RES_METODO), ("fin_metodo", RES_FIN_METODO),
    ("constructor", RES_CONSTRUCTOR), ("fin_constructor", RES_FIN_CONSTRUCTOR),
    ("hereda", RES_HEREDA),
    ("si", RES_SI), ("fin_si", RES_FIN_SI), ("sino", RES_SINO),
    ("para", RES_PARA), ("fin_para", RES_FIN_PARA),
    ("mientras", RES_MIENTRAS), ("fin_mientras", RES_FIN_MIENTRAS),
    ("imprimir", RES_IMPRIMIR), ("leer", RES_LEER),
    ("retornar", RES_RETORNAR), ("nuevo", RES_NUEVO),
    ("entero", RES_ENTERO), ("flotante", RES_FLOTANTE),
    ("cadena", RES_CADENA), ("booleano", RES_BOOLEANO),
    ("void", RES_VOID), ("verdadero", RES_VERDADERO),
    ("falso", RES_FALSO), ("nulo", RES_NULO)
)

ERR_NOERROR = 0
ERR_CADENA = -1000
ERR_NUMERO = -1001
ERR_COMENTARIO = -1002
ERR_CAR_INVALIDO = -1003

class Lexico:
    def __init__(self, t_chars):
        self.tira_cars = []
        self.no_lineas = 0
        self.lst_tokens = []
        for c in t_chars:
            self.tira_cars.append(c)
        
    def genera_lexico(self, con_comentarios):
        self.no_lineas = 0
        self.lst_tokens = []
        
        tipo_error = ERR_NOERROR
        str_token = ""
        typ_token = LIN_SIN_TIPO
        i_token = 0
        
        while i_token < len(self.tira_cars): 
            car = self.tira_cars[i_token]
            
            columna = self.tipo_caracter(car)
            if typ_token == LIN_SIN_TIPO:
                typ_token = self.tipo_token(columna)
                linea = typ_token
            
            if matriz_lexico[linea][columna] == -1000:
                tipo_error = ERR_CADENA
                break
            elif matriz_lexico[linea][columna] == -1001:
                tipo_error = ERR_NUMERO
                break
            elif matriz_lexico[linea][columna] == -1002:
                tipo_error = ERR_COMENTARIO
                break
            elif matriz_lexico[linea][columna] == -1003:
                str_token = car
                tipo_error = ERR_CAR_INVALIDO
                break
            elif matriz_lexico[linea][columna] > 0:
                str_token = str_token + car
                linea = matriz_lexico[linea][columna]
                i_token = i_token + 1
                
            elif matriz_lexico[linea][columna] == -1:
                if typ_token == LIN_IDENTIFICADOR:
                    b_r = self.tipo_identificador(str_token.lower())
                    self.lst_tokens.append((str_token.lower(), b_r))
                elif typ_token == LIN_NUMERO:
                    typ_token = LIN_NUM_FLOTANTE if "." in str_token else LIN_NUM_ENTERO
                    self.lst_tokens.append((str_token, typ_token))
                elif (typ_token in (LIN_MAS, LIN_MENOS, LIN_IGUAL, LIN_MAYOR, LIN_MENOR)):
                    self.lst_tokens.append((str_token, typ_token))
                elif typ_token == LIN_ESPACIO:
                    i_token = i_token + 1
                elif typ_token == LIN_EOLN:
                    self.lst_tokens.append(("[EOLN]", typ_token))
                    self.no_lineas = self.no_lineas + 1 
                    i_token = i_token + 1
                elif typ_token in (LIN_COMENTARIO, LIN_HASH):
                    str_token = str_token + car
                    i_token = i_token + 1
                    
                    if con_comentarios:
                        self.lst_tokens.append((str_token, typ_token))
                else:
                    str_token = str_token + car
                    i_token = i_token + 1
                    self.lst_tokens.append((str_token, typ_token))

                str_token = ""
                typ_token = LIN_SIN_TIPO
            
        self.lst_tokens.append(("[EOF]", LIN_EOF))                
        return tipo_error, str_token
    
    def tipo_caracter(self, c):
        car = ""
        if c == " ": 
             car = COL_ESPACIO
        elif (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c == '_'):
            car = COL_LETRAS
        elif (c >= '0' and c <= '9'):
            car = COL_NUMEROS 
        elif c == '.':
            car = COL_PUNTO 
        elif c in '()[]*/,':
            car = COL_UNITARIOS 
        elif c == '=':
            car = COL_IGUAL 
        elif c == '>':
            car = COL_MAYOR 
        elif c == '<':
            car = COL_MENOR 
        elif c == '+':
            car = COL_MAS 
        elif c == '-':
            car = COL_MENOS 
        elif c == '"':
            car = COL_COMILLAS
        elif c == '\n':
            car = COL_EOLN 
        elif c == '#': 
            car = COL_HASH 
        elif c == '{':
            car = COL_LLAVE_ABRIR 
        elif c == '}':
            car = COL_LLAVE_CERRAR
        elif c == "":
            car = COL_EOF 
        else:
            car = COL_OTROS 

        return car
    
    def tipo_token(self, c):
        tipo_tok = -1
  
        if c == COL_ESPACIO:      
            tipo_tok = LIN_ESPACIO 
        elif c == COL_EOLN:
            tipo_tok = LIN_EOLN
        elif c == COL_EOF:
            tipo_tok = LIN_EOF
        elif c == COL_LETRAS:
            tipo_tok = LIN_IDENTIFICADOR 
        elif c == COL_COMILLAS:
            tipo_tok = LIN_CADENA
        elif c == COL_NUMEROS:
            tipo_tok = LIN_NUMERO 
        elif c == COL_UNITARIOS:
            tipo_tok = LIN_SIMBOLO
        elif c == COL_MAS:
            tipo_tok = LIN_MAS 
        elif c == COL_HASH:
            tipo_tok = LIN_HASH 
        elif c == COL_MENOS:
            tipo_tok = LIN_MENOS
        elif c == COL_LLAVE_ABRIR:
            tipo_tok = LIN_COMENTARIO 
        elif c == COL_PUNTO:
            tipo_tok = LIN_PUNTO
        elif c == COL_IGUAL:
            tipo_tok = LIN_IGUAL
        elif c == COL_MAYOR:
            tipo_tok = LIN_MAYOR
        elif c == COL_MENOR:
            tipo_tok = LIN_MENOR
        else:
            tipo_tok = LIN_SIN_TIPO
    
        return tipo_tok
    
    def get_tipo_token_str(self, t, tt):
        s_t = "no definido"
        
        if t == LIN_ESPACIO:
            s_t = "espacio"
        elif t == LIN_IDENTIFICADOR:
            s_t = f"identificador [{tt.upper()}]"
        elif t == LIN_CADENA:
            s_t = "constante cadena"
        elif t == LIN_NUMERO:
            s_t = "constante numero"
        elif t == LIN_SIMBOLO:
            s_t = "simbolo"
        elif t == LIN_MAS:
            s_t = "operador suma"
        elif t == LIN_HASH:
            s_t = "comentario corto"
        elif t == LIN_MENOS:
            s_t = "operador resta"
        elif t == LIN_COMENTARIO:
            s_t = "comentario largo"
        elif t == LIN_EOLN:
            s_t = "fin de linea"
        elif t == LIN_EOF:
            s_t = "fin de archivo"
        elif t == LIN_SIN_TIPO:
            s_t = "sin tipo definido"
        elif t == LIN_PUNTO:
            s_t = "punto"
        elif t == LIN_IGUAL:
            s_t = "operador igual"
        elif t == LIN_MAYOR:
            s_t = "operador mayor"
        elif t == LIN_MENOR:
            s_t = "operador menor"
        elif t >= RES_CLASE and t <= RES_NULO:
            s_t = f"palabra reservada [{tt}]"
        elif t == LIN_NUM_ENTERO:
            s_t = "constante numero entero"
        elif t == LIN_NUM_FLOTANTE:
            s_t = "constante numero flotante"
            
        return s_t        
        
    def tipo_identificador(self, id):   
        p_res = LIN_IDENTIFICADOR
        for p in lst_reservadas:
            if id == p[0]:
                p_res = p[1]
                break
            
        return p_res

    def get(self):
        return self.lst_tokens
    
    def get_lineas(self):
        return self.no_lineas
    
    def mensaje_error(self, err):
        s = ""
        if ERR_NOERROR == err:
            s = "no se encontraron errores de léxico"
        elif ERR_CADENA == err:
            s = "cadena con errores"
        elif ERR_NUMERO == err:
            s = "numero mal construido"
        elif ERR_COMENTARIO == err:
            s = "comentario mal cerrado"
        elif ERR_CAR_INVALIDO == err:
            s = "token inválido"

        return s