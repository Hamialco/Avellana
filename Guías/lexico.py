"""
Lexico.py 

   v.2  ::  14.sept.2025
       clasificación de tokens identificador: identificadores y palabras reservadas
       Clasificación de tipos (ENTEROS, FLOTANTES, CADENAS)
       Clasificacion de constantes (ENTERAS, FLOTANTES, CADENAS)
       Clasificación de Símbolos
"""


matrizLexico = [
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, -1, 4, -1000, -1000, 4, 4, 4],
    [0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
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
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   #  <--- esta linea no sirve para nada
    [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	0,	0,	0],
    [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	0,	0],
    [0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1003,	0,	0,	0,	0,	0],
    [0,	0,	0,	-1003,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [0,	0,	0,	0,	0,	26,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [-1, -1, -1, -1,	-1,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [-1, -1, -1, -1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [0,	0,	0,	0,	0,	0,	29,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
    [-1,	-1,	-1,	-1,	-1,	30,	-1,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [-1,	-1,	-1,	-1,	-1,	33,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
    [-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1],
]

#---------------------- columnas
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

#-----------------------lineas 
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


#---------------------- reservadas
RES_SI = 3000
RES_FINSI = 3001
RES_SINO = 3002

RES_CICLO = 3003
RES_FINCI = 3004

RES_MIENTRAS = 3005
RES_FINMI = 3006

RES_DEF = 3007
RES_FINDEF = 3008

RES_SALIDA = 3012
RES_ENTRADA = 3013

RES_INICIO = 3014
RES_FINAL = 3015

#-------------------------- tipos
RES_ENTERO = 4000
RES_FLOTANTE = 4001
RES_CADENA = 4002



lstReservadas = (("si", RES_SI), ("finsi", RES_FINSI), ("sino", RES_SINO),
                ("ciclo", RES_CICLO), ("finci", RES_FINCI),
                ("mientras", RES_MIENTRAS), ("finmi", RES_FINMI),
                ("def", RES_DEF), ("findef", RES_FINDEF),
                ("entero", RES_ENTERO), ("flotante", RES_FLOTANTE), ("cadena", RES_CADENA),
                ("salida",RES_SALIDA), ("entrada", RES_ENTRADA),
                ("inicio", RES_INICIO), ("final", RES_FINAL))



#-------------------------- codigos de error (LEXICO)
ERR_NOERROR = 0
ERR_CADENA = -1000
ERR_NUMERO = -1001
ERR_COMENTANTARIO = -1002
ERR_CAR_INVALIDO = -1003



class Lexico :
    tiraCars = []    # todos los caracteres  separados, uno por posicion de la lista
    lstTokens = []    # lista de Tokens encontrados (tipo de token  /  valor lexico)
    noLineas = 0   # número de lineas procesadas / linea donde ocurre un error lexico
    
    
    
    
    def __init__(self, tChars) :
        self.tiraCars = []
        self.noLineas = 0
        self.lstTokens = []
        for c in tChars :
            self.tiraCars.append(c)

        
    def generaLexico(self, conComentarios) :   # regresa codigo de error y el token donde ocurrió
        # conComentarios = True : agrega los comentarios   False : elimina los comentarios
        self.noLineas = 0
        self.lstTokens = []
        
        tipoError = ERR_NOERROR
        strToken = ""
        typToken = LIN_SIN_TIPO
        iToken = 0
        
        
        
        while iToken < len(self.tiraCars) : 
            car = self.tiraCars[iToken]
            
            
            columna = self.tipoCaracter(car)
            if typToken == LIN_SIN_TIPO :
                typToken = self.tipoToken(columna)
                linea = typToken
            
            if matrizLexico[linea][columna] == -1000 :
                tipoError = ERR_CADENA
                break
            elif matrizLexico[linea][columna] == -1001 :
                tipoError = ERR_NUMERO
                break
            elif matrizLexico[linea][columna] == -1002 :
                tipoError = ERR_COMENTANTARIO
                break
            elif matrizLexico[linea][columna] == -1003 :
                strToken = car
                tipoError = ERR_CAR_INVALIDO
                break
            elif matrizLexico[linea][columna] > 0 :
                strToken = strToken + car
                linea = matrizLexico[linea][columna]
                iToken = iToken + 1
                
            elif matrizLexico[linea][columna] == -1  :
                if (typToken == LIN_IDENTIFICADOR) :
                    bR = self.tipoIdentificador(strToken.lower())
                    self.lstTokens.append((strToken.lower(), bR))
                elif typToken == LIN_NUMERO :
                    typToken = LIN_NUM_FLOTANTE if "." in strToken else LIN_NUM_ENTERO
                    self.lstTokens.append((strToken, typToken))
                elif (typToken == LIN_MAS or 
                  typToken == LIN_MENOS or typToken == LIN_IGUAL or 
                  typToken == LIN_MAYOR or typToken == LIN_MENOR) :
                    self.lstTokens.append((strToken, typToken))
                elif typToken == LIN_ESPACIO :
                    iToken = iToken + 1
                elif typToken == LIN_EOLN :
                    self.lstTokens.append(("[EOLN]", typToken))
                    self.noLineas = self.noLineas + 1 
                    iToken = iToken + 1
                elif typToken in (LIN_COMENTARIO, LIN_HASH) :
                    strToken = strToken + car
                    iToken = iToken + 1
                    
                    if conComentarios :
                        self.lstTokens.append((strToken, typToken))
                        
                else :
                    strToken = strToken + car
                    iToken = iToken + 1
                    self.lstTokens.append((strToken, typToken))

                strToken = ""
                typToken = LIN_SIN_TIPO
            
        self.lstTokens.append(("[EOF]", LIN_EOF))                
        return tipoError, strToken
    
    def tipoCaracter(self, c) :  # regresa la columna dentro de la Matriz
        car = ""
        if c == " " : 
             car = COL_ESPACIO
        elif (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c == '_') :
            car = COL_LETRAS
        elif (c >= '0' and c <= '9') :
            car = COL_NUMEROS 
        elif c == '.' :
            car = COL_PUNTO 
        elif c in '()[]*/,' :
            car = COL_UNITARIOS 
        elif c == '=' :
            car = COL_IGUAL 
        elif c == '>' :
            car = COL_MAYOR 
        elif c == '<' :
            car = COL_MENOR 
        elif c == '+' :
            car = COL_MAS 
        elif c == '-' :
            car = COL_MENOS 
        elif c == '"' :
            car = COL_COMILLAS
        elif c == '\n' :
            car = COL_EOLN 
        elif c == '#' : 
            car = COL_HASH 
        elif c == '{' :
            car = COL_LLAVE_ABRIR 
        elif c == '}' :
            car = COL_LLAVE_CERRAR
        elif c == "" :
            car = COL_EOF 
        else :
            car = COL_OTROS 

        return car
    
    
    def tipoToken(self, c) :  # regresa la Linea dentro de la matriz
        tipoTok = -1
  
        if c == COL_ESPACIO :      
            tipoTok = LIN_ESPACIO 
        elif c == COL_EOLN :
            tipoTok = LIN_EOLN
        elif c == COL_EOF :
            tipoTok = LIN_EOF
        elif c == COL_LETRAS :
            tipoTok = LIN_IDENTIFICADOR 
        elif c == COL_COMILLAS :
            tipoTok = LIN_CADENA
        elif c == COL_NUMEROS :
            tipoTok = LIN_NUMERO 
        elif c == COL_UNITARIOS :
            tipoTok = LIN_SIMBOLO
        elif c == COL_MAS :
            tipoTok = LIN_MAS 
        elif c == COL_HASH :
            tipoTok = LIN_HASH 
        elif c == COL_MENOS :
            tipoTok = LIN_MENOS
        elif c == COL_LLAVE_ABRIR :
            tipoTok = LIN_COMENTARIO 
        elif c == COL_PUNTO :
            tipoTok = LIN_PUNTO
        elif c == COL_IGUAL :
            tipoTok = LIN_IGUAL
        elif c == COL_MAYOR :
            tipoTok = LIN_MAYOR
        elif c == COL_MENOR :
            tipoTok = LIN_MENOR
        else :
            tipoTok = LIN_SIN_TIPO
    
        return tipoTok
    
    def getTipoTokenStr(self, t, tt) :
        sT = "No definido"
        
        if t == LIN_ESPACIO :
            sT = "ESPACIO"
        elif t == LIN_IDENTIFICADOR :
            sT = f"IDENTIFICADOR [{tt.upper()}]"    # Identificador ó palabra reservada ??
        elif t == LIN_CADENA :
            sT = "CONSTANTE CADENA"
        elif t == LIN_NUMERO :
            sT = "CONSTANTE NUMERO"   #  Número Entero ó Flotante ??
        elif t == LIN_SIMBOLO :
            sT = "SIMBOLO"   # (  )  [  ]  *  /    ,
        elif t == LIN_MAS :
            sT = "OPERADOR SUMA"   # +   ++
        elif t == LIN_HASH :
            sT = "COMENTARIO CORTO"
        elif t == LIN_MENOS :
            sT = "OPERADOR RESTA"
        elif t == LIN_COMENTARIO :
            sT = "COMENTARIO LARGO"
        elif t == LIN_EOLN :
            sT = "FIN DE LINEA"
        elif t == LIN_EOF :
            sT = "FIN DE ARCHIVO"
        elif t == LIN_SIN_TIPO :
            sT = "SIN TIPO DEFINIDO"
        elif t == LIN_PUNTO :
            sT = "PUNTO"
        elif t == LIN_IGUAL :
            sT = "OPERADOR IGUAL"   #  =   ==
        elif t == LIN_MAYOR :
            sT = "OPERADOR MAYOR"  #  >   >=  
        elif t == LIN_MENOR :
            sT = "OPERADOR MENOR"  #  <   <=   <>
        elif t >= RES_SI and t <= RES_FINAL :
            sT = f"PALABRA RESERVADA [{tt}]"
        elif t >= RES_ENTERO and t <= RES_CADENA : 
            sT = f"TIPO DE DATO [{tt}]"
        elif t == LIN_NUM_ENTERO :
            sT = "CONSTANTE NUMERO ENTERO"
        elif t == LIN_NUM_FLOTANTE :
            sT = "CONSTANTE NUMERO FLOTANTE"
            
        return sT        
        
    
    def tipoIdentificador(self, id) :   
        pRes = LIN_IDENTIFICADOR
        for p in lstReservadas :
            if id == p[0] :
                pRes = p[1]
                break
            
        return pRes


    def get(self) :  # regresa la lista de tokens (y su tipo) encontrados
        return self.lstTokens
    
    def getLineas(self) :    # regresa número total de lineas revisadas
        return self.noLineas
    
    def mensajeError(self, err) :
        s = ""
        if ERR_NOERROR == err :
            s = "NO se encontraron errores de LEXICO"
        elif ERR_CADENA == err :
            s = "Cadena con errores"
        elif ERR_NUMERO == err :
            s = "Numero mal construido"
        elif ERR_COMENTANTARIO == err :
            s = "Comentario mal cerrado"
        elif ERR_CAR_INVALIDO == err :
            s = "Token inválido"

        return s
        