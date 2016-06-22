#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import gramatica

###############################################################################


class Item(object):

    def __init__(self, simbolo, produz, pos = 0):
        self.__simbolo__ = simbolo
        self.__produz__  = tuple(produz)
        self.__pos__     = pos
	
    def proximoItem(self):
        return Item(self.__simbolo__, self.__produz__, self.__pos__ + 1)

    def proximoSimbolo(self):
        if self.__pos__ == len(self.__produz__):
            return gramatica.EPSILON
        else:
            return self.__produz__[self.__pos__]
	
    def fim(self):
        return self.__pos__ == len(self.__produz__)
	
    def simbolo(self):
        return self.__simbolo__

    def producao(self):
        return gramatica.Producao(self.__simbolo__, self.__produz__)

    def __hash__(self):
        return hash(self.__simbolo__) ^ hash(self.__produz__)

    def __eq__(self, item):
        return self.__simbolo__ == item.__simbolo__ and self.__produz__ == item.__produz__ and self.__pos__ == item.__pos__

    def __repr__(self):
        rhs = ''
        for n, simbolo in enumerate(self.__produz__):
            if self.__pos__ == n:
                rhs += '. '
            rhs += str(simbolo) + ' '
        if self.__pos__ == len(self.__produz__):
            rhs += '.'
        return '%s -> %s' % (self.__simbolo__, rhs)


###############################################################################


class Estado(object):

    def __init__(self, itens):
        self.__itens__ = set(itens)
	
    def fecha(self, gram):
        novos = list(self.__itens__)
        for item in novos:
            simbolo = item.proximoSimbolo()
            if simbolo in gram.nterminais():
                fecho = set(Item(simbolo, produz) for produz in gram.producoes(simbolo))
                fecho -= self.__itens__
                self.__itens__ |= fecho
                novos.extend(fecho)
		
    def filhos(self, gramatica):
        d = dict()
        for item in self.__itens__:
            if not item.fim():
                d.setdefault(item.proximoSimbolo(), set()).add(item.proximoItem())
        for simbolo, itens in d.iteritems():
            e =  Estado(itens)
            e.fecha(gramatica)
            yield simbolo, e
	
    def itens(self):
        for item in self.__itens__:
            yield item

    def __hash__(self):
        return hash(frozenset(self.__itens__))

    def __eq__(self, estado):
        return self.__itens__ == estado.__itens__

    def __repr__(self):
        return ' ' + '\n '.join(str(item) for item in self.__itens__)


###############################################################################


NADA    = ''
REDUZ   = 'Reduz'
EMPILHA = 'Empilha'
ACEITA  = 'AC'

class Slr(object):

    def __init__(self, gramatica):
        self.__gramatica__ = gramatica
        self.__geraEstados__()

    # Gera os estados que serão irão compor a tabela
    
    def __geraEstados__(self):
        self.__estados__ = []

        # partindo do estado 0
        estado0 = Estado(Item(gramatica.INICIO, produz) for produz in self.__gramatica__.producoes(gramatica.INICIO))
        estado0.fecha(self.__gramatica__)

        feitos = set((estado0,))
        fila   = list((estado0,))
        tabela = list()

        for numero, estado in enumerate(fila):
            tabela.append(dict())
            for item in estado.itens():
                if item.fim():
                    for simbolo in self.__gramatica__.sequencia(item.simbolo()):
                        if tabela[numero].setdefault(simbolo, (NADA, 0))[0] == REDUZ:
                            raise Exception('reduz-reduz detectado!')
                        if tabela[numero][simbolo][0] == NADA:
                            tabela[numero][simbolo] = (REDUZ, item.producao())

            for simbolo, filho in estado.filhos(self.__gramatica__):
                if tabela[numero].setdefault(simbolo, (NADA, 0))[0] == REDUZ:
                    aux2 = 3

                if simbolo == gramatica.FIM:
                    tabela[numero][simbolo] = (ACEITA, 0)

                elif not filho in feitos:
                    tabela[numero][simbolo] = (EMPILHA, len(fila))
                    feitos.add(filho)
                    fila.append(filho)

                else:
                    tabela[numero][simbolo] = (EMPILHA, fila.index(filho))

        self.__tabela__ = tabela
	
    
    # Análise dos tokens percorrendo a tabela slr(1) da gramática.
    #
    # pilha1 => contém os estados
    # pilha2 => contém os símbolos

    def parse(self, simbolos):
        simbolos = list(simbolos)
        simbolos.append(gramatica.FIM)
        line_token = 0

        aceita = False
        pilha1 = []
        pilha2 = []
        estado = 0
        reduzi = False
        iter_simbolos = iter(simbolos)
        simbolo = iter_simbolos.next()
        
        while not aceita:
            
            if not self.__tabela__[estado].has_key(simbolo):
                return {'result': False, 'line': line_token, 'token': simbolo}

            acao = self.__tabela__[estado][simbolo]

            if acao[0] == ACEITA:
                aceita = True

            elif acao[0] == EMPILHA:
                
                pilha1.append(estado)
                pilha2.append(simbolo)
                estado = acao[1]
                simbolo = iter_simbolos.next()
                line_token += 1

            elif acao[0] == REDUZ:
                
                for i in xrange(len(acao[1].produz())):
                    estado = pilha1.pop()
                    pilha2.pop()
                
                pilha1.append(estado)
                pilha2.append(acao[1].simbolo())
                estado = self.__tabela__[estado][acao[1].simbolo()][1]
                
                # [DEBUG] estado/acao atual
                # print estado
                
                # [DEBUG] Pilha com estados 
                # print pilha1

                # [DEBUG] Pilha com simbolos
                # print pilha2

        return {'result': True}

###############################################################################
