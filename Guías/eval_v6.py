
from lexico import *


class Eval :
    def __init__(self, expresion) :
        expresion = expresion + " "
        self.operandos = []
        self.operadores = []

        lex = Lexico(expresion)
        error, token = lex.generaLexico(False)
        if error != ERR_NOERROR :
            return 0
        self.lst = lex.get()


    def aplicarOperacion(self):
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


    def evalExpresion(self):
        for tok in self.lst :
            print(tok)
            token = tok[0]
            tipoToken = tok[1]

            if tipoToken == LIN_NUM_ENTERO :
                self.operandos.append(int(token))
            if tipoToken ==  LIN_NUM_FLOTANTE :
                self.operandos.append(float(token))
            #elif token in '+-*/':
            #    self.operadores.append(token)
            elif token in '+-*/':
                while (self.operadores and self.operadores[-1] != '(' and
                    self.precedencia(self.operadores[-1]) >= self.precedencia(token)) :
                    self.aplicarOperacion()
                self.operadores.append(token)
            elif token == '(':
                self.operadores.append(token)
            elif token == ')':
                while self.operadores and self.operadores[-1] != '(':
                    self.aplicarOperacion()
                self.operadores.pop()  # Quitar el '('
            elif tipoToken == LIN_EOF :
                continue

        while self.operadores:
            self.aplicarOperacion()

        return self.operandos[0]


#--------------------------------------------------- principal
#ev = Eval("(50* 2) - 3")
ev = Eval("12  * 2 - 3")
resultado = ev.evalExpresion()
print(resultado)


