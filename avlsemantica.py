"""
semantica
"""

from avllexico import *

class Semantica:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos
        self.errores = []
        
    def verificar_tipos(self, expresion):
        """Verifica la coherencia de tipos en una expresión"""
        # Implementación de verificación de tipos
        pass
        
    def verificar_declaracion(self, identificador):
        """Verifica si un identificador está declarado"""
        for elem in self.tabla_simbolos:
            if elem[0] == identificador:
                return True
        return False
    
    def obtener_tipo(self, identificador):
        """Obtiene el tipo de un identificador"""
        for elem in self.tabla_simbolos:
            if elem[0] == identificador:
                return elem[1]
        return RES_NO_DECL