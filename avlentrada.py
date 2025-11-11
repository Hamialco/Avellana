"""
Manejo de entrada de datos para la máquina virtual
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