"""
maquina_virtual
"""

class MaquinaVirtual:
    def __init__(self):
        self.pila = []
        self.memoria = {}
        self.puntero = 0
        self.codigo = []
        self.etiquetas = {}
        self.salida = []
        self.entradas = []
        self.indice_entrada = 0
        
    def cargar_codigo(self, codigo):
        """Carga el byte-code en la máquina virtual"""
        self.codigo = codigo
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
        
        while self.puntero < len(self.codigo):
            instruccion = self.codigo[self.puntero]
            
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
                elif opcode == 9:  # READ
                    if self.indice_entrada < len(self.entradas):
                        entrada = self.entradas[self.indice_entrada]
                        self.indice_entrada += 1
                        try:
                            # Intentar convertir a número
                            if '.' in entrada:
                                valor = float(entrada)
                            else:
                                valor = int(entrada)
                        except ValueError:
                            valor = entrada  # Mantener como string
                        self.memoria[instruccion[1]] = valor
                    else:
                        # Valor por defecto si no hay entrada
                        self.memoria[instruccion[1]] = 0
                elif opcode == 10:  # JMP
                    if instruccion[1] in self.etiquetas:
                        self.puntero = self.etiquetas[instruccion[1]]
                        continue
                elif opcode == 11:  # JMPZ
                    if self.pila and instruccion[1] in self.etiquetas:
                        if self.pila.pop() == 0:
                            self.puntero = self.etiquetas[instruccion[1]]
                            continue
                elif opcode == 12:  # JMPNZ
                    if self.pila and instruccion[1] in self.etiquetas:
                        if self.pila.pop() != 0:
                            self.puntero = self.etiquetas[instruccion[1]]
                            continue
                elif opcode == 13:  # CALL
                    # Guardar posición de retorno
                    self.pila.append(self.puntero + 1)
                    # Saltar a función
                    if instruccion[1] in self.etiquetas:
                        self.puntero = self.etiquetas[instruccion[1]]
                        continue
                elif opcode == 14:  # RET
                    # Retornar a posición guardada
                    if self.pila:
                        self.puntero = self.pila.pop()
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
                        
            except Exception as e:
                self.salida.append(f"ERROR en ejecución: {str(e)}")
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
        """Ejecuta una sola instrucción (para depuración)"""
        if self.puntero < len(self.codigo):
            instruccion = self.codigo[self.puntero]
            
            if isinstance(instruccion[0], str) and instruccion[0].endswith(':'):
                self.puntero += 1
                return True
                
            # Ejecutar una sola instrucción
            # (Implementación similar a ejecutar() pero para una instrucción)
            self.puntero += 1
            return True
        return False