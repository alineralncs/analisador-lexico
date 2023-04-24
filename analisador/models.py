from django.db import models
import re
from .exceptions import IdentifierException, KeywordException, IntegerException, FloatException, OperatorException, DelimiterException
from .exceptions import Identifier, Keyword, Integer, Float, Operator, Delimiter
# Create your models here.

class Arquivo(models.Model):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='arquivos/')

    def __str__(self):
        return self.nome

    def analisar(self, arquivo): 
        regex = {
            # Expressões regulares para palavras-chaves, identificadores, operadores, delimitadores, inteiros, floats e strings
            'keyword': r'(int|char|long|short|float|double|void|if|else|for|while|do|break|continue|struct|switch|case|default|return)',
            'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'operator': r'[+\-*/]|<=|>=|==|!=|\|\||&&|[()!]|(?<=[^+\-*/])\+(?=[^+\-*/=])|(?<=[^+\-*/])\-(?=[^+\-*/=])|\+=(?!=)|-=(?!=)|\*=(?!=)|/=(?!=)|<(?!=)|>(?!=)|(?<=<)=|(?<=>)=|%(?!=)|->(?!=)',
            'delimiter': r'(\(|\)|\[|\]|\{|\}|;|,)',
            'integer': r'\d+',
            'float': r'\d+\.\d+',
            'string': r'"(?:\\.|[^\\"])*"|\'(?:\\.|[^\\\'])*\'',
        }
            #
        token_regex = '|'.join('(?P<%s>%s)' % (name, exp)
                                for name, exp in regex.items())
            # print('token regex', token_regex)
            # i = 0
            # self.posicaoInicial = 0
        TOKEN_TYPES = {
        'IDENTIFIER': Identifier,
        'INTEGER': Integer,
        'FLOAT': Float,
        'OPERATOR': Operator,
        'DELIMITER': Delimiter,
        }
        tokens_list = []
        for line in arquivo.split('\n'):
            print('aq')
            for match in re.finditer(token_regex, line):
                for name, exp in regex.items():
                    if(match.lastgroup == name):
                        token_type = name
                        lexeme = match.group(name)

                    # for token_type, lexeme in get_tokens(text):
                    #     if token_type in TOKEN_TYPES:
                    #         try:
                    #             TOKEN_TYPES[token_type](lexeme).validate(token_type)
                    #             tokens_list.append((token_type, lexeme))
                    #         except TokenValidationException as e:
                    #             print(f"Error: {e}")
                    #     else:
                    #         print(f"Error: Invalid token type {token_type}")
                    #     for token_type, lexeme in tokens_list:
                    #         print(f"Token type: {token_type.__name__}, Lexeme: {lexeme}")

                    # int aaa
                    # int bbb 
                        # if token_type == 'identifier':
                            # satsifaz aaa bbb
                        try:
                            if Identifier(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except IdentifierException as e:
                            print('Error: {}'.format(e)) 
                        try:
                            if Integer(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except IntegerException as e:
                                print('Error: {}'.format(e))

                        try:
                            if Float(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except FloatException as e:
                                print('Error: {}'.format(e))
                        try:
                            if Operator(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except OperatorException as e:
                                print('Error: {}'.format(e))
                        try:
                            if Delimiter(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except DelimiterException as e:
                                print('Error: {}'.format(e))
                        try:
                            if Keyword(lexeme).validate():
                                tokens_list.append((token_type, lexeme))
                        except KeywordException as e:
                                print('Error: {}'.format(e)) 
                        # # try:
                        #         Keyword(lexeme).validate()
                        #         tokens_list.append((token_type, lexeme))
                        # except KeywordException as e:
                        #         print('Error: {}'.format(e)) 
                        # elif(token_type == 'integer'):
                        #     try:
                        #         Integer(lexeme).validate()
                        #         tokens_list.append((token_type, lexeme))
                        #     except IntegerException as e:
                        #         print('Error: {}'.format(e))
                        # elif(token_type == 'float'):
                        #     try:
                        #         Float(lexeme).validate()
                        #         tokens_list.append((token_type, lexeme))
                        #     except FloatException as e:
                        #         print('Error: {}'.format(e))
                        # elif(token_type == 'operator'):
                        #     try:
                        #         Operator(lexeme).validate()
                        #         tokens_list.append((token_type, lexeme))
                        #     except OperatorException as e:
                        #         print('Error: {}'.format(e))
                        # elif(token_type == 'delimiter'):
                        #     try:
                        #         Delimiter(lexeme).validate()
                        #         tokens_list.append((token_type, lexeme))
                        #     except DelimiterException as e:
                        #         print('Error: {}'.format(e))
                        # else:
                        #     # token = <tipo, valor>
                        #     tokens_list.append((token_type, lexeme))
      
        return tokens_list

