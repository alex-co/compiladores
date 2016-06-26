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
            line_n = line[0]
            
            for i, token in enumerate(line[1:]):
                token = token[1:-1]
                
                if   'attr'in token:
                    test_result = self.attr_check(i)
                    
                elif 'op_arit' in token:
                    test_result = self.op_arit_check(i)
                    
                elif 'op_rel' in token:
                    test_result = self.op_rel_check(i)

                elif 'op_logic' in token:
                    test_result = self.op_logic_check(i)

                else:
                    continue
                    
                if not test_result[0]:
                    return '  Type mismatch at line %s: \n  %s' % (line_n, test_result[1])

        return '  No types mismatch found, everything remains fine.'


    def attr_check(self,index):
        
        return (False, 'attr in position %d' % index)
        
        
    def op_arit_check(self,index):
        
        return (True, 'op_arit in position %d' % index)
        
        
    def op_rel_check(self,index):
        
        return (True, 'op_rel in position %d' % index)
        

    def op_logic_check(self,index):
        
        return (True, 'op_logic in position %d' % index)
        
        
    def matching_result(self):
        return self.__matching__
        
#-----------------------------------------------------------------------        
