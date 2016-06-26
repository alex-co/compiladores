#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#-----------------------------------------------------------------------

class VerifTipos(object):
    
    # Todo o procedimento de checagem de tipos é feita
    # na instanciação da classe VerifTipos.

    def __init__(self, tokens_list):
        
        self.__tokens_list__ = tokens_list
        self.__types_list__  = [['int'],['char'],['float'],['string']]
        self.build_types_table()
        self.__matching__ = self.parse_lines()

    # Preenche tabela de tipos com todas a variáveis declaras
    # destino: self.__types_list__

    def build_types_table(self):
        
        wait_next_token = False
        for line in self.__tokens_list__:
            for token in line[1:]:
                token_id   = token.split(';')[0][1:]
                token_attr = token.split(';', 1)[1][:-1]

                if wait_next_token:
                    for lin in self.__types_list__:
                        if current_type in lin[0]:
                            lin.append(token_id)
                    current_type    = ''
                    wait_next_token = False
                
                if token_id == 'type' and token_attr != 'const':
                    current_type    = token_attr
                    wait_next_token = True

    # Procura por tokens que sugerem uma checagem de tipos
    # e encaminha para checagem no método apropriado.
    
    def parse_lines(self):
        
        test_result = (True)
        
        for line in self.__tokens_list__:
            line_n = int(line[0]) + 1
            
            for i, token in enumerate(line[1:]):
                token = token[1:-1]
                if   'attr'in token:
                    test_result = self.attr_check(line,i+1)
                elif 'op_arit' in token:
                    test_result = self.op_arit_check(line,i+1)
                elif 'op_rel' in token:
                    test_result = self.op_rel_check(line,i+1)
                elif 'op_logic' in token:
                    test_result = self.op_logic_check(line,i+1)
                else:
                    continue
                    
                if not test_result[0]:
                    return '  Types mismatch at line %s: \n  %s' % (line_n, test_result[1])

        return '  No types mismatch found, everything remains fine.'

    # Restorna o tipo de um determinado 'id' da tabela de tipos
    # ou checa o tipo de um número ou o tipo de uma constante.
    
    def get_type(self,line,index,pos):

        token_id   = line[index+pos].split(';')[0][1:]
        token_attr = line[index+pos].split(';', 1)[1][:-1]
        
        if token_attr == 'num':
            if self.is_int(token_id):
                return 'int'
            if self.is_float(token_id):
                return 'float'
        elif token_attr == 'ch':
            return 'char'
        elif token_attr == 'string':
            return 'string'
        else:
            for type_line in self.__types_list__:
                if token_id in type_line:
                    return type_line[0]
        
        return 'unknown'

    # Checa os tipos envolvidos em uma atribuição.
    
    def attr_check(self,line,index):
        
        type_before = self.get_type(line,index,-1)
        token_attr  = line[index-1].split(';', 1)[1][:-1]
        if token_attr != 'id':
            return (False, "Constant '%s' cannot accept assignments" % (type_before))
        elif type_before == 'unknown':
            token_id = line[index-1].split(';')[0][1:]
            return (False, "Variable '%s' is been used before previous declaration" % (token_id))
        type_after  = self.get_type(line,index, 1)
        if type_before != type_after:
            return (False, "'%s' to '%s' assignments are not allowed" % (type_after, type_before))
        return (True, "")
        
    # TODO: Checa os tipos envolvidos em uma operação aritmética.
    
    def op_arit_check(self,line,index):
        return (True, 'op_arit in position %d' % index)
        
    # TODO: Checa os tipos envolvidos com operadores relacionais.
    
    def op_rel_check(self,line,index):
        return (True, 'op_rel in position %d' % index)
        
    # TODO: Checa os tipos envolvidos com operadores lógicos.
    
    def op_logic_check(self,line,index):
        return (True, 'op_logic in position %d' % index)
        
    # TODO: Tratar casos de retorno de funções
    # TODO: Tratar casos com declarações de constantes
    
    # Determina se um 'string' represnta um 'float'.
    
    def is_float(self,number):
        try:
            num = float(number)
        except ValueError:
            return False
        return True

    # Determina se um 'string' represnta um 'int'.
    
    def is_int(self,number):
        try:
            num = int(number)
        except ValueError:
            return False
        return True

    # Getter do resultado da verificação de tipos.
    
    def matching_result(self):
        return self.__matching__
        
#-----------------------------------------------------------------------        
