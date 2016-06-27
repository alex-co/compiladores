#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, copy

    # TODO: Tratar casos de retorno de funções
    # TODO: Tratar casos com declarações de constantes

#-----------------------------------------------------------------------

class VerifTipos(object):

    # Todo o procedimento de checagem de tipos é feita
    # na instanciação da classe VerifTipos.
    def __init__(self, symbols_list):

        self.__symbols_list__ = symbols_list
        self.clean_symbols_list()
        self.__types_list__  = [['int'],['char'],['float'],['string'],['const']]
        self.__types_hash__  = {}
        self.build_type_tables()
        self.__matching__    = self.parse_lines()

    # Remove caracteres {<,>}, campos vazios por ' ' e separador por ','
    def clean_symbols_list(self):

        for i in range(0,len(self.__symbols_list__)):
            for j in range(1,len(self.__symbols_list__[i])):
                symbol = self.__symbols_list__[i][j]
                symbol = symbol[1:-1]
                symbol_id   = symbol.split(';')[0]
                symbol_attr = symbol.split(';',1)[1]
                if symbol_id   == '': symbol_id   = ' '
                if symbol_attr == '': symbol_attr = ' '
                self.__symbols_list__[i][j] = ','.join([symbol_id,symbol_attr])
                
    def get_symbol_from_list(self,lin,col,offset):
        symbol = self.__symbols_list__[lin][col+offset]
        symbol_id    = symbol.split(',')[0]
        symbol_attr  = symbol.split(',')[1]
        return (symbol_id,symbol_attr)
        
    def insert_symbol_in_list(self,the_list,symbol,symbol_type):
        for line in the_list:
            if symbol_type in line[0]:
                line.append(symbol)

    # Preenche tabela de tipos com todas a variáveis declaradas
    def build_type_tables(self):

        self.__types_hash__['global'] = copy.deepcopy(self.__types_list__)
        typeset = self.__types_hash__['global']

        wait_next_symbol = False
        skip_steps = 0

        for i in range(0,len(self.__symbols_list__)):
            for j in range(1,len(self.__symbols_list__[i])):
                
                if skip_steps > 0:
                    skip_steps -= 1;
                    break

                symbol_id   = self.get_symbol_from_list(i,j,0)[0]
                symbol_attr = self.get_symbol_from_list(i,j,0)[1]

                # escopo da 'main'
                if symbol_attr == 'main' and symbol_id == 'reserved':
                    self.__types_hash__['main'] = copy.deepcopy(self.__types_list__)
                    typeset = self.__types_hash__['main']
                    continue

                # escopo de funções
                if symbol_attr == 'id' and self.__symbols_list__[i][j+1].split(',')[1] == '(':
                    self.__types_hash__[symbol_id] = copy.deepcopy(self.__types_list__)
                    self.__types_hash__[symbol_id].append(['return'])
                    typeset = self.__types_hash__[symbol_id]

                # declarações das variáveis
                if symbol_id == 'type':
                    nxt1_symbol = self.get_symbol_from_list(i,j,1)
                    if nxt1_symbol[1] == 'id':
                        self.insert_symbol_in_list(typeset,nxt1_symbol[0],symbol_attr)
                    
                if symbol_id == 'reserved':
                    
                    if symbol_attr == 'const':
                        nxt1_symbol = self.get_symbol_from_list(i,j,1)
                        nxt2_symbol = self.get_symbol_from_list(i,j,2)
                        if nxt1_symbol[0] == 'type' and nxt2_symbol[1] == 'id':
                            self.insert_symbol_in_list(typeset,nxt2_symbol[0],'const')
                    
                    if symbol_attr == 'return':
                        nxt1_symbol = self.get_symbol_from_list(i,j,1)
                        if nxt1_symbol[1] == 'id':
                            self.insert_symbol_in_list(typeset,nxt1_symbol[0],'return')

        # Imprime lista de variáveis por escopo
        #for item in self.__types_hash__:
        #    print "%s => %s" % (item, self.__types_hash__[item])

    # Procura por símbolos que sugerem uma checagem de tipos
    # e encaminha para checagem no método apropriado.
    def parse_lines(self):

        test_result = (True, "")

        for line in self.__symbols_list__:
            line_n = int(line[0]) + 1

            for i, symbol in enumerate(line[1:]):
                if   'attr'in symbol:
                    test_result = self.attr_check(line,i+1)
                elif 'op_arit' in symbol:
                    test_result = self.op_arit_check(line,i+1)
                elif 'op_rel' in symbol:
                    test_result = self.op_rel_check(line,i+1)
                elif 'op_logic' in symbol:
                    test_result = self.op_logic_check(line,i+1)
                else:
                    continue

                if not test_result[0]:
                    return '  Type mismatch at line %s: \n  %s' % (line_n, test_result[1])

        return '  No type mismatch found, everything is definitely fine!'

    # Restorna o tipo de um determinado 'id' da tabela de tipos
    # ou checa o tipo de um número ou o tipo de uma constante.
    def get_type(self,line,index,pos):

        symbol_id   = line[index+pos].split(',')[0]
        symbol_attr = line[index+pos].split(',')[1]

        if symbol_attr == 'num':
            if self.is_int(symbol_id):
                return 'int'
            if self.is_float(symbol_id):
                return 'float'
        elif symbol_attr == 'ch':
            return 'char'
        elif symbol_attr == 'string':
            return 'string'
        else:
            for type_line in self.__types_list__:
                if symbol_id in type_line:
                    return type_line[0]
        return 'unknown'

    # Checa os tipos envolvidos em uma atribuição.
    def attr_check(self,line,index):

        type_before  = self.get_type(line,index,-1)
        symbol_attr  = line[index-1].split(',')[1]
        if symbol_attr != 'id':
            return (False, "Constant '%s' cannot accept assignments" % (type_before))
        elif type_before == 'unknown':
            symbol_id = line[index-1].split(',')[0]
            return (False, "Variable '%s' is been used before previous declaration" % (symbol_id))
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
