from django.db import models
import re
from .exceptions import IdentifierException, KeywordException, IntegerException, FloatException, OperatorException, DelimiterException, StringValidation
from .exceptions import ExceptionGenerator,Identifier, Keyword, Integer, Float, Operator, Delimiter
# Create your models here.

class Arquivo(models.Model):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='arquivos/')

    def __str__():
        return self.nome
    # r'(\*[_a-zA-Z][_a-zA-Z0-9]*)|([_a-zA-z][_a-zA-Z0-9]*)

    # r'(\*[_a-zA-Z][_a-zA-Z0-9]*)|([_a-zA-Z][_a-zA-Z0-9]*)'
    def analyse(codigoFonte):
        keywords = ['int', 'char', 'long', 'short', 'float', 'double', 'void', 'if', 'else', 'for', 'while',
                             'do', 'break', 'continue', 'struct', 'switch', 'case', 'default', 'return', 'main',
                             'printf', 'scanf']
        types = [
                'int',
                'char',
                'long',
                'float',
                'double',
                'void',
                'String',
                'char'
            ]

        regex = {
            # Expressões regulares para palavras-chaves, identificadores, operadores, delimitadores, inteiros, floats e strings
            'keyword': r'(?<!\w)(int|char|long|short|float|double|void|if|else|for|while|do|break|continue|struct|switch|case|default|return|main|printf|scanf|elif|auto|enum|extern|goto|register|signed|sizeof|static|typedef|union|unsigned|volatile|while)(?!\w)',
            'operator': r'(\+\+|--|->|&&|\|\||<<|>>|<=|>=|==|!=|[!%^&*+=\-\|/~<>\?])',
            'delimiter': r'(\(|\)|\[|\]|\{|\}|;|,|:)',
            'float': r'(?<!\w)[-+]?(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?\b',
            'integer': r'\d+[a-zA-Z]*',
            'string': r'"[^"\n]*"',
            'identifier': r'(?!\b(auto|break|main|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|_Imaginary)\b)[a-zA-Z_]\w*', 
            #'identifier': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 
        }
        #
        token_regex = '|'.join('(?P<%s>%s)' % (name, exp)
                               for name, exp in regex.items())

        # agrupando o dic regex 
        print('token regex', token_regex)


        tokens_list = []
        errors = []
        last_lexeme = None
        i = 0

        codigoFonte = re.sub(
            r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)', '', codigoFonte)

        for line in codigoFonte.split('\n'):
            for match in re.finditer(token_regex, line):

                for name, exp in regex.items():

                    if(match.lastgroup == name):

                        token_type = name

                        lexeme = match.group(name)
                        
                        print(token_type)
                        print(lexeme)
                        ###############################
                        try:
                            if token_type == 'keyword':
                                print(token_type)
                                if lexeme in types and last_lexeme in types:
                                    print(
                                        "Identificador Inválido pois não pode ser uma palavra reservada")
                                else:
                                    if Keyword(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                    else:
                                        print("Error!")
                                        errors.append(
                                            'O lexeme {} não é válido'.format(lexeme))

                            elif token_type == 'identifier':
                                print(token_type)
                                if Identifier(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'operator':
                                if lexeme == '*' and (last_lexeme in types or last_lexeme in keywords or re.match(
                                        regex['delimiter'], last_lexeme)):
                                    token_type = 'pointer'
                                    tokens_list.append((token_type, lexeme))
                                    print(token_type)
                                else:
                                    if Operator(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                    else:
                                        print("Error!")
                                        errors.append(
                                            'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'delimiter':
                                if Delimiter(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'integer':
                                if re.match(r'^\d+$', lexeme):
                                    if Integer(lexeme).validate():
                                        tokens_list.append(
                                            (token_type, lexeme))
                                elif re.match(r"\d+\.\d+", lexeme):
                                    if Float(lexeme).validate():
                                        token_type = 'float'
                                        tokens_list.append(
                                            (token_type, lexeme))
                                else:
                                    token_type = 'identifier'
                                    #print(token_type)
                                    errors.append(
                                        'O lexeme {} é um identificador inválido' .format(lexeme))
            
                                    #print("Este é um identificador inválido")
                            elif token_type == 'float':
                                print(token_type)
                                if Float(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            elif token_type == 'string':
                                print(token_type)
                                if StringValidation(lexeme).validate():
                                    tokens_list.append((token_type, lexeme))
                                else:
                                    print("Error!")
                                    errors.append(
                                        'O lexeme {} não é válido'.format(lexeme))
                            else:
                                print("Erro")
                        except ExceptionGenerator as e:
                            print("Passou?")
                            print("Error: {}".format(e))
                            errors.append(
                                'O lexeme {} não é válido'.format(lexeme))
                        last_lexeme = lexeme

        return tokens_list, errors