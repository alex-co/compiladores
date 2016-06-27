#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt

sys.path.insert(0, 'analisador_lexico/')
import automata

sys.path.insert(0, 'analisador_sintatico/')
from gramatica import Gramatica
from slr import Slr

sys.path.insert(0, 'verificador_tipos/')
from veritypes import VerifTipos



def import_gram(gfile):

    f = file(gfile)
    conta = 0   
    prods = list()

    for linha in f:
        conta += 1
        linha = linha.rstrip(os.linesep)

        if linha == '' or linha[0] == '#':
            continue

        regra = tuple(linha.split())

        if len(regra) < 2 or regra[1] != '->':
            raise Exception('Erro: %s:%d' % (arquivo, conta))

        prods.append((regra[0],(regra[2:])))
    
    return prods
    


def tokens_by_line(tokens_list, token_ln):
    
    token  = token_ln[0].get('token')
    line_n = str(token_ln[1] + 1)

    if not tokens_list:
        tokens_list.append([line_n,token])
    else:
        for line in tokens_list:
            if line_n in line[0]:
                line.append(token)
                break
        else:
            tokens_list.append([line_n,token])

    return



def main(argv):

    # importa gramatica
    producoes = import_gram('minic.gram')

    # arquivo fonte de entrada
    source = sys.argv[1]

    # arquivo de saída dos tokens gerados
    dest = open('output.tokens', 'w')

    # tabela de simbolos
    symbol_table = list()
    tokens       = list()
    lines        = list()
    
    # para uso do verificador de tipos
    tokens_list = list()
    
    runaway   = True
    separator = "---------------------------------------------------------"

#=======================================================================
# Analisador Léxico

    print "%s\n%s" % (separator, separator)
    print "Lexical analysis status:"

    with open(source) as fp: 

        while True:
            token_line = automata.get_token(fp)
            token = token_line[0]
            line  = token_line[1]
            
            if not token.has_key('comment'):
                if token.has_key('error'):
                    print token.get('error')
                    sys.exit()

                if token.has_key('token'):
                    token_id   = token.get('token').split(';')[0][1:]
                    token_attr = token.get('token').split(';', 1)[1][:-1]
                    dest.write(token.get('token') + '\n')
                    tokens.append(token_attr)
                    lines.append(line)
                    # Monta uma tabela com os tokens contidos nas linhas
                    # do código fonte para o verificador de tipos.
                    tokens_by_line(tokens_list, token_line)

                if token.has_key('eof'):
                    print "  %d lines scanned, everything is fine so far..." % (token.get('eof'))
                    runaway = False
                    break
    if runaway:
        print "%s\n%s" % (separator, separator)
        print "  Syntactic analysis aborted..."
        sys.exit()
        
#=======================================================================
# Analisador Sintático
    
    print "%s\n%s" % (separator, separator)
    print "Syntactic analysis status:"

    grammar = Gramatica(producoes, producoes[0][0])
    slr     = Slr(grammar)
    result  = slr.parse(tokens)

    if result.get('result'):
        print '  No syntactic errors found, everything remains fine.'
    else:
        print '  Syntactic error near "%s" at line %s' % (result.get('token'), lines[int(result.get('line'))])
        print "  Type checking analysis aborted..."
        print "%s\n%s" % (separator, separator)
        sys.exit()


#=======================================================================

# Verificador de Tipos

    print "%s\n%s" % (separator, separator)
    print "Type checking analysis status:"

    vt = VerifTipos(tokens_list);

    print vt.matching_result()
    print "%s\n%s" % (separator, separator)

#=======================================================================

if __name__ == '__main__':
    main(sys.argv)
