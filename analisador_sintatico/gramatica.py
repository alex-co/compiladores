#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import pdb
import sys

EPSILON = 'EPSILON'
INICIO  = 'S'
FIM     = '$'

def iter_r(seq):
    for i, d in enumerate(seq):
        yield (d, seq[i+1:])

class Producao(object):
    def __init__(self, simbolo, produz):
        self.__simbolo__ = simbolo
        self.__produz__ = tuple(produz)
	
    def simbolo(self):
        return self.__simbolo__

    def produz(self):
        return self.__produz__

    def __repr__(self):
        rhs = ''
        for simbolo in self.__produz__:
            rhs += ' ' + str(simbolo)
        return ('%s ->%s' % (self.__simbolo__, rhs))

    def __hash__(self):
        return hash(self.__simbolo__) ^ hash(self.__produz__)

    def __cmp__(self, prod):
        return self.__simbolo__ == prod.__simbolo__ and self.__produz__ == prod.__produz__

class Gramatica(object):
    def __init__(self, regras, inicial):
        self.__regras__      = (Producao(INICIO, (inicial, FIM)),) + tuple(Producao(regra[0], tuple(regra[1])) for regra in regras )
        self.__regras_dict__ = dict()

        for regra in self.__regras__:
            self.__regras_dict__.setdefault(regra.simbolo(), set()).add(regra.produz())

        self.__nterminais__ = set(regra.simbolo() for regra in self.__regras__)
        self.__simbolos__   = set(simbolo for regra in self.__regras__ for simbolo in regra.produz() ) | self.__nterminais__
        self.__terminais__  = self.__simbolos__ - self.__nterminais__
        self.__first__      = dict((simbolo, set()) for simbolo in self.__nterminais__)
        self.__follow__     = dict((simbolo, set()) for simbolo in self.__simbolos__)

        # calcula conjunto first individualmente
        def fi(simbolos):
            if len(simbolos) == 0:
                return set([EPSILON])
            resp = set()
            for simbolo in simbolos:
                if simbolo in self.__terminais__:
                    resp.add(simbolo)
                    break
                elif not (EPSILON in self.__first__[simbolo]):
                    resp |= (self.__first__[simbolo])
                    break
                else:
                    resp |= (self.__first__[simbolo] - set([EPSILON]))
            else:
                resp.add(EPSILON)
#            print resp
            return resp

        # calcula conjunto FIRST para todo mundo
        change = True
        while change:
            change = False
            for regra in self.__regras__:
                f = fi(regra.produz())
                if not self.__first__[regra.simbolo()] >= f:
                    change = True
                    self.__first__[regra.simbolo()] |= f


        # calcula conjunto FOLLOW para todo mundo
        change = True
        while change:
            change = False
            for regra in self.__regras__:
                for simbolo, resto in iter_r(regra.produz()):
                    f = fi(resto)
                    if not self.__follow__[simbolo] >= f - set([EPSILON]):
                        change = True
                        self.__follow__[simbolo] |= f - set([EPSILON])
                    if EPSILON in f:
                        if not self.__follow__[simbolo] >= self.__follow__[regra.simbolo()]:
                            change = True
                            self.__follow__[simbolo] |= self.__follow__[regra.simbolo()]

    def sequencia(self, simbolo):
        return self.__follow__[simbolo]

    def terminais(self):
        return self.__terminais__

    def nterminais(self):
        return self.__nterminais__

    def producoes(self, simbolo):
        return self.__regras_dict__[simbolo]

