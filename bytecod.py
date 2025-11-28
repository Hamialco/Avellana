"""
Generador de Bytecode
"""

from lexico import Tipos


class Instrucciones:
    
    PUSH = 0
    POP = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    STORE = 6
    LOAD = 7
    PRINT = 8
    READ = 9
    JMP = 10
    JMPZ = 11
    JMPNZ = 12
    CALL = 13
    RET = 14
    HALT = 15
    
    EQ = 16
    NEQ = 17
    GT = 18
    LT = 19
    GTE = 20
    LTE = 21
    
    RETVAL = 22
    
    STORE_ARR = 23
    LOAD_ARR = 24
    ARR_SIZE = 25
    
    DUP = 26
    SWAP = 27
    
    AND = 28
    OR = 29
    NOT = 30
    
    @classmethod
    def obtener_nombre(cls, codigo_instruccion):
        nombres = {
            cls.PUSH: "PUSH",
            cls.POP: "POP",
            cls.ADD: "ADD",
            cls.SUB: "SUB",
            cls.MUL: "MUL",
            cls.DIV: "DIV",
            cls.STORE: "STORE",
            cls.LOAD: "LOAD",
            cls.PRINT: "PRINT",
            cls.READ: "READ",
            cls.JMP: "JMP",
            cls.JMPZ: "JMPZ",
            cls.JMPNZ: "JMPNZ",
            cls.CALL: "CALL",
            cls.RET: "RET",
            cls.HALT: "HALT",
            cls.EQ: "EQ",
            cls.NEQ: "NEQ",
            cls.GT: "GT",
            cls.LT: "LT",
            cls.GTE: "GTE",
            cls.LTE: "LTE",
            cls.RETVAL: "RETVAL",
            cls.STORE_ARR: "STORE_ARR",
            cls.LOAD_ARR: "LOAD_ARR",
            cls.ARR_SIZE: "ARR_SIZE",
            cls.DUP: "DUP",
            cls.SWAP: "SWAP",
            cls.AND: "AND",
            cls.OR: "OR",
            cls.NOT: "NOT",
        }
        return nombres.get(codigo_instruccion, f"UNKNOWN_{codigo_instruccion}")

class GeneradorBytecode:
    
    def __init__(self):
        self.codigo = []
        self.etiquetas = {}
        self.contador_etiquetas = 0
        self.tabla_variables = {}
        self.contador_temporales = 0
        self.instrucciones = Instrucciones
        
    
    def generar_bytecode(self, arbol_sintactico, tabla_simbolos):
        self.codigo = []
        self.tabla_simbolos = tabla_simbolos
        self.contador_etiquetas = 0
        self.contador_temporales = 0
        
        try:
            self._generar_codigo(arbol_sintactico)
            self._agregar_instruccion_final()
            return self.codigo
            
        except Exception as e:
            self.codigo = []
            self._agregar_instruccion(self.instrucciones.PUSH, f"Error: {str(e)}")
            self._agregar_instruccion(self.instrucciones.PRINT)
            self._agregar_instruccion(self.instrucciones.HALT)
            return self.codigo
    
    def _generar_codigo(self, nodo):
        if not isinstance(nodo, dict):
            return
            
        tipo_nodo = nodo.get('tipo', 'desconocido')
        
        if tipo_nodo == 'programa':
            self._generar_codigo_programa(nodo)
        elif tipo_nodo == 'declaracion':
            self._generar_codigo_declaracion(nodo)
        elif tipo_nodo == 'asignacion':
            self._generar_codigo_asignacion(nodo)
        elif tipo_nodo == 'imprimir':
            self._generar_codigo_imprimir(nodo)
        elif tipo_nodo == 'leer':
            self._generar_codigo_leer(nodo)
        elif tipo_nodo == 'declaracion_arreglo':
            self._generar_codigo_declaracion_arreglo(nodo)
        elif tipo_nodo == 'acceso_arreglo':
            self._generar_codigo_acceso_arreglo(nodo)
        elif tipo_nodo == 'asignacion_arreglo':
            self._generar_codigo_asignacion_arreglo(nodo)
        elif tipo_nodo == 'leer_arreglo':
            self._generar_codigo_leer_arreglo(nodo)
        elif tipo_nodo == 'si':
            self._generar_codigo_si(nodo)
        elif tipo_nodo == 'mientras':
            self._generar_codigo_mientras(nodo)
        elif tipo_nodo == 'para':
            self._generar_codigo_para(nodo)
        elif tipo_nodo == 'definicion_funcion':
            self._generar_codigo_funcion(nodo)
        elif tipo_nodo == 'llamada_funcion':
            self._generar_codigo_llamada_funcion(nodo)
        elif tipo_nodo == 'retornar':
            self._generar_codigo_retornar(nodo)
        else:
            self._generar_codigo_error(f"Nodo desconocido: {tipo_nodo}")
    
    def _generar_codigo_programa(self, nodo):
        # Primero: generar todas las definiciones de funciones
        definiciones_funciones = []
        instrucciones_principales = []
        
        for instruccion in nodo.get('instrucciones', []):
            if instruccion.get('tipo') == 'definicion_funcion':
                definiciones_funciones.append(instruccion)
            else:
                instrucciones_principales.append(instruccion)
        
        # Saltar sobre las definiciones de funciones
        etiqueta_inicio = self._generar_etiqueta()
        self._agregar_instruccion(self.instrucciones.JMP, etiqueta_inicio)
        
        # Generar código de las funciones
        for funcion in definiciones_funciones:
            self._generar_codigo(funcion)
        
        # Etiqueta de inicio del programa principal
        self._agregar_etiqueta(etiqueta_inicio)
        
        # Generar código del programa principal
        for instruccion in instrucciones_principales:
            self._generar_codigo(instruccion)
    
    def _generar_codigo_declaracion(self, nodo):
        nombre_variable = nodo.get('variable')
        tipo_dato = nodo.get('tipo_dato')
        valor_inicial = nodo.get('valor')
        
        if valor_inicial:
            self._generar_expresion(valor_inicial)
            self._agregar_instruccion(self.instrucciones.STORE, nombre_variable)
        else:
            valor_por_defecto = self._obtener_valor_por_defecto(tipo_dato)
            self._agregar_instruccion(self.instrucciones.PUSH, valor_por_defecto)
            self._agregar_instruccion(self.instrucciones.STORE, nombre_variable)
    
    def _generar_codigo_asignacion(self, nodo):
        nombre_variable = nodo.get('variable')
        expresion = nodo.get('expresion')
        
        self._generar_expresion(expresion)
        self._agregar_instruccion(self.instrucciones.STORE, nombre_variable)
    
    def _generar_codigo_imprimir(self, nodo):
        expresion = nodo.get('expresion')
        
        if expresion:
            self._generar_expresion(expresion)
        else:
            self._agregar_instruccion(self.instrucciones.PUSH, "")
            
        self._agregar_instruccion(self.instrucciones.PRINT)
    
    def _generar_codigo_leer(self, nodo):
        nombre_variable = nodo.get('variable')
        self._agregar_instruccion(self.instrucciones.READ, nombre_variable)
    
    def _generar_codigo_declaracion_arreglo(self, nodo):
        nombre_arreglo = nodo.get('nombre')
        tipo_elemento = nodo.get('tipo_elemento')
        tamanio = nodo.get('tamanio', 0)
        
        # Inicializar arreglo con valores por defecto
        valor_por_defecto = self._obtener_valor_por_defecto(tipo_elemento)
        
        for indice in range(tamanio):
            self._agregar_instruccion(self.instrucciones.PUSH, indice)
            self._agregar_instruccion(self.instrucciones.PUSH, valor_por_defecto)
            self._agregar_instruccion(self.instrucciones.STORE_ARR, nombre_arreglo)

    def _generar_expresion_acceso_arreglo(self, expresion):
        nombre_arreglo = expresion.get('nombre')
        indice = expresion.get('indice')
        
        self._generar_expresion(indice)
        self._agregar_instruccion(self.instrucciones.LOAD_ARR, nombre_arreglo)

    def _generar_codigo_asignacion_arreglo(self, nodo):
        nombre_arreglo = nodo.get('nombre')
        indice = nodo.get('indice')
        valor = nodo.get('valor')
        
        self._generar_expresion(indice)  # Índice en pila
        self._generar_expresion(valor)   # Valor en pila
        self._agregar_instruccion(self.instrucciones.STORE_ARR, nombre_arreglo)

    def _generar_codigo_leer_arreglo(self, nodo):
        nombre_arreglo = nodo.get('arreglo')
        indice = nodo.get('indice')
        
        # Generar código para el índice
        self._generar_expresion(indice)
        
        # Leer a una variable temporal
        variable_temporal = f"{nombre_arreglo}"
        self._agregar_instruccion(self.instrucciones.READ, variable_temporal)
        
        # Cargar índice nuevamente y almacenar en el arreglo
        self._generar_expresion(indice)
        self._agregar_instruccion(self.instrucciones.LOAD, variable_temporal)
        self._agregar_instruccion(self.instrucciones.STORE_ARR, nombre_arreglo)
    
    def _generar_codigo_si(self, nodo):
        condicion = nodo.get('condicion')
        cuerpo = nodo.get('cuerpo', [])
        cuerpo_sino = nodo.get('sino', [])
        
        # Generar código para la condición
        self._generar_expresion(condicion)
        
        etiqueta_sino = self._generar_etiqueta()
        etiqueta_fin = self._generar_etiqueta()
        
        # Saltar a 'sino' si la condición es falsa (0)
        self._agregar_instruccion(self.instrucciones.JMPZ, etiqueta_sino)
        
        # Código para el bloque 'si' (condición verdadera)
        for instruccion in cuerpo:
            self._generar_codigo(instruccion)
        
        # SIEMPRE saltar al final después del bloque 'si'
        self._agregar_instruccion(self.instrucciones.JMP, etiqueta_fin)
        
        # Etiqueta para el bloque 'sino'
        self._agregar_etiqueta(etiqueta_sino)
        
        # Código para el bloque 'sino' (condición falsa)
        for instruccion in cuerpo_sino:
            self._generar_codigo(instruccion)
        
        # Etiqueta de fin
        self._agregar_etiqueta(etiqueta_fin)

    def _generar_codigo_mientras(self, nodo):
        condicion = nodo.get('condicion')
        cuerpo = nodo.get('cuerpo', [])
        
        etiqueta_inicio = self._generar_etiqueta()
        etiqueta_fin = self._generar_etiqueta()
        
        # Etiqueta de inicio del bucle
        self._agregar_etiqueta(etiqueta_inicio)
        
        # Evaluar condición
        self._generar_expresion(condicion)
        self._agregar_instruccion(self.instrucciones.JMPZ, etiqueta_fin)
        
        # Cuerpo del bucle
        for instruccion in cuerpo:
            self._generar_codigo(instruccion)
        
        # Volver al inicio para reevaluar condición
        self._agregar_instruccion(self.instrucciones.JMP, etiqueta_inicio)
        
        # Etiqueta de fin del bucle
        self._agregar_etiqueta(etiqueta_fin)

    def _generar_codigo_para(self, nodo):
        variable = nodo.get('variable')
        inicio = nodo.get('inicio')
        condicion = nodo.get('condicion')
        incremento = nodo.get('incremento')
        cuerpo = nodo.get('cuerpo', [])  # ¡Esto es importante!
        
        # Generar código de inicialización
        if inicio:
            self._generar_expresion(inicio)
            self._agregar_instruccion(self.instrucciones.STORE, variable)
        
        etiqueta_inicio = self._generar_etiqueta()
        etiqueta_fin = self._generar_etiqueta()
        
        # Etiqueta de inicio del bucle
        self._agregar_etiqueta(etiqueta_inicio)
        
        # Evaluar condición
        self._generar_expresion(condicion)
        self._agregar_instruccion(self.instrucciones.JMPZ, etiqueta_fin)
        
        # Cuerpo del bucle (¡esto estaba faltando!)
        for instruccion in cuerpo:
            self._generar_codigo(instruccion)
        
        # Incremento
        if incremento:
            self._generar_codigo(incremento)
        else:
            # Incremento por defecto: i = i + 1
            self._agregar_instruccion(self.instrucciones.LOAD, variable)
            self._agregar_instruccion(self.instrucciones.PUSH, 1)
            self._agregar_instruccion(self.instrucciones.ADD)
            self._agregar_instruccion(self.instrucciones.STORE, variable)
        
        # Volver al inicio
        self._agregar_instruccion(self.instrucciones.JMP, etiqueta_inicio)
        
        # Etiqueta de fin del bucle
        self._agregar_etiqueta(etiqueta_fin)
    
    def _generar_codigo_funcion(self, nodo):
        nombre_funcion = nodo.get('nombre')
        parametros = nodo.get('parametros', [])
        cuerpo = nodo.get('cuerpo', [])
        
        etiqueta_funcion = f"func_{nombre_funcion}"
        self._agregar_etiqueta(etiqueta_funcion)
        
        # Procesar parámetros
        for param in parametros:
            self._agregar_instruccion(self.instrucciones.STORE, param['nombre'])
        
        # Generar el cuerpo de la función
        for instruccion in cuerpo:
            self._generar_codigo(instruccion)
        
        # VERIFICAR: Si la última instrucción no es RET, agregarlo
        tiene_ret_explicito = any(
            isinstance(inst, dict) and inst.get('tipo') == 'retornar'
            for inst in cuerpo
        )
        
        if not tiene_ret_explicito:
            self._agregar_instruccion(self.instrucciones.RET)
    
    def _generar_codigo_llamada_funcion(self, nodo):
        nombre_funcion = nodo.get('nombre')
        argumentos = nodo.get('argumentos', [])
        
        for argumento in reversed(argumentos):
            self._generar_expresion(argumento)
        
        etiqueta_retorno = self._generar_etiqueta()
        self._agregar_instruccion(self.instrucciones.PUSH, etiqueta_retorno)
        self._agregar_instruccion(self.instrucciones.CALL, f"func_{nombre_funcion}")
        
        self._agregar_etiqueta(etiqueta_retorno)
    
    def _generar_codigo_retornar(self, nodo):
        expresion = nodo.get('expresion')
        
        if expresion is not None:
            self._generar_expresion(expresion)
            self._agregar_instruccion(self.instrucciones.RETVAL)
        else:
            self._agregar_instruccion(self.instrucciones.RET)
    
    def _generar_codigo_error(self, mensaje):
        self._agregar_instruccion(self.instrucciones.PUSH, f"ERROR: {mensaje}")
        self._agregar_instruccion(self.instrucciones.PRINT)
        self._agregar_instruccion(self.instrucciones.HALT)
    
    
    def _generar_expresion(self, expresion):
        if not isinstance(expresion, dict):
            return
            
        tipo_expresion = expresion.get('tipo', 'desconocido')
        
        if tipo_expresion == 'literal':
            self._generar_expresion_literal(expresion)
        elif tipo_expresion == 'variable':
            self._generar_expresion_variable(expresion)
        elif tipo_expresion == 'binaria':
            self._generar_expresion_binaria(expresion)
        elif tipo_expresion == 'unaria':
            self._generar_expresion_unaria(expresion)
        elif tipo_expresion == 'acceso_arreglo':
            self._generar_expresion_acceso_arreglo(expresion)
        elif tipo_expresion == 'llamada_funcion':
            self._generar_expresion_llamada_funcion(expresion)
        elif tipo_expresion == 'error':  # AGREGAR ESTE MANEJO
            # Para expresiones con error, generar un valor por defecto
            self._agregar_instruccion(self.instrucciones.PUSH, 0)
        else:
            # En lugar de error, generar valor por defecto
            self._agregar_instruccion(self.instrucciones.PUSH, 0)
    
    def _generar_expresion_literal(self, expresion):
        valor = expresion.get('valor')
        tipo_dato = expresion.get('tipo_dato')
        
        valor_convertido = self._convertir_valor_literal(valor, tipo_dato)
        self._agregar_instruccion(self.instrucciones.PUSH, valor_convertido)
    
    def _generar_expresion_variable(self, expresion):
        nombre_variable = expresion.get('nombre')
        self._agregar_instruccion(self.instrucciones.LOAD, nombre_variable)
    
    def _generar_expresion_binaria(self, expresion):
        izquierda = expresion.get('izquierda')
        derecha = expresion.get('derecha')
        operador = expresion.get('operador')
        
        self._generar_expresion(izquierda)
        self._generar_expresion(derecha)
        
        mapeo_operadores = {
            '+': self.instrucciones.ADD,
            '-': self.instrucciones.SUB,
            '*': self.instrucciones.MUL,
            '/': self.instrucciones.DIV,
            '==': self.instrucciones.EQ,
            '<>': self.instrucciones.NEQ,
            '>': self.instrucciones.GT,
            '<': self.instrucciones.LT,
            '>=': self.instrucciones.GTE,
            '<=': self.instrucciones.LTE,
            '&&': self.instrucciones.AND,
            '||': self.instrucciones.OR,
        }
        
        instruccion_operador = mapeo_operadores.get(operador)
        if instruccion_operador:
            self._agregar_instruccion(instruccion_operador)
        else:
            self._generar_codigo_error(f"Operador desconocido: {operador}")
    
    def _generar_expresion_unaria(self, expresion):
        operador = expresion.get('operador')
        expresion_interna = expresion.get('expresion')
        
        self._generar_expresion(expresion_interna)
        
        if operador == '!':
            self._agregar_instruccion(self.instrucciones.NOT)
        else:
            self._generar_codigo_error(f"Operador unario desconocido: {operador}")
    
    def _generar_expresion_acceso_arreglo(self, expresion):
        nombre_arreglo = expresion.get('nombre')
        indice = expresion.get('indice')
        
        self._generar_expresion(indice)
        
        self._agregar_instruccion(self.instrucciones.LOAD_ARR, nombre_arreglo)
    
    def _generar_expresion_llamada_funcion(self, expresion):
        self._generar_codigo_llamada_funcion(expresion)
    
    
    def _agregar_instruccion(self, instruccion, operando=None):
        if operando is not None:
            self.codigo.append((instruccion, operando))
        else:
            self.codigo.append((instruccion,))
    
    def _agregar_etiqueta(self, etiqueta):
        self.codigo.append((f"{etiqueta}:",))
        self.etiquetas[etiqueta] = len(self.codigo) - 1
    
    def _generar_etiqueta(self):
        etiqueta = f"L{self.contador_etiquetas}"
        self.contador_etiquetas += 1
        return etiqueta
    
    def _agregar_instruccion_final(self):
        tiene_halt = any(
            isinstance(inst, tuple) and len(inst) > 0 and inst[0] == self.instrucciones.HALT
            for inst in self.codigo
        )
        
        if not tiene_halt:
            self._agregar_instruccion(self.instrucciones.HALT)
    
    def _obtener_valor_por_defecto(self, tipo_dato):
        if tipo_dato in [Tipos.LEX_ENTERO, Tipos.ENTERO]:
            return 0
        elif tipo_dato in [Tipos.LEX_FLOTANTE, Tipos.FLOTANTE]:
            return 0.0
        elif tipo_dato in [Tipos.LEX_CADENA, Tipos.CADENA]:
            return ""
        elif tipo_dato in [Tipos.LEX_BOOLEANO, Tipos.BOOLEANO]:
            return False
        elif tipo_dato == Tipos.LEX_VERDADERO:
            return True
        elif tipo_dato == Tipos.LEX_FALSO:
            return False
        else:
            return 0
    
    def _convertir_valor_literal(self, valor, tipo_dato):
        if tipo_dato in [Tipos.ENTERO, Tipos.LEX_ENTERO, Tipos.LIN_NUM_ENTERO]:
            return int(valor)
        elif tipo_dato in [Tipos.FLOTANTE, Tipos.LEX_FLOTANTE, Tipos.LIN_NUM_FLOTANTE]:
            return float(valor)
        elif tipo_dato in [Tipos.CADENA, Tipos.LEX_CADENA, Tipos.LIN_CADENA]:
            return str(valor).strip('"')
        elif tipo_dato in [Tipos.BOOLEANO, Tipos.LEX_BOOLEANO]:
            if isinstance(valor, str):
                return valor.lower() == 'verdadero'
            else:
                return bool(valor)
        else:
            return valor
    
    
    def mostrar_bytecode(self):
        lineas = []
        
        for instruccion in self.codigo:
            if isinstance(instruccion[0], str) and instruccion[0].endswith(':'):
                lineas.append(instruccion[0])
            else:
                codigo_inst = instruccion[0]
                nombre_inst = Instrucciones.obtener_nombre(codigo_inst)
                
                if len(instruccion) > 1:
                    operando = instruccion[1]
                    if isinstance(operando, str) and not operando.startswith('L'):
                        operando_formateado = f'"{operando}"'
                    else:
                        operando_formateado = str(operando)
                    lineas.append(f"  {nombre_inst} {operando_formateado}")
                else:
                    lineas.append(f"  {nombre_inst}")
        
        return "\n".join(lineas)
    
    def obtener_codigo(self):
        return self.codigo
    
    def limpiar(self):
        self.codigo = []
        self.etiquetas = {}
        self.contador_etiquetas = 0
        self.contador_temporales = 0


class ByteCodeGenerator(GeneradorBytecode):
    
    def __init__(self):
        super().__init__()
        self.INSTRUCCIONES = {
            'PUSH': Instrucciones.PUSH,
            'POP': Instrucciones.POP,
            'ADD': Instrucciones.ADD,
            'SUB': Instrucciones.SUB,
            'MUL': Instrucciones.MUL,
            'DIV': Instrucciones.DIV,
            'STORE': Instrucciones.STORE,
            'LOAD': Instrucciones.LOAD,
            'PRINT': Instrucciones.PRINT,
            'READ': Instrucciones.READ,
            'JMP': Instrucciones.JMP,
            'JMPZ': Instrucciones.JMPZ,
            'JMPNZ': Instrucciones.JMPNZ,
            'CALL': Instrucciones.CALL,
            'RET': Instrucciones.RET,
            'HALT': Instrucciones.HALT,
            'EQ': Instrucciones.EQ,
            'NEQ': Instrucciones.NEQ,
            'GT': Instrucciones.GT,
            'LT': Instrucciones.LT,
            'GTE': Instrucciones.GTE,
            'LTE': Instrucciones.LTE,
            'RETVAL': Instrucciones.RETVAL,
            'STORE_ARR': Instrucciones.STORE_ARR,
            'LOAD_ARR': Instrucciones.LOAD_ARR,
            'ARR_SIZE': Instrucciones.ARR_SIZE,
            'DUP': Instrucciones.DUP,
            'SWAP': Instrucciones.SWAP,
            'AND': Instrucciones.AND,
            'OR': Instrucciones.OR,
            'NOT': Instrucciones.NOT,
        }
    
    def generar_bytecode(self, arbol_sintactico, tabla_simbolos):
        return super().generar_bytecode(arbol_sintactico, tabla_simbolos)
    
    def get_codigo(self):
        return self.obtener_codigo()
    
    def nueva_etiqueta(self):
        return self._generar_etiqueta()


INSTRUCCIONES = Instrucciones


def obtener_nombre_instruccion(codigo_instruccion):
    return Instrucciones.obtener_nombre(codigo_instruccion)