#!/usr/bin/python

DELIMITER  = [' ', '\t', '\n', '(', ')', '{', '}', ';']

SPEC_CHAR  = ['{', '}', '[', ']', '(', ')', ';']
DATA_TYPE  = ['int', 'char', 'float', 'const', 'string']
RESERVED   = ['for', 'while', 'if', 'else', 'main', 'return']

ARIT_OP    = ['+', '++', '-', '--', '*', '/', '#', '%']
REL_OP     = ['>', '<', '>=', '<=', '==', '!=']
LOGIC_OP   = ['||', '&&']

FORBIDDEN  = ['@', '$', '`', ',']

# Few useful constants (this is more like language, but...)
NEWLINE    = '\n'
TAB        = '\t'
BLANKSPACE = ' '
BLANK      = [NEWLINE, TAB, BLANKSPACE]

SINGLEQUOTE = '\''
DOUBLEQUOTE = '\"'
QUOTES      = [SINGLEQUOTE, DOUBLEQUOTE]

OPENCOMMENT  = '/*'
CLOSECOMMENT = '*/'

# token keys
COMMENT = 'comment'
TOKEN   = 'token'
ERROR   = 'error'
EOF     = 'eof'

CHAR = 1
