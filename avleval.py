"""
eval_v6.py
evaluador de expresiones para lenguaje orientado a objetos en español
"""

from avllexico import *

class Eval:
    def __init__(self, expresion):
        expresion = expresion + " "
        self.operandos = []
        self.operadores = []

        lex = Lexico(expresion)
        error, token = lex.genera_lexico(False)
        if error != ERR_NOERROR:
            return 0
        self.lst = lex.get()

    def aplicar_operacion(self):
        operador = self.operadores.pop()
        derecha = self.operandos.pop()
        izquierda = self.operandos.pop()
        if operador == '+':
            self.operandos.append(izquierda + derecha)
        elif operador == '-':
            self.operandos.append(izquierda - derecha)
        elif operador == '*':
            self.operandos.append(izquierda * derecha)
        elif operador == '/':
            self.operandos.append(izquierda / derecha)

    def precedencia(self, op):
        if op in ('+', '-'):
            return 1
        elif op in ('*', '/'):
            return 2
        return 0

    def eval_expresion(self):
        for tok in self.lst:
            print(tok)
            token = tok[0]
            tipo_token = tok[1]

            if tipo_token == LIN_NUM_ENTERO:
                self.operandos.append(int(token))
            if tipo_token == LIN_NUM_FLOTANTE:
                self.operandos.append(float(token))
            elif token in '+-*/':
                while (self.operadores and self.operadores[-1] != '(' and
                    self.precedencia(self.operadores[-1]) >= self.precedencia(token)):
                    self.aplicar_operacion()
                self.operadores.append(token)
            elif token == '(':
                self.operadores.append(token)
            elif token == ')':
                while self.operadores and self.operadores[-1] != '(':
                    self.aplicar_operacion()
                self.operadores.pop()
            elif tipo_token == LIN_EOF:
                continue

        while self.operadores:
            self.aplicar_operacion()

        return self.operandos[0]

if __name__ == "__main__":
    ev = Eval("12 * 2 - 3")
    resultado = ev.eval_expresion()
    print(resultado)