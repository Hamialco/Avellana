"""
bytecode
"""
from avllexico import *
class ByteCodeGenerator:
    def __init__(self):
        self.codigo = []
        self.etiquetas = {}
        self.contador_etiquetas = 0
        self.tabla_variables = {}
        self.contador_temporales = 0
        
    INSTRUCCIONES = {
        'PUSH': 0,      # PUSH valor
        'POP': 1,       # POP
        'ADD': 2,       # ADD
        'SUB': 3,       # SUB
        'MUL': 4,       # MUL
        'DIV': 5,       # DIV
        'STORE': 6,     # STORE nombre_variable
        'LOAD': 7,      # LOAD nombre_variable
        'PRINT': 8,     # PRINT
        'READ': 9,      # READ nombre_variable
        'JMP': 10,      # JMP etiqueta
        'JMPZ': 11,     # JMPZ etiqueta (salta si cero)
        'JMPNZ': 12,    # JMPNZ etiqueta (salta si no cero)
        'CALL': 13,     # CALL nombre_funcion
        'RET': 14,      # RET
        'HALT': 15,     # HALT
        'EQ': 16,       # EQ (igual)
        'NEQ': 17,      # NEQ (no igual)
        'GT': 18,       # GT (mayor que)
        'LT': 19,       # LT (menor que)
        'GTE': 20,      # GTE (mayor o igual)
        'LTE': 21,       # LTE (menor o igual)
        'RETVAL': 22,    # RETVAL (retornar valor)
        'STORE_ARR': 23,    # STORE_ARR nombre indice (almacena en arreglo)
        'LOAD_ARR': 24,     # LOAD_ARR nombre indice (carga desde arreglo)
        'ARR_SIZE': 25,     # ARR_SIZE nombre (obtiene tamaño)
    }

    def _generar_codigo_acceso_arreglo(self, nodo):
        """Genera bytecode para acceso a arreglo"""
        # Cargar índice
        self._generar_expresion(nodo['indice'])
        
        if nodo['tipo'] == 'acceso_arreglo':
            # Cargar elemento del arreglo
            self.codigo.append((self.INSTRUCCIONES['LOAD_ARR'], nodo['nombre']))
        elif nodo['tipo'] == 'asignacion_arreglo':
            # Generar valor a asignar
            self._generar_expresion(nodo['valor'])
            # Almacenar en arreglo
            self.codigo.append((self.INSTRUCCIONES['STORE_ARR'], nodo['nombre']))

    def _generar_codigo_declaracion_arreglo(self, nodo):
        """Genera bytecode para declaración de arreglo"""
        # Inicializar arreglo con valores por defecto
        for i in range(nodo['tamanio']):
            # Push índice
            self.codigo.append((self.INSTRUCCIONES['PUSH'], i))
            
            # Push valor por defecto según tipo
            if nodo['tipo_elemento'] == RES_ENTERO:
                self.codigo.append((self.INSTRUCCIONES['PUSH'], 0))
            elif nodo['tipo_elemento'] == RES_FLOTANTE:
                self.codigo.append((self.INSTRUCCIONES['PUSH'], 0.0))
            elif nodo['tipo_elemento'] == RES_CADENA:
                self.codigo.append((self.INSTRUCCIONES['PUSH'], ""))
            elif nodo['tipo_elemento'] == RES_BOOLEANO:
                self.codigo.append((self.INSTRUCCIONES['PUSH'], 0))
                
            # Almacenar en arreglo
            self.codigo.append((self.INSTRUCCIONES['STORE_ARR'], nodo['nombre']))

    def generar_bytecode(self, arbol_sintactico, tabla_simbolos):
        """Genera byte-code real a partir del árbol sintáctico"""
        self.codigo = []
        self.tabla_simbolos = tabla_simbolos
        self._generar_codigo(arbol_sintactico)
        self.codigo.append((self.INSTRUCCIONES['HALT'],))
        return self.codigo
    
    def _generar_codigo(self, nodo):
        """Método recursivo para generar código"""
        if isinstance(nodo, dict):
            if nodo['tipo'] == 'programa':
                for instruccion in nodo.get('instrucciones', []):
                    self._generar_codigo(instruccion)
                    
            elif nodo['tipo'] == 'declaracion':
                # Reservar espacio para la variable
                var_name = nodo['variable']
                if 'valor' in nodo:
                    self._generar_expresion(nodo['valor'])
                    self.codigo.append((self.INSTRUCCIONES['STORE'], var_name))
                else:
                    # Inicializar con valor por defecto
                    if nodo['tipo_dato'] == RES_ENTERO:
                        self.codigo.append((self.INSTRUCCIONES['PUSH'], 0))
                    elif nodo['tipo_dato'] == RES_FLOTANTE:
                        self.codigo.append((self.INSTRUCCIONES['PUSH'], 0.0))
                    elif nodo['tipo_dato'] == RES_CADENA:
                        self.codigo.append((self.INSTRUCCIONES['PUSH'], ""))
                    self.codigo.append((self.INSTRUCCIONES['STORE'], var_name))
                    
            elif nodo['tipo'] == 'asignacion':
                self._generar_expresion(nodo['expresion'])
                self.codigo.append((self.INSTRUCCIONES['STORE'], nodo['variable']))
                
            elif nodo['tipo'] == 'imprimir':
                self._generar_expresion(nodo['expresion'])
                self.codigo.append((self.INSTRUCCIONES['PRINT'],))
                
            elif nodo['tipo'] == 'leer':
                self._generar_codigo_entrada(nodo)
                
            elif nodo['tipo'] == 'si':
                self._generar_condicion(nodo['condicion'])
                etiqueta_fin = self.nueva_etiqueta()
                etiqueta_sino = self.nueva_etiqueta() if 'sino' in nodo else etiqueta_fin
                
                # Saltar a sino si la condición es falsa
                self.codigo.append((self.INSTRUCCIONES['JMPZ'], etiqueta_sino))
                
                # Cuerpo del si
                for instruccion in nodo['cuerpo']:
                    self._generar_codigo(instruccion)
                    
                if 'sino' in nodo:
                    self.codigo.append((self.INSTRUCCIONES['JMP'], etiqueta_fin))
                    self.codigo.append((etiqueta_sino + ':',))
                    
                    # Cuerpo del sino
                    for instruccion in nodo['sino']:
                        self._generar_codigo(instruccion)
                        
                self.codigo.append((etiqueta_fin + ':',))
                
            elif nodo['tipo'] == 'mientras':
                etiqueta_inicio = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                
                self.codigo.append((etiqueta_inicio + ':',))
                self._generar_condicion(nodo['condicion'])
                self.codigo.append((self.INSTRUCCIONES['JMPZ'], etiqueta_fin))
                
                # Cuerpo del mientras
                for instruccion in nodo['cuerpo']:
                    self._generar_codigo(instruccion)
                    
                self.codigo.append((self.INSTRUCCIONES['JMP'], etiqueta_inicio))
                self.codigo.append((etiqueta_fin + ':',))
                
            elif nodo['tipo'] == 'para':
                # Inicialización
                if 'inicio' in nodo:
                    self._generar_expresion(nodo['inicio'])
                    self.codigo.append((self.INSTRUCCIONES['STORE'], nodo['variable']))
                    
                etiqueta_inicio = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                
                self.codigo.append((etiqueta_inicio + ':',))
                
                # Cuerpo del para
                if 'condicion' in nodo:
                    self._generar_condicion(nodo['condicion'])
                    self.codigo.append((self.INSTRUCCIONES['JMPZ'], etiqueta_fin))

                for instruccion in nodo['cuerpo']:
                    self._generar_codigo(instruccion)

                if 'incremento' in nodo:
                    self._generar_codigo(nodo['incremento'])
                    
                # Incremento (simulado)
                self.codigo.append((self.INSTRUCCIONES['LOAD'], nodo['variable']))
                self.codigo.append((self.INSTRUCCIONES['PUSH'], 1))
                self.codigo.append((self.INSTRUCCIONES['ADD'],))
                self.codigo.append((self.INSTRUCCIONES['STORE'], nodo['variable']))
                
                # Condición de salida (simulada - máximo 100 iteraciones)
                self.codigo.append((self.INSTRUCCIONES['LOAD'], nodo['variable']))
                self.codigo.append((self.INSTRUCCIONES['PUSH'], 100))
                self.codigo.append((self.INSTRUCCIONES['LT'],))
                self.codigo.append((self.INSTRUCCIONES['JMP'], etiqueta_inicio))

                
                self.codigo.append((etiqueta_fin + ':',))
                
            elif nodo['tipo'] == 'llamada_funcion':
                self._generar_codigo_llamada_funcion(nodo)
    
            elif nodo['tipo'] == 'definicion_funcion':
                self._generar_codigo_funcion(nodo)

            elif nodo['tipo'] == 'declaracion_arreglo':
                self._generar_codigo_declaracion_arreglo(nodo)

            elif nodo['tipo'] in ['acceso_arreglo', 'asignacion_arreglo']:
                self._generar_codigo_acceso_arreglo(nodo)

    def _generar_codigo_funcion(self, nodo):
        """Genera bytecode para definición de función"""
        etiqueta_funcion = f"func_{nodo['nombre']}"
        self.codigo.append((etiqueta_funcion + ':',))
        
        # Procesar cuerpo de la función
        for instruccion in nodo['cuerpo']:
            if instruccion['tipo'] == 'retornar':
                self._generar_codigo_retorno(instruccion)
            else:
                self._generar_codigo(instruccion)
        
        # Si no hay RET explícito, agregar retorno por defecto
        if not any(inst.get('tipo') == 'retornar' for inst in nodo['cuerpo']):
            if nodo.get('tipo_retorno') != RES_VOID:
                # Retornar valor por defecto según el tipo
                if nodo['tipo_retorno'] == RES_ENTERO:
                    self.codigo.append((self.INSTRUCCIONES['PUSH'], 0))
                elif nodo['tipo_retorno'] == RES_FLOTANTE:
                    self.codigo.append((self.INSTRUCCIONES['PUSH'], 0.0))
                elif nodo['tipo_retorno'] == RES_CADENA:
                    self.codigo.append((self.INSTRUCCIONES['PUSH'], ""))
                elif nodo['tipo_retorno'] == RES_BOOLEANO:
                    self.codigo.append((self.INSTRUCCIONES['PUSH'], 0))
                self.codigo.append((self.INSTRUCCIONES['RETVAL'],))
            else:
                self.codigo.append((self.INSTRUCCIONES['RET'],))

    def _generar_codigo_llamada_funcion(self, nodo):
        """Genera bytecode para llamada a función con retorno"""
        # Guardar dirección de retorno
        etiqueta_retorno = self.nueva_etiqueta()
        self.codigo.append((self.INSTRUCCIONES['PUSH'], etiqueta_retorno))
        
        # Saltar a función
        etiqueta_funcion = f"func_{nodo['nombre']}"
        self.codigo.append((self.INSTRUCCIONES['JMP'], etiqueta_funcion))
        
        # Punto de retorno
        self.codigo.append((etiqueta_retorno + ':',))
        
        # El valor de retorno queda en el tope de la pila
        # Se puede usar en expresiones posteriores

    def _generar_codigo_entrada(self, nodo):
        """Genera bytecode para lectura de entrada"""
        self.codigo.append((self.INSTRUCCIONES['READ'], nodo['variable']))

    def _generar_codigo_retorno(self, nodo):
        """Genera bytecode para instrucción retornar"""
        if nodo['expresion'] is not None:
            # Generar código para la expresión a retornar
            self._generar_expresion(nodo['expresion'])
            # Retornar con valor (el valor está en el tope de la pila)
            self.codigo.append((self.INSTRUCCIONES['RETVAL'],))
        else:
            # Retorno sin valor
            self.codigo.append((self.INSTRUCCIONES['RET'],))

    def _generar_expresion(self, expresion):
        """Genera código para expresiones"""
        if expresion['tipo'] == 'literal':
            valor = self._convertir_valor(expresion['valor'], expresion['tipo_dato'])
            self.codigo.append((self.INSTRUCCIONES['PUSH'], valor))
            
        elif expresion['tipo'] == 'variable':
            self.codigo.append((self.INSTRUCCIONES['LOAD'], expresion['nombre']))
            
        elif expresion['tipo'] == 'binaria':
            self._generar_expresion(expresion['izquierda'])
            self._generar_expresion(expresion['derecha'])
            
            operador = expresion['operador']
            if operador == '+':
                self.codigo.append((self.INSTRUCCIONES['ADD'],))
            elif operador == '-':
                self.codigo.append((self.INSTRUCCIONES['SUB'],))
            elif operador == '*':
                self.codigo.append((self.INSTRUCCIONES['MUL'],))
            elif operador == '/':
                self.codigo.append((self.INSTRUCCIONES['DIV'],))
    
    def _generar_condicion(self, condicion):
        """Genera código para condiciones"""
        if condicion['tipo'] == 'comparacion':
            self._generar_expresion(condicion['izquierda'])
            self._generar_expresion(condicion['derecha'])
            
            operador = condicion['operador']
            if operador == '==':
                self.codigo.append((self.INSTRUCCIONES['EQ'],))
            elif operador == '<>':
                self.codigo.append((self.INSTRUCCIONES['NEQ'],))
            elif operador == '>':
                self.codigo.append((self.INSTRUCCIONES['GT'],))
            elif operador == '<':
                self.codigo.append((self.INSTRUCCIONES['LT'],))
            elif operador == '>=':
                self.codigo.append((self.INSTRUCCIONES['GTE'],))
            elif operador == '<=':
                self.codigo.append((self.INSTRUCCIONES['LTE'],))
    
    def _convertir_valor(self, valor, tipo_dato):
        """Convierte valores según su tipo"""
        if tipo_dato == LIN_NUM_ENTERO:
            return int(valor)
        elif tipo_dato == LIN_NUM_FLOTANTE:
            return float(valor)
        elif tipo_dato == LIN_CADENA:
            return str(valor).strip('"')
        return valor
    
    def nueva_etiqueta(self):
        """Genera una nueva etiqueta única"""
        etiqueta = f"L{self.contador_etiquetas}"
        self.contador_etiquetas += 1
        return etiqueta
    
    def mostrar_bytecode(self):
        """Muestra el byte-code generado de forma legible"""
        output = []
        for instruccion in self.codigo:
            if isinstance(instruccion[0], int):
                nombre = [k for k, v in self.INSTRUCCIONES.items() if v == instruccion[0]][0]
                if len(instruccion) > 1:
                    output.append(f"{nombre} {instruccion[1]}")
                else:
                    output.append(nombre)
            else:
                output.append(instruccion[0])
        return "\n".join(output)
    
    def get_codigo(self):
        return self.codigo