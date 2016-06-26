#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#-----------------------------------------------------------------------

class VerifTipos(object):
    
    def __init__(self, tokens_list):
        
        self.__tokens_list__ = tokens_list
        self.__types_list__  = [['int'],['char'],['float'],['string']]
        
        self.build_types_table()
        
        self.__matching__ = self.parse_lines()
       

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
        
        
    def op_arit_check(self,line,index):
        return (True, 'op_arit in position %d' % index)
        
        
    def op_rel_check(self,line,index):
        return (True, 'op_rel in position %d' % index)
        

    def op_logic_check(self,line,index):
        return (True, 'op_logic in position %d' % index)
    
    
    def is_float(self,number):
        try:
            num = float(number)
        except ValueError:
            return False
        return True


    def is_int(self,number):
        try:
            num = int(number)
        except ValueError:
            return False
        return True


    def matching_result(self):
        return self.__matching__
        
#-----------------------------------------------------------------------        
