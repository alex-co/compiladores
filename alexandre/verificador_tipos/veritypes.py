#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, copy

    # TODO: Tratar casos de retorno de funções
    # TODO: Tratar casos com declarações de constantes

#-----------------------------------------------------------------------

class VerifTipos(object):

    # Todo o procedimento de checagem de tipos é feita
    # na instanciação da classe VerifTipos.
    def __init__(self, tokens_list):

        self.__tokens_list__ = tokens_list
        self.clean_tokens_list()
        self.__types_list__  = [['int'],['char'],['float'],['string'],['const'],['return'],['limits']]
        self.__types_hash__  = {}
        self.build_type_tables()
        self.__matching__    = self.parse_lines()

    # Remove caracteres {<,>}, campos vazios por ' ' e separador por ','
    def clean_tokens_list(self):

        for i in range(0,len(self.__tokens_list__)):
            for j in range(1,len(self.__tokens_list__[i])):
                token = self.__tokens_list__[i][j]
                token = token[1:-1]
                token_id   = token.split(';')[0]
                token_attr = token.split(';',1)[1]
                if token_id   == '': token_id   = ' '
                if token_attr == '': token_attr = ' '
                self.__tokens_list__[i][j] = ','.join([token_id,token_attr])

    # TODO: Identificar os escopos das funções.
    #       OK -> Criar lista de tipos para {global,main, func1, ... ,func_n}

    # Preenche tabela de tipos com todas a variáveis declaradas
    def build_type_tables(self):

        self.__types_hash__['global'] = copy.deepcopy(self.__types_list__)
        typeset = self.__types_hash__['global']

        #pilha = []
        wait_next_token = False
        #wait_func_init  = False

        for i in range(0,len(self.__tokens_list__)):
            prev_simbol = ''
            for j in range(1,len(self.__tokens_list__[i])):
                token = self.__tokens_list__[i][j]
                token_id    = token.split(',')[0]
                token_attr  = token.split(',')[1]

                # escopo da 'main'
                if token_attr == 'main' and token_id == 'reserved':
                    self.__types_hash__['main'] = copy.deepcopy(self.__types_list__)
                    typeset = self.__types_hash__['main']
                    #wait_func_init  = True
                    continue

                # escopo de funções
                if token_attr == 'id' and self.__tokens_list__[i][j+1].split(',')[1] == '(':
                    self.__types_hash__[token_id] = copy.deepcopy(self.__types_list__)
                    typeset = self.__types_hash__[token_id]
                    #wait_func_init  = True
                    #continue

                # declarações das variáveis
                if wait_next_token:
                    for lin in typeset[:-3]:
                        if current_type in lin[0]:
                            lin.append(token_id)
                    current_type    = ''
                    wait_next_token = False

                if token_id == 'type' and token_attr != 'const':
                    current_type    = token_attr
                    wait_next_token = True

        for item in self.__types_hash__:
            print "%s => %s" % (item, self.__types_hash__[item])

    # Procura por tokens que sugerem uma checagem de tipos
    # e encaminha para checagem no método apropriado.
    def parse_lines(self):

        test_result = (True)

        for line in self.__tokens_list__:
            line_n = int(line[0]) + 1

            for i, token in enumerate(line[1:]):
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
                    return '  Type mismatch at line %s: \n  %s' % (line_n, test_result[1])

        return '  No type mismatch found, everything is definitely fine!'

    # Restorna o tipo de um determinado 'id' da tabela de tipos
    # ou checa o tipo de um número ou o tipo de uma constante.
    def get_type(self,line,index,pos):

        token_id   = line[index+pos].split(',')[0]
        token_attr = line[index+pos].split(',')[1]

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
        token_attr  = line[index-1].split(',')[1]
        if token_attr != 'id':
            return (False, "Constant '%s' cannot accept assignments" % (type_before))
        elif type_before == 'unknown':
            token_id = line[index-1].split(',')[0]
            return (False, "Variable '%s' is been used before previous declaration" % (token_id))
        type_after  = self.get_type(line,index, 1)
        if type_before != type_after:
            return (False, "'%s' to '%s' assignments are not allowed" % (type_after, type_before))
        return (True, "")

    # Checa os tipos envolvidos em uma operação aritmética.
    def op_arit_check(self,line,index):

        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1)
        if type_before not in {'int','float'}:
            return (False, "Arithmetic operators only applies to number types, '%s' was found instead." % (type_before))
        if operator in {'++','--'}:
            if type_before == 'int':
                return (True, "")
            else:
                return (False, "The '%s' operator only apply to integers, '%s' was found instead." % (operator,type_before))
        type_after  = self.get_type(line,index, 1)
        if type_after not in {'int','float'}:
            return (False, "Arithmetic operators only applies to number types, '%s' was found instead." % (type_after))
        if type_before != type_after:
            return (False, "The '%s' %s '%s' arithmetic operation is not allowed" % (type_before,operator,type_after))
        if operator is '/' and type_before is not 'int':
            return (False, "Integer division operator '/' applied to '%s' was found" % (type_before))
        if operator is '#' and type_before is not 'float':
            return (False, "Float division operator '#' applied to '%s' was found" % (type_before))
        return (True, "")

    # Checa os tipos envolvidos com operadores relacionais.
    def op_rel_check(self,line,index):

        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1)
        type_after  = self.get_type(line,index, 1)
        if type_before != type_after:
            return (False, "Found '%s' %s '%s' : operands have different types." % (type_before,operator,type_after))
        return (True, "")

    # Checa os tipos envolvidos com operadores lógicos.
    def op_logic_check(self,line,index):

        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1)
        type_after  = self.get_type(line,index, 1)
        if type_before != type_after:
            return (False, "Found '%s' %s '%s' : operands have different types." % (type_before,operator,type_after))
        return (True, "")

    # Determina se um 'string' representa um 'float'.
    def is_float(self,number):

        try:
            num = float(number)
        except ValueError:
            return False
        return True

    # Determina se um 'string' representa um 'int'.
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
