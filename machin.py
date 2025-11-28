"""
maquina_virtual
"""
class ManejadorEntrada:
    def __init__(self):
        self.entradas_pendientes = []
        self.callback_entrada = None
    
    def configurar_entrada_interactiva(self, callback):
        """Configura callback para entrada interactiva desde GUI"""
        self.callback_entrada = callback
    
    def agregar_entradas(self, entradas):
        """Agrega entradas predefinidas para pruebas"""
        self.entradas_pendientes.extend(entradas)
    
    def obtener_entrada(self, mensaje=""):
        """Obtiene entrada del usuario"""
        if self.entradas_pendientes:
            return self.entradas_pendientes.pop(0)
        elif self.callback_entrada:
            return self.callback_entrada(mensaje)
        else:
            # Valor por defecto para pruebas
            return "0"
    
    def limpiar_entradas(self):
        """Limpia todas las entradas pendientes"""
        self.entradas_pendientes = []

class MaquinaVirtual:
    def __init__(self):
        self.pila = []
        self.memoria = {}
        self.puntero = 0
        self.codigo = []
        self.etiquetas = {}
        self.salida = []
        self.manejador_entrada = ManejadorEntrada()
        self.ejecutando_paso_a_paso = False
        self.pausa_ejecucion = False
        self.arreglos = {} #Diccionario para almacenar arreglos
        
    def cargar_codigo(self, codigo):
        """Carga el byte-code en la máquina virtual"""
        self.codigo = codigo
        self.arreglos = {} #Limpiar arreglos
        self._mapear_etiquetas()
        
    def _mapear_etiquetas(self):
        """Mapea las etiquetas a sus posiciones en el código"""
        for i, instruccion in enumerate(self.codigo):
            if isinstance(instruccion[0], str) and instruccion[0].endswith(':'):
                self.etiquetas[instruccion[0][:-1]] = i
    
    def configurar_entradas(self, entradas):
        """Configura entradas predefinidas para pruebas"""
        self.entradas = entradas
        self.indice_entrada = 0
        
    def obtener_salida(self):
        """Retorna la salida generada durante la ejecución"""
        return self.salida
        
    def limpiar_salida(self):
        """Limpia la salida acumulada"""
        self.salida = []
    
    def ejecutar(self):
        """Ejecuta el byte-code cargado"""
        self.puntero = 0
        self.pila = []
        self.memoria = {}
        self.salida = []
        
        # Asegurar que puntero sea entero
        self.puntero = int(self.puntero)
        
        while self.puntero < len(self.codigo):
            instruccion = self.codigo[self.puntero]
            
             # DEBUG: Mostrar instrucción actual
            print(f"Ejecutando [{self.puntero}]: {instruccion}")
            
            if isinstance(instruccion[0], str) and instruccion[0].endswith(':'):
                self.puntero += 1
                continue
                
            opcode = instruccion[0]
            
            try:
                if opcode == 0:  # PUSH
                    self.pila.append(instruccion[1])
                elif opcode == 1:  # POP
                    if self.pila:
                        self.pila.pop()
                elif opcode == 2:  # ADD
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        if isinstance(a, str) or isinstance(b, str):
                            self.pila.append(str(a) + str(b))
                        else:    
                            self.pila.append(a + b)        
                elif opcode == 3:  # SUB
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(a - b)
                elif opcode == 4:  # MUL
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(a * b)
                elif opcode == 5:  # DIV
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        if b != 0:
                            self.pila.append(a / b)
                        else:
                            self.salida.append("ERROR: División por cero")
                elif opcode == 6:  # STORE
                    if self.pila:
                        valor = self.pila.pop()
                        self.memoria[instruccion[1]] = valor
                elif opcode == 7:  # LOAD
                    if instruccion[1] in self.memoria:
                        self.pila.append(self.memoria[instruccion[1]])
                    else:
                        self.pila.append(0)  # Valor por defecto
                elif opcode == 8:  # PRINT
                    if self.pila:
                        valor = self.pila.pop()
                        self.salida.append(str(valor))
                        print(f"SALIDA: {valor}")  # Para depuración
                    else:
                        self.salida.append("ERROR: Pila vacía al intentar imprimir")
                elif opcode == 9:  # READ
                    variable = instruccion[1]
                    entrada = self.manejador_entrada.obtener_entrada(f"Ingrese {variable}: ")
                    try:
                        # Intentar convertir a número
                        if entrada.isdigit():
                            valor = int(entrada)
                        elif '.' in entrada and entrada.replace('.', '').isdigit():
                            valor = float(entrada)
                        else:
                            valor = entrada
                            
                        self.memoria[variable] = valor
                        self.salida.append(f"[ENTRADA] {variable} = {valor}")
                    except ValueError:
                        self.memoria[variable] = entrada
                        self.salida.append(f"[ENTRADA] {variable} = '{entrada}'")
                elif opcode == 10:  # JMP
                    if instruccion[1] in self.etiquetas:
                        self.puntero = self.etiquetas[instruccion[1]]
                        continue
                elif opcode == 11:  # JMPZ
                    if self.pila and instruccion[1] in self.etiquetas:
                        valor = self.pila.pop()
                        if valor == 0:
                            self.puntero = self.etiquetas[instruccion[1]]
                            continue
                elif opcode == 12:  # JMPNZ
                    if self.pila and instruccion[1] in self.etiquetas:
                        if self.pila.pop() != 0:
                            self.puntero = self.etiquetas[instruccion[1]]
                            continue
                elif opcode == 13:  # CALL
                    # Guardar posición de retorno (la siguiente instrucción)
                    self.pila.append(self.puntero + 1)
                    # Saltar a función
                    if instruccion[1] in self.etiquetas:
                        self.puntero = self.etiquetas[instruccion[1]]
                        continue
                elif opcode == 14:  # RET
                    # Retornar a posición guardada (sin sumar +1)
                    if self.pila:
                        direccion_retorno = self.pila.pop()
                        self.puntero = int(direccion_retorno)  # ← QUITAR el +1
                        continue
                elif opcode == 15:  # HALT
                    break
                elif opcode == 16:  # EQ
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a == b else 0)
                elif opcode == 17:  # NEQ
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a != b else 0)
                elif opcode == 18:  # GT
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a > b else 0)
                elif opcode == 19:  # LT
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a < b else 0)
                elif opcode == 20:  # GTE
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a >= b else 0)
                elif opcode == 21:  # LTE
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        self.pila.append(1 if a <= b else 0)
                elif opcode == 22:  # RETVAL
                    # El valor de retorno está en el tope de la pila
                    valor_retorno = self.pila.pop() if self.pila else None
                    
                    # Retornar a posición guardada
                    if self.pila:
                        direccion_retorno = self.pila.pop()
                        self.puntero = int(direccion_retorno)
                        
                        # Poner el valor de retorno en la pila para que lo use el llamador
                        if valor_retorno is not None:
                            self.pila.append(valor_retorno)
                    continue
                elif opcode == 23:  # STORE_ARR
                    if len(self.pila) >= 2:
                        valor = self.pila.pop()
                        indice = self.pila.pop()
                        nombre_arreglo = instruccion[1]
                        
                        # Inicializar arreglo si no existe
                        if nombre_arreglo not in self.arreglos:
                            self.arreglos[nombre_arreglo] = {}
                        
                        # Almacenar valor
                        self.arreglos[nombre_arreglo][indice] = valor
                elif opcode == 24:  # LOAD_ARR
                    if self.pila:
                        indice = self.pila.pop()
                        nombre_arreglo = instruccion[1]
                        
                        # Cargar valor del arreglo
                        if (nombre_arreglo in self.arreglos and 
                            indice in self.arreglos[nombre_arreglo]):
                            self.pila.append(self.arreglos[nombre_arreglo][indice])
                        else:
                            # Valor por defecto si no existe
                            self.pila.append(0)
                elif opcode == 25:  # ARR_SIZE
                    nombre_arreglo = instruccion[1]
                    if nombre_arreglo in self.arreglos:
                        # Para arreglos simples, usar máximo índice + 1
                        indices = list(self.arreglos[nombre_arreglo].keys())
                        if indices:
                            self.pila.append(max(indices) + 1)
                        else:
                            self.pila.append(0)
                    else:
                        self.pila.append(0)
                elif opcode == 26:  # DUP
                    if self.pila:
                        self.pila.append(self.pila[-1])
                elif opcode == 27:  # SWAP
                    if len(self.pila) >= 2:
                        a = self.pila.pop()
                        b = self.pila.pop()
                        self.pila.append(a)
                        self.pila.append(b)
                elif opcode == 28:  # AND
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        # Convertir a booleanos para la operación AND
                        resultado = 1 if (a and b) else 0
                        self.pila.append(resultado)
                elif opcode == 29:  # OR
                    if len(self.pila) >= 2:
                        b = self.pila.pop()
                        a = self.pila.pop()
                        # Convertir a booleanos para la operación OR
                        resultado = 1 if (a or b) else 0
                        self.pila.append(resultado)
                elif opcode == 30:  # NOT
                    if self.pila:
                        valor = self.pila.pop()
                        # Convertir a booleano para la operación NOT
                        resultado = 1 if not valor else 0
                        self.pila.append(resultado)
            except Exception as e:
                self.salida.append(f"ERROR en ejecución: {str(e)}")
                import traceback
                self.salida.append(traceback.format_exc())
                break
                
            self.puntero += 1
    
    def obtener_estado(self):
        """Retorna el estado actual de la máquina"""
        return {
            'pila': self.pila.copy(),
            'memoria': self.memoria.copy(),
            'puntero': self.puntero,
            'salida': self.salida.copy()
        }
        
    def ejecutar_paso_a_paso(self):
        """Ejecuta una sola instrucción para depuración"""
        if self.puntero >= len(self.codigo):
            return False
            
        instruccion = self.codigo[self.puntero]
        
        if isinstance(instruccion[0], str) and instruccion[0].endswith(':'):
            self.puntero += 1
            return True
            
        # Ejecutar una instrucción
        opcode = instruccion[0]
        self._ejecutar_instruccion(instruccion)
        
        if opcode not in [10, 11, 12, 13, 14]:  # Saltos y llamadas
            self.puntero += 1
            
        return True

    def _ejecutar_instruccion(self, instruccion):
        """Ejecuta una sola instrucción (extraída de ejecutar())"""
        opcode = instruccion[0]
    
        if opcode == 0:  # PUSH
            self.pila.append(instruccion[1])
        elif opcode == 13:  # CALL
            self.pila.append(self.puntero + 1)
            if instruccion[1] in self.etiquetas:
                self.puntero = self.etiquetas[instruccion[1]]
        elif opcode == 14:  # RET
            if self.pila:
                direccion_retorno = self.pila.pop()
                self.puntero = int(direccion_retorno)
                
    def configurar_entrada_interactiva(self, callback):
        """Configura entrada interactiva desde GUI"""
        self.manejador_entrada.configurar_entrada_interactiva(callback)
        
    def configurar_entradas(self, entradas):
        """Configura entradas predefinidas para pruebas"""
        self.manejador_entrada.agregar_entradas(entradas)