""" Esta es la version personalizada del lexico para mi lenguaje llamado Avellana """

# Matriz de transición léxica para Avellana - CORREGIDA
matrizLexico = [
    # Estados para reconocer los tokens de Avellana
    # Col: 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20   21
    [-1,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,  -1,  0,   0,   0,   0,   0,   0,   0,   0],   # 0
    [0,   2,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 1
    [-1,  2,   2,   -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 2
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 3
    [4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   -1,  4,   -1000,-1000,4,   4,   4,   4,   4,   4,   4,   4],  # 4
    [0,   0,   6,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 5
    [-1,  -1,  6,   7,   -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 6
    [-1001,-1001,8,  -1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001,-1001], # 7
    [-1,  -1,  8,   -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 8
    [0,   0,   0,   0,   -1,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 9
    [0,   0,   0,   0,   0,   0,   0,   0,   11,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 10
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  12,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 11
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 12
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   14,  0,   0,   0,   0,   0,   0,   0],   # 13
    [14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  -1,  -1,  14,  14,  14,  14,  14,  14,  14,  14],  # 14
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   16,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 15
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  17,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 16
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 17
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   19,  0,   0,   0,   0,   0,   0],   # 18
    [19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  19,  -1002,19,  19,  -1,  19,  19,  19,  19,  19],  # 19
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,  0,   0,   0,   0,   0,   0,   0,   0,   0],   # 20
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,  0,   0,   0,   0,   0,   0,   0,   0],   # 21
    [0,   0,   0,   -1003,0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 22
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1003,0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 23
    [0,   0,   0,   0,   0,   26,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 24
    [-1,  -1,  -1,  -1,  -1,  27,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 25
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 26
    [0,   0,   0,   0,   0,   0,   29,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],   # 27
    [-1,  -1,  -1,  -1,  -1,  30,  -1,  30,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 28
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 29
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  32,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 30
    [-1,  -1,  -1,  -1,  -1,  33,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 31
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 32
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   35,  0,   0,   0,   0],   # 33
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   36,  0,   0,   0],   # 34
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 35
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 36
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   38,  0,   0],   # 37
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 38
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   40,  0],   # 39
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 40
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   42],  # 41
    [-1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], # 42
]

# Columnas de la matriz - CORREGIDO
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
COL_INTERROGACION = 17
COL_PIPE = 18
COL_PAREN_ABRE = 19
COL_PAREN_CIERRA = 20
COL_COMA = 21

# Líneas (estados) de la matriz - CORREGIDO
LIN_ESPACIO = 0
LIN_IDENTIFICADOR = 1
LIN_CADENA = 3
LIN_NUMERO = 5
LIN_SIMBOLO = 9
LIN_MAS = 10
LIN_HASH = 13
LIN_MENOS = 15
LIN_COMENTARIO = 18
LIN_EOLN = 20
LIN_EOF = 21
LIN_SIN_TIPO = 22
LIN_PUNTO = 23
LIN_IGUAL = 24
LIN_MAYOR = 27
LIN_MENOR = 30
LIN_INTERROGACION = 33
LIN_PIPE = 34
LIN_PAREN_ABRE = 37
LIN_PAREN_CIERRA = 39
LIN_COMA = 41
LIN_MULTIPLICACION = 4   # Usando COL_UNITARIOS para * y /
LIN_DIVISION = 4
LIN_CORCHETE_ABRE = 4    # Usando COL_UNITARIOS para [ y ]
LIN_CORCHETE_CIERRA = 4

# Palabras reservadas de Avellana - Declaraciones
RES_SEA = 3000
RES_SEAN = 3001
RES_FIJO = 3002
RES_CUANDO = 3003
RES_HACE = 3004
RES_FIN = 3005
RES_DEFINE = 3006
RES_COMO = 3007
RES_TRAE = 3008
RES_DESDE = 3009

# Palabras reservadas - Control de flujo
RES_SI = 3010
RES_SI_NO = 3011
RES_O_SI = 3012
RES_ENTONCES = 3013
RES_SEGUN = 3014
RES_OPCION = 3015
RES_MIENTRAS = 3016
RES_POR_CADA = 3017
RES_EN = 3018
RES_REPETIR = 3019
RES_HASTA_QUE = 3020
RES_SALIR = 3021
RES_SIGUIENTE = 3022
RES_DE = 3023
RES_A_MENOS_QUE = 3024

# Palabras reservadas - Valores
RES_VERDAD = 3030
RES_FALSO = 3031
RES_NADA = 3032
RES_Y = 3033
RES_O = 3034
RES_NO = 3035
RES_ES = 3036
RES_NO_ES = 3037
RES_TIPO_DE = 3038

# Palabras reservadas - Funciones
RES_RETORNA = 3040
RES_YO = 3041
RES_SUPERIOR = 3042

# Palabras reservadas - Estructuras
RES_TIENE = 3050
RES_PUEDE = 3051
RES_PROPIEDAD = 3052
RES_COMO_CLASE = 3053
RES_EXTIENDE = 3054
RES_CON_CAPACIDAD = 3055
RES_CAPACIDAD = 3056

# Palabras reservadas - Manejo de errores
RES_INTENTA = 3060
RES_MANEJA = 3061
RES_SIEMPRE = 3062
RES_ERROR = 3063
RES_O_SI_FALLA = 3064

# Palabras reservadas - Funcional
RES_DONDE = 3070
RES_TRANSFORMA = 3071
RES_COMBINA = 3072
RES_COMPONER = 3073

# Palabras reservadas - Async
RES_COMO_TAREA = 3080
RES_ESPERA = 3081
RES_EN_PARALELO = 3082

# Palabras reservadas - Contextos
RES_DENTRO_DE = 3090
RES_REQUIERE = 3091
RES_ASEGURA = 3092

# Palabras reservadas - Rangos y operadores
RES_HASTA = 3100
RES_CON_PASO = 3101
RES_CADA = 3102
RES_INVERTIDO = 3103
RES_FINAL = 3104
RES_AGREGA = 3105
RES_AGREGA_VARIOS = 3106
RES_CONTIENE = 3107

# Tipos de datos
RES_NUMERO = 4000
RES_TEXTO = 4001
RES_BOOL = 4002
RES_LISTA = 4003
RES_COLECCION = 4004
RES_CONJUNTO = 4005

# Unidades especiales
RES_SEGUNDOS = 4010
RES_MILISEGUNDOS = 4011
RES_MINUTOS = 4012
RES_METROS = 4013
RES_KILOMETROS = 4014

# Operadores adicionales
RES_IMPRIMIR = 5000
RES_LEER = 5001

# Lista completa de palabras reservadas - ACTUALIZADA
lstReservadas = (
    # Declaraciones
    ("sea", RES_SEA), ("sean", RES_SEAN), ("fijo", RES_FIJO),
    ("cuando", RES_CUANDO), ("hace", RES_HACE), ("fin", RES_FIN),
    ("define", RES_DEFINE), ("como", RES_COMO), ("trae", RES_TRAE),
    ("desde", RES_DESDE),
    
    # Control de flujo
    ("si", RES_SI), ("si_no", RES_SI_NO), ("o_si", RES_O_SI),
    ("entonces", RES_ENTONCES), ("segun", RES_SEGUN), ("opcion", RES_OPCION),
    ("mientras", RES_MIENTRAS), ("por_cada", RES_POR_CADA), ("en", RES_EN),
    ("repetir", RES_REPETIR), ("hasta_que", RES_HASTA_QUE),
    ("salir", RES_SALIR), ("siguiente", RES_SIGUIENTE), ("de", RES_DE),
    ("a_menos_que", RES_A_MENOS_QUE),
    
    # Valores
    ("verdad", RES_VERDAD), ("falso", RES_FALSO), ("nada", RES_NADA),
    ("y", RES_Y), ("o", RES_O), ("no", RES_NO),
    ("es", RES_ES), ("no_es", RES_NO_ES), ("tipo_de", RES_TIPO_DE),
    
    # Funciones
    ("retorna", RES_RETORNA), ("yo", RES_YO), ("superior", RES_SUPERIOR),
    
    # Estructuras
    ("tiene", RES_TIENE), ("puede", RES_PUEDE), ("propiedad", RES_PROPIEDAD),
    ("como_clase", RES_COMO_CLASE), ("extiende", RES_EXTIENDE),
    ("con_capacidad", RES_CON_CAPACIDAD), ("capacidad", RES_CAPACIDAD),
    
    # Manejo de errores
    ("intenta", RES_INTENTA), ("maneja", RES_MANEJA), ("siempre", RES_SIEMPRE),
    ("error", RES_ERROR), ("o_si_falla", RES_O_SI_FALLA),
    
    # Funcional
    ("donde", RES_DONDE), ("transforma", RES_TRANSFORMA),
    ("combina", RES_COMBINA), ("componer", RES_COMPONER),
    
    # Async
    ("como_tarea", RES_COMO_TAREA), ("espera", RES_ESPERA),
    ("en_paralelo", RES_EN_PARALELO),
    
    # Contextos
    ("dentro_de", RES_DENTRO_DE), ("requiere", RES_REQUIERE),
    ("asegura", RES_ASEGURA),
    
    # Rangos y operadores
    ("hasta", RES_HASTA), ("con_paso", RES_CON_PASO),
    ("cada", RES_CADA), ("invertido", RES_INVERTIDO),
    ("final", RES_FINAL), ("agrega", RES_AGREGA),
    ("agrega_varios", RES_AGREGA_VARIOS), ("contiene", RES_CONTIENE),
    
    # Tipos
    ("numero", RES_NUMERO), ("texto", RES_TEXTO), ("bool", RES_BOOL),
    ("lista", RES_LISTA), ("coleccion", RES_COLECCION), ("conjunto", RES_CONJUNTO),
    
    # Unidades
    ("segundos", RES_SEGUNDOS), ("milisegundos", RES_MILISEGUNDOS),
    ("minutos", RES_MINUTOS), ("metros", RES_METROS), ("kilometros", RES_KILOMETROS),
    
    # Operadores E/S
    ("imprimir", RES_IMPRIMIR), ("leer", RES_LEER),
)

# Códigos de error
ERR_NOERROR = 0
ERR_CADENA = -1000
ERR_NUMERO = -1001
ERR_COMENTARIO = -1002
ERR_CAR_INVALIDO = -1003

# Mensajes de error chidos
MENSAJES_ERROR = {
    ERR_CADENA: "Se te olvidaron las comillas",
    ERR_NUMERO: "Revisa los puntos decimales",
    ERR_COMENTARIO: "Cierra bien el comentario",
    ERR_CAR_INVALIDO: "Este carácter no es válido en Avellana"
}


class LexicoAvellana:
    """
    Analizador Léxico para Avellana
    Convierte el código fuente en tokens reconocibles
    """
    
    def __init__(self, codigo_fuente):
        self.tiraCars = list(codigo_fuente)
        self.lstTokens = []
        self.noLineas = 0
    
    def generaLexico(self):
        """
        Genera el análisis léxico completo
        Retorna: (codigo_error, token_donde_ocurrio, mensaje_amigable)
        """
        self.noLineas = 1  # Comenzamos en línea 1
        self.lstTokens = []
        
        tipoError = ERR_NOERROR
        strToken = ""
        typToken = LIN_SIN_TIPO
        iToken = 0
        
        while iToken < len(self.tiraCars):
            car = self.tiraCars[iToken]
            
            columna = self.tipoCaracter(car)
            if typToken == LIN_SIN_TIPO:
                typToken = self.tipoToken(columna)
                linea = typToken
            
            # Verificar que los índices estén dentro de los límites
            if linea >= len(matrizLexico) or columna >= len(matrizLexico[linea]):
                strToken = car
                tipoError = ERR_CAR_INVALIDO
                break
                
            valor_matriz = matrizLexico[linea][columna]
            
            # Manejo de errores
            if valor_matriz == -1000:
                tipoError = ERR_CADENA
                break
            elif valor_matriz == -1001:
                tipoError = ERR_NUMERO
                break
            elif valor_matriz == -1002:
                tipoError = ERR_COMENTARIO
                break
            elif valor_matriz == -1003:
                strToken = car
                tipoError = ERR_CAR_INVALIDO
                break
            
            # Estado de transición válido
            elif valor_matriz > 0:
                strToken += car
                linea = valor_matriz
                iToken += 1
            
            # Token completo (estado de aceptación)
            elif valor_matriz == -1:
                if typToken == LIN_IDENTIFICADOR:
                    bR = self.tipoIdentificador(strToken.lower())
                    self.lstTokens.append((strToken.lower(), bR, self.noLineas))
                elif typToken in [LIN_NUMERO, LIN_MAS, LIN_MENOS, LIN_IGUAL, 
                                  LIN_MAYOR, LIN_MENOR, LIN_PIPE, LIN_PAREN_ABRE, 
                                  LIN_PAREN_CIERRA, LIN_COMA]:
                    self.lstTokens.append((strToken, typToken, self.noLineas))
                elif typToken == LIN_ESPACIO:
                    iToken += 1
                elif typToken == LIN_EOLN:
                    self.noLineas += 1
                    iToken += 1
                else:
                    strToken += car
                    iToken += 1
                    self.lstTokens.append((strToken, typToken, self.noLineas))
                
                strToken = ""
                typToken = LIN_SIN_TIPO
            else:
                iToken += 1
        
        # Procesar último token si queda pendiente
        if strToken and tipoError == ERR_NOERROR:
            if typToken == LIN_IDENTIFICADOR:
                bR = self.tipoIdentificador(strToken.lower())
                self.lstTokens.append((strToken.lower(), bR, self.noLineas))
            else:
                self.lstTokens.append((strToken, typToken, self.noLineas))
        
        mensaje = MENSAJES_ERROR.get(tipoError, "") if tipoError != ERR_NOERROR else ""
        return tipoError, strToken, mensaje
    
    def tipoCaracter(self, c):
        """Determina la columna en la matriz según el carácter - CORREGIDO"""
        if c == " ":
            return COL_ESPACIO
        elif c.isalpha() or c == '_':
            return COL_LETRAS
        elif c.isdigit():
            return COL_NUMEROS
        elif c == '.':
            return COL_PUNTO
        elif c in '()[]*/,:;':
            if c == '(':
                return COL_PAREN_ABRE
            elif c == ')':
                return COL_PAREN_CIERRA
            elif c == '[':
                return COL_UNITARIOS  # Usar COL_UNITARIOS para corchetes
            elif c == ']':
                return COL_UNITARIOS
            elif c == ',':
                return COL_COMA
            elif c == '*':
                return COL_UNITARIOS  # Usar COL_UNITARIOS para * y /
            elif c == '/':
                return COL_UNITARIOS
            return COL_UNITARIOS
        elif c == '=':
            return COL_IGUAL
        elif c == '>':
            return COL_MAYOR
        elif c == '<':
            return COL_MENOR
        elif c == '+':
            return COL_MAS
        elif c == '-':
            return COL_MENOS
        elif c == '"' or c == "'":
            return COL_COMILLAS
        elif c == '\n':
            return COL_EOLN
        elif c == '#':
            return COL_HASH
        elif c == '{':
            return COL_LLAVE_ABRIR
        elif c == '}':
            return COL_LLAVE_CERRAR
        elif c == '¿' or c == '?':
            return COL_INTERROGACION
        elif c == '|':
            return COL_PIPE
        elif c == "" or c == '\0':
            return COL_EOF
        else:
            return COL_OTROS
    
    def tipoToken(self, c):
        """Determina la línea inicial en la matriz según la columna - CORREGIDO"""
        tipos = {
            COL_ESPACIO: LIN_ESPACIO,
            COL_EOLN: LIN_EOLN,
            COL_EOF: LIN_EOF,
            COL_LETRAS: LIN_IDENTIFICADOR,
            COL_COMILLAS: LIN_CADENA,
            COL_NUMEROS: LIN_NUMERO,
            COL_UNITARIOS: LIN_SIMBOLO,  # *, /, [, ], etc.
            COL_MAS: LIN_MAS,
            COL_HASH: LIN_HASH,
            COL_MENOS: LIN_MENOS,
            COL_LLAVE_ABRIR: LIN_COMENTARIO,
            COL_PUNTO: LIN_PUNTO,
            COL_IGUAL: LIN_IGUAL,
            COL_MAYOR: LIN_MAYOR,
            COL_MENOR: LIN_MENOR,
            COL_INTERROGACION: LIN_INTERROGACION,
            COL_PIPE: LIN_PIPE,
            COL_PAREN_ABRE: LIN_PAREN_ABRE,
            COL_PAREN_CIERRA: LIN_PAREN_CIERRA,
            COL_COMA: LIN_COMA,
        }
        return tipos.get(c, LIN_SIN_TIPO)
    
    def getTipoTokenStr(self, tipo, valor):
        """Retorna descripción legible del tipo de token - MEJORADO"""
        descripciones = {
            LIN_ESPACIO: "ESPACIO",
            LIN_IDENTIFICADOR: f"IDENTIFICADOR [{valor.upper()}]",
            LIN_CADENA: "CADENA DE TEXTO",
            LIN_NUMERO: "NÚMERO",
            LIN_SIMBOLO: f"SÍMBOLO [{valor}]",
            LIN_MAS: "OPERADOR SUMA",
            LIN_HASH: "COMENTARIO",
            LIN_MENOS: "OPERADOR RESTA",
            LIN_COMENTARIO: "COMENTARIO LARGO",
            LIN_EOLN: "↵ FIN DE LÍNEA",
            LIN_EOF: " FIN DE ARCHIVO",
            LIN_SIN_TIPO: " SIN TIPO",
            LIN_PUNTO: "• PUNTO",
            LIN_IGUAL: "= OPERADOR IGUAL/COMPARACIÓN",
            LIN_MAYOR: "> OPERADOR MAYOR",
            LIN_MENOR: "< OPERADOR MENOR",
            LIN_INTERROGACION: "¿? PREGUNTA",
            LIN_PIPE: "|> PIPELINE",
            LIN_PAREN_ABRE: "( PARÉNTESIS ABRE",
            LIN_PAREN_CIERRA: ") PARÉNTESIS CIERRA",
            LIN_COMA: ", COMA",
        }
        
        if tipo >= RES_SEA and tipo <= RES_CONTIENE:
            return f" PALABRA RESERVADA [{valor}]"
        elif tipo >= RES_NUMERO and tipo <= RES_CONJUNTO:
            return f" TIPO DE DATO [{valor}]"
        elif tipo >= RES_SEGUNDOS and tipo <= RES_KILOMETROS:
            return f"⏱ UNIDAD [{valor}]"
        elif tipo in [RES_IMPRIMIR, RES_LEER]:
            return f" FUNCIÓN E/S [{valor}]"
        
        return descripciones.get(tipo, "No definido")
    
    def tipoIdentificador(self, identificador):
        """Determina si es identificador o palabra reservada"""
        for palabra, codigo in lstReservadas:
            if identificador == palabra:
                return codigo
        return LIN_IDENTIFICADOR
    
    def get(self):
        """Retorna la lista de tokens encontrados"""
        return self.lstTokens
    
    def getLineas(self):
        """Retorna el número total de líneas procesadas"""
        return self.noLineas
    
    def getEstadisticas(self):
        """Retorna estadísticas del análisis - MEJORADO"""
        stats = {
            'total_tokens': len(self.lstTokens),
            'lineas': self.noLineas,
            'identificadores': sum(1 for t in self.lstTokens if t[1] == LIN_IDENTIFICADOR),
            'palabras_reservadas': sum(1 for t in self.lstTokens if t[1] >= 3000 and t[1] < 5000),
            'numeros': sum(1 for t in self.lstTokens if t[1] == LIN_NUMERO),
            'cadenas': sum(1 for t in self.lstTokens if t[1] == LIN_CADENA),
            'operadores': sum(1 for t in self.lstTokens if t[1] in [LIN_MAS, LIN_MENOS, LIN_IGUAL]),
            'parentesis': sum(1 for t in self.lstTokens if t[1] in [LIN_PAREN_ABRE, LIN_PAREN_CIERRA]),
        }
        return stats

    def filtrar_tokens_utiles(self):
        """Filtra tokens que no son espacios ni saltos de línea"""
        return [token for token in self.lstTokens 
                if token[1] not in [LIN_ESPACIO, LIN_EOLN]]