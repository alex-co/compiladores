#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Produções:                                                            Checagem:

# 1:  PROG      -> DECL_VAR CONST FUNCOES MAIN
# 2:  DECL_VAR  -> TIPO id ; DECL_VAR
# 3:  DECL_VAR  ->
# 4:  CONST     -> const id = num ; CONST                               [ TIPO id == ( int | float ) ]
# 5:  CONST     ->
# 6:  FUNCOES   -> FUNCAO FUNCOES
# 7:  FUNCOES   ->
# 8:  FUNCAO    -> TIPO id ( ) { DECL_VAR CMDS return id ; }            [ TIPO id == return (TIPO id) ]
# 9:  MAIN      -> main { DECL_VAR CMDS }
# 10: TIPO      -> int
# 11: TIPO      -> float
# 12: TIPO      -> char
# 13: TIPO      -> string
# 14: CMDS      -> CMD CMDS
# 15: CMDS      -> CMD
# 16: CMD       -> IF
# 17: CMD       -> WHILE
# 18: CMD       -> FOR
# 19: CMD       -> ATR
# 20: CMD       -> INCR ;
# 21: CMD       -> CH_FUNC
# 22: IF        -> if ( TESTE ) { CMDS }
# 23: IF        -> if ( TESTE ) { CMDS } else { CMDS }
# 24: WHILE     -> while ( TESTE ) { CMDS }
# 25: FOR       -> for ( ATR_FOR ; TESTE ; INCR ) { CMDS }
# 26: ATR       -> id = num ;                                           [ TIPO id == ( int | float ) ]
# 27: ATR       -> id = EXPR_MAT ;                                      [ TIPO id == TIPO EXPR_MAT ]
# 28: ATR       -> id = ch ;                                            [ TIPO id == ch ]
# 29: ATR       -> id = string ;                                        [ TIPO id == string ]
# 30: ATR       -> id = CH_FUNC ;                                       [ TIPO id == return (TIPO id) ]
# 31: ATR       -> id = id ;                                            [ TIPO id == TIPO id ]
# 32: CH_FUNC   -> id ( ) ;
# 33: INCR      -> id ++                                                [ TIPO id == int ]
# 34: INCR      -> id --                                                [ TIPO id == int ]
# 35: ATR_FOR   -> id = num                                             [ TIPO id == ( int | float ) ]
# 36: EXPR_MAT  -> num OP_ARIT num                                      [ (int == int) | (float == float) ]
# 37: EXPR_MAT  -> id  OP_ARIT id
# 38: EXPR_MAT  -> id  OP_ARIT num
# 39: EXPR_MAT  -> num OP_ARIT id
# 40: TESTE     -> EXPR_REL
# 41: TESTE     -> EXPR_REL OP_LOG TESTE
# 42: EXPR_REL  -> id  OP_REL id
# 43: EXPR_REL  -> id  OP_REL num
# 44: EXPR_REL  -> num OP_REL id
# 45: EXPR_REL  -> num OP_REL num
# 46: OP_REL    -> ==
# 47: OP_REL    -> >
# 48: OP_REL    -> <
# 49: OP_REL    -> >=
# 50: OP_REL    -> <=
# 51: OP_REL    -> !=
# 52: OP_LOG    -> &&
# 53: OP_LOG    -> ||
# 54: OP_ARIT   -> +
# 55: OP_ARIT   -> -
# 56: OP_ARIT   -> *
# 57: OP_ARIT   -> /
# 58: OP_ARIT   -> #
# 59: OP_ARIT   -> %
