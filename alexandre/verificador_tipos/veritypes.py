#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, copy

#-----------------------------------------------------------------------

class VerifTipos(object):

    # Todo o procedimento de checagem de tipos é feita
    # na instanciação da classe VerifTipos.
    def __init__(self, symbols_list):

        self.__symbols_list__ = symbols_list
        self.format_symbols_list()
        self.__types_list__   = [['int'],['char'],['float'],['string'],['const']]
        self.__scope_limits__ = {}
        self.__types_hash__   = {}
        self.build_type_tables()
        self.__matching__     = self.parse_lines()

    # Remove caracteres {<,>}, campos vazios por ' ' e separador por ','
    def format_symbols_list(self):

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

    def get_scope(self,line_n):
        keys = list(self.__scope_limits__.keys())
        for scope in keys:
            ini = self.__scope_limits__[scope][0]
            fim = self.__scope_limits__[scope][1]
            if ini <= int(line_n) <= fim:
                return scope
        return 'global'

    # Preenche tabela de tipos com todas a variáveis e constantes
    # Define os limites de cada escopo
    def build_type_tables(self):

        self.__types_hash__['global'] = copy.deepcopy(self.__types_list__)
        typeset = self.__types_hash__['global']
        self.__scope_limits__['global'] = [1,1]
        scopelm = self.__scope_limits__['global']

        wait_next_symbol = False

        for i in range(0,len(self.__symbols_list__)):
            lin_n = int(self.__symbols_list__[i][0])
            scopelm[1] = lin_n
            for j in range(1,len(self.__symbols_list__[i])):

                symbol_id   = self.get_symbol_from_list(i,j,0)[0]
                symbol_attr = self.get_symbol_from_list(i,j,0)[1]

                # escopo da 'main'
                if symbol_attr == 'main' and symbol_id == 'reserved':
                    self.__types_hash__['main'] = copy.deepcopy(self.__types_list__)
                    typeset = self.__types_hash__['main']
                    self.__scope_limits__['main'] = [lin_n,lin_n]
                    scopelm[1] -= 1
                    scopelm = self.__scope_limits__['main']
                    continue

                # escopo de funções
                if symbol_attr == 'id' and self.get_symbol_from_list(i,j,1)[1] == '(':
                    self.__types_hash__[symbol_id] = copy.deepcopy(self.__types_list__)
                    #self.__types_hash__[symbol_id].append(['return'])
                    typeset = self.__types_hash__[symbol_id]
                    self.__scope_limits__[symbol_id] = [lin_n,lin_n]
                    scopelm[1] -= 1
                    scopelm = self.__scope_limits__[symbol_id]
                    prv1_symbol = self.get_symbol_from_list(i,j,-1)
                    self.insert_symbol_in_list(typeset,symbol_id,prv1_symbol[1])

                # declarações das variáveis
                if symbol_id == 'type':
                    if self.get_symbol_from_list(i,j,2)[1] == '(': continue
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
        #sys.exit()
        # Imprime lista com limites dos escopos
        #for item in self.__scope_limits__:
        #    print "%s => %s" % (item, self.__scope_limits__[item])

    # Procura por símbolos que sugerem uma checagem de tipos
    # e encaminha para checagem no método apropriado.
    def parse_lines(self):

        test_result = (True, "")
        for line in self.__symbols_list__:
            line_n = int(line[0]) + 1
            scope = self.get_scope(line_n)
            for i, symbol in enumerate(line[1:]):
                if   'attr'in symbol:
            #        test_result = (True, "")
                    test_result = self.attr_check(line,i+1,scope)

                elif 'op_arit' in symbol:
                    test_result = self.op_arit_check(line,i+1,scope)
                elif 'op_rel' in symbol:
                    test_result = self.op_rel_check(line,i+1,scope)
                elif 'op_logic' in symbol:
                    test_result = self.op_logic_check(line,i+1,scope)
                elif 'return' in symbol:
                    test_result = self.return_check(line,i+1,scope)
                else:
                    continue

                if not test_result[0]:
                    return '  Type mismatch at line %s: \n  %s' % (line_n, test_result[1])
        return '  No type mismatch found, everything is definitely fine!'

    # Retorna o tipo de um determinado 'id' da tabela de tipos
    # ou checa o tipo de um número ou o tipo de uma constante.
    def get_type(self,line,index,offset,scope):
        symbol_id   = line[index+offset].split(',')[0]
        symbol_attr = line[index+offset].split(',')[1]
        scopes = ['global']
        if scope != 'global':
            scopes.append(scope)
        # se for uma constante não declarada
        if symbol_attr == 'num':
            if self.is_int(symbol_id):
                return ('const','int')
            if self.is_float(symbol_id):
                return ('const','float')
        elif symbol_attr == 'ch'     and symbol_id != 'type':
            return ('const','char')
        elif symbol_attr == 'string' and symbol_id != 'type':
            return ('const','string')
        # se for uma variável ou constante declarada
        the_type = []
        for s in scopes:
            for type_line in self.__types_hash__[s]:
                if symbol_id in type_line:
                    the_type.append(type_line[0])
        if not the_type:
            return ('none','unknown')
        if len(the_type) == 1: # or 'return' in the_type:
            return ('var',the_type[0])
        if 'const' in the_type:
            return ('const',the_type[0])
        return ('fail','unknown')


    # Checa os tipos envolvidos em uma atribuição.
    def attr_check(self,line,index,scope):

        type_before  = self.get_type(line,index,-1,scope)
        if type_before[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index-1][0],scope))
        if type_before[0] == 'const' and line[index-3].split(',')[1] != 'const':
                return (False, "Constant '%s' cannot accept assignments." % (type_before[1]))
        type_after  = self.get_type(line,index,1,scope)
        if type_after[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index+1][0],scope))
        if type_before[1] != type_after[1]:
            return (False, "'%s' to '%s' assignments are not allowed" % (type_after[1],type_before[1]))
        return (True, "")

    # Checa os tipos envolvidos em uma operação aritmética.
    def op_arit_check(self,line,index,scope):
        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1,scope)
        if type_before[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index-1][0],scope))
        if type_before[1] not in {'int','float'}:
            return (False, "Arithmetic operators only applies to number types, '%s' was found instead." % (type_before[1]))
        if operator in {'++','--'}:
            if type_before[1] == 'int':
                return (True, "")
            else:
                return (False, "The '%s' operator only apply to integers, '%s' was found instead." % (operator,type_before[1]))
        type_after  = self.get_type(line,index,1,scope)
        if type_after[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index+1][0],scope))
        if type_after[1] not in {'int','float'}:
            return (False, "Arithmetic operators only applies to number types, '%s' was found instead." % (type_after[1]))
        if type_before[1] != type_after[1]:
            return (False, "The '%s' %s '%s' arithmetic operation is not allowed" % (type_before[1],operator,type_after[1]))
        if operator is '/' and type_before[1] != 'int':
            return (False, "Integer division operator '/' applied to '%s' was found" % (type_before[1]))
        if operator is '#' and type_before[1] != 'float':
            return (False, "Float division operator '#' applied to '%s' was found" % (type_before[1]))
        return (True, "")

    # Checa os tipos envolvidos com operadores relacionais.
    def op_rel_check(self,line,index,scope):
        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1,scope)
        type_after  = self.get_type(line,index, 1,scope)
        if type_after[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index+1][0],scope))
        if type_before[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index-1][0],scope))
        if type_before[1] != type_after[1]:
            return (False, "Found '%s' %s '%s' : operands have different types." % (type_before[1],operator,type_after[1]))
        return (True, "")

    # Checa os tipos envolvidos com operadores lógicos.
    def op_logic_check(self,line,index,scope):
        operator    = line[index].split(',')[1]
        type_before = self.get_type(line,index,-1,scope)
        type_after  = self.get_type(line,index, 1,scope)
        if type_after[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index+1][0],scope))
        if type_before[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index-1][0],scope))
        if type_before[1] != type_after[1]:
            return (False, "Found '%s' %s '%s' : operands have different types." % (type_before[1],operator,type_after[1]))
        return (True, "")

    # Checa retorno de função.
    def return_check(self,line,index,scope):
        type_after = self.get_type(line,index,1,scope)
        for type_line in self.__types_hash__[scope]:
            if scope in type_line:
                type_fret = type_line[0]
                break
        if type_after[1] == 'unknown':
            return (False, "Variable '%s' was not found in this scope (%s)." % (line[index+1][0],scope))
        if type_after[1] != type_fret:
            return (False, "Function must return '%s' but '%s' was found instead." % (type_fret,type_after[1]))
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
