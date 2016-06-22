#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, getopt

sys.path.insert(0, 'analisador_lexico/')
import automata

sys.path.insert(0, 'analisador_sintatico/')
from gramatica import Gramatica
from slr import Slr

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


def main(argv):
    # importa gramatica
    producoes = import_gram('minic.gram')

    # arquivo fonte de entrada
    source = sys.argv[1]

    # arquivo de saída dos tokens gerados
    dest = open('output.tokens', 'w')

    # tabela de simbolos
    symbol_table = list()
    tokens = list()
    lines = list()

    print "Lexical analysis ----------------------------------------"
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
                    dest.write(token.get('token') + '\n')
                    tokens.append(token.get('token').split(';', 1)[1][:-1])
                    lines.append(line)

                    if (token.get('token').split(';')[0])[1:] == "id":
                        identifier = (token.get('token').split(';')[1])[:-1]
                        table_entry = {'identifier': identifier} 
                        symbol_table.append(table_entry)

                if token.has_key('eof'):
                    print "\n%d lines were scanned, everything is fine!" % (token.get('eof'))
                    print "---------------------------------------------------------\n\n"
                    break

    print "Sintatical analysis -------------------------------------"
    grammar = Gramatica(producoes, producoes[0][0])
    slr     = Slr(grammar)
    result  = slr.parse(tokens)

    if result.get('result'):
        print 'Everything went fine. No syntactical errors found.'
    else:
        print 'Syntactical error near "%s" at line %s' % (result.get('token'), lines[int(result.get('line'))])
    print "---------------------------------------------------------"

if __name__ == '__main__':
    main(sys.argv)
