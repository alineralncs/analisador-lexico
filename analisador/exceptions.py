import re


class IdentifierException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Identifier:
    SUPPORTED_TYPES = ['IDENTIFIER']
    def __init__(self, value):
        self.value = value

       
    def validate(self):
        reserved_words = {'int': 'INT', 'char': 'CHAR', 'long': 'LONG', 'short': 'SHORT', 'float': 'FLOAT',
                          'double': 'DOUBLE', 'void': 'VOID', 'if': 'IF', 'else': 'ELSE', 'for': 'FOR',
                          'while': 'WHILE', 'do': 'DO', 'break': 'BREAK', 'continue': 'CONTINUE', 'struct': 'STRUCT',
                          'switch': 'SWITCH', 'case': 'CASE', 'default': 'DEFAULT', 'return': 'RETURN', 'main': 'MAIN',
                          'printf': 'PRINTF'}
        print('self', self.value)
        if self.value in reserved_words:
            raise IdentifierException(f"Palavra reservada inválida: {self.value}")
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$|^[0-9][A-Za-z0-9_]*$', self.value):
            raise IdentifierException(f"Identificador inválido: {self.value}. Não pode começar com um número.")
        return self.value
            
class KeywordException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Keyword:
    SUPPORTED_TYPES = ['KEYWORD']
    def __init__(self, value):
        self.value = value  


    def validate(self):
        keyword_list = ['int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while', 'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return']
        numberint = r'\d+',
        numberfloat = r'\d+\.\d+'
        indetifier = r'[a-zA-Z_][a-zA-Z0-9_]*'
  
        if self.value in keyword_list:  #or not re.match(numberint, self.value) or not re.match(numberfloat, self.value) or not re.match(indetifier, self.value):
            print('entra aqui')
            raise KeywordException(
                'Este é um Identificador inválido: {} pois é uma palavra reservada'.format(self.value))


class IntegerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Integer:
    SUPPORTED_TYPES = ['INTEGER']
    def __init__(self, value):
        self.value = value

    def validate(self):
        try:
            int(self.value)
        except ValueError:
            raise IntegerException(
                'Este é um Inteiro inválido: {}.'.format(self.value))


class FloatException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Float:
    SUPPORTED_TYPES = ['FLOAT']
    def __init__(self, value):
        self.value = value

    def validate(self):
        try:
            float(self.value)
        except ValueError:
            raise FloatException(
                'Este é um Float inválido: {}.'.format(self.value))


class OperatorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Operator:
    SUPPORTED_TYPES = ['OPERATOR']
    def __init__(self, value):
        self.value = value

    def validate(self):
        if self.value not in ['++', '--', '=', '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '!', '&&', '||', '&']:
            raise OperatorException(
                'Este é um Operador inválido: {}.'.format(self.value))


class DelimiterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Delimiter:
    SUPPORTED_TYPES = ['DELIMITER']
    def __init__(self, value):
        self.value = value

    def validate(self):
        if self.value not in ['(', ')', '[', ']', '{', '}', ';', ',']:
            raise DelimiterException(
                'Este é um Delimitador inválido: {}.'.format(self.value))
