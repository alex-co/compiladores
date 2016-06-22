#!/usr/bin/python

import sys, getopt
import automata

if __name__ == "__main__":
   source = sys.argv[1]
   dest = open('output.tokens', 'w')

   symbol_table = list()
    
   with open(source) as fp:
      while True:
         token = automata.get_token(fp)
         if not token.has_key('comment'):
            if token.has_key('error'):
               print token.get('error')
               sys.exit()

            if token.has_key('token'):
               dest.write(token.get('token') + '\n')

               if (token.get('token').split(';')[0])[1:] == "id":
                  identifier = (token.get('token').split(';')[1])[:-1]
                  table_entry = {'identifier': identifier} 
                  symbol_table.append(table_entry)

            if token.has_key('eof'):
               print "\n%d lines were scanned, everything is fine!\n" % (token.get('eof'))

               print "SYMBOL TABLE"
               for entry in symbol_table:
                  print "identifier\t%s" % (entry.get('identifier')) 

               sys.exit()

