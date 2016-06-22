#!/usr/bin/python

import grammar as grammar
import error_messages as error

line = 0

def skip_blank(fp):
   symbol = fp.read(grammar.CHAR)
   global line

   while True:
      if not symbol.isspace():
         fp.seek(fp.tell() - 1)
         break

      elif symbol == grammar.NEWLINE:
         line += 1
         
      symbol = fp.read(grammar.CHAR)
# ------------------------------------------------------------------------------


def skip_comment(fp):
   window = fp.read(grammar.CHAR)
   global line

   open_comment_line = line

   while True:
      symbol = fp.read(grammar.CHAR)

      if symbol == grammar.NEWLINE:
         line += 1

      if len(symbol) == 0:
         return {grammar.ERROR: error.MISSING_END_COMMENT % (open_comment_line + 1)} 

      window += symbol

      if window == grammar.OPENCOMMENT:
         return {grammar.ERROR: error.MISSING_END_COMMENT % (open_comment_line + 1)}

      if window != grammar.CLOSECOMMENT:
         window = window[1]
      else:
         break

   return {grammar.COMMENT: grammar.COMMENT}
# ------------------------------------------------------------------------------


def is_alpha(fp, ch):
   """Return an alpha token (identifiers, reserved words and language types)"""
   global line
   symbol = ch
   lexeme = ''

   while True:
      if symbol in grammar.FORBIDDEN:
         return {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

      if symbol in grammar.DELIMITER or \
         symbol in grammar.LOGIC_OP or \
         symbol in grammar.ARIT_OP:
         fp_pos = fp.tell()
         break

      if symbol in grammar.ARIT_OP or symbol == '=':
         fp_pos = fp.tell()
         break

      lexeme += symbol
      symbol = fp.read(grammar.CHAR)

   if lexeme in grammar.DATA_TYPE:
      token = {grammar.TOKEN: "<type;%s>" % (lexeme)}
   elif lexeme in grammar.RESERVED: 
      token = {grammar.TOKEN: "<reserved;%s>" % (lexeme)}
   else:
      token = {grammar.TOKEN: "<%s;id>" % (lexeme)}

   fp.seek(fp_pos - 1)
   return token
# ------------------------------------------------------------------------------


def is_digit(fp, ch):
   """Return a number token"""
   global line
   has_point = False
   symbol = ch
   lexeme = ""
   token = {}
   global line

   while True:
      if symbol in grammar.FORBIDDEN:
         return {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

      if symbol in grammar.DELIMITER:
         fp_pos = fp.tell()
         fp.seek(fp_pos - 1)
         break

      lexeme += symbol

      if symbol.isalpha():
         return {grammar.ERROR: error.ID_OR_NUMBER % (line + 1)}

      if symbol == '.':
         if has_point:
            return {grammar.ERROR: error.EXTRA_DOTS_NUMBER % (line + 1)}
         else:
            has_point = True

         fp_pos = fp.tell()
         symbol = fp.read(grammar.CHAR)

         if not symbol.isdigit():
            return {grammar.ERROR: error.DOT_WITHOUT_NUMBER % (line + 1)}
         else:
            fp.seek(fp_pos)

      if symbol in grammar.DELIMITER:
         break

      symbol = fp.read(grammar.CHAR)
   
   token = {grammar.TOKEN: "<%s;num>" % (lexeme)}
   return token
# ------------------------------------------------------------------------------


def is_arithmetic_op(fp, ch):
   """
      Return an arithmetic token or skip comment
   """
   symbol = ch
   lexeme = symbol

   if symbol in ['*', '#']:
      token = {grammar.TOKEN: "<op_arit;%s>" % lexeme}


   if symbol in ['/', '+', '-']:
      fp_pos = fp.tell()
      lexeme += fp.read(grammar.CHAR)

      if lexeme[1] in grammar.FORBIDDEN:
         return {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

      if lexeme == grammar.OPENCOMMENT:
         token = skip_comment(fp)

      if lexeme in grammar.ARIT_OP:
         token = {grammar.TOKEN: "<op_arit;%s>" % (lexeme)}

      
      if not lexeme[1] in grammar.ARIT_OP:
         token = {grammar.TOKEN: "<op_arit;%s>" % (symbol)}
         fp.seek(fp_pos)


   return token
# ------------------------------------------------------------------------------

def is_logic_op(fp, ch):
   global line
   token = {}

   symbol = ch
   lexeme = symbol + fp.read(1)

   if lexeme[0] in grammar.FORBIDDEN or lexeme[1] in grammar.FORBIDDEN:
      return {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

   if lexeme in grammar.LOGIC_OP:
      token = {grammar.TOKEN: "<op_logic;%s>" % (lexeme)}
   else:
      token = {grammar.ERROR: error.UNKNOWN_LOGIC_OPERATOR % (line + 1, lexeme)}   

   return token
# ------------------------------------------------------------------------------
   

def is_rel_op_or_attr(fp, ch):
   global line

   symbol = ch
   lexeme = symbol
   token = {}

   if lexeme in grammar.LOGIC_OP:
      token = {grammar.TOKEN: "<op_log;%s>" % (lexeme)}

   if lexeme == '=':
      token = {grammar.TOKEN: "<attr;%s>" % (lexeme)}

   if lexeme in grammar.REL_OP:
      token = {grammar.TOKEN: "<op_rel;%s>" % (lexeme)}

   fp_pos = fp.tell()
   lexeme += fp.read(grammar.CHAR)

   if symbol in grammar.FORBIDDEN:
      return {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

   if lexeme in grammar.REL_OP:
      token = {grammar.TOKEN: "<op_rel;%s>" % (lexeme)}
   else:
      fp.seek(fp_pos)
   
   return token
# ------------------------------------------------------------------------------


def is_special_char(fp, ch):
   token = {grammar.TOKEN: "<;%s>" % (ch)}
   return token
# ------------------------------------------------------------------------------


def is_string_char_value(fp, ch):
   symbol = ch
   lexeme = symbol
   global line

   if symbol == grammar.SINGLEQUOTE:
      symbol = fp.read(grammar.CHAR)
      lexeme += symbol

      if symbol == grammar.SINGLEQUOTE:
         return {grammar.ERROR: error.EMPTY_CHAR % (line + 1)}

      symbol = fp.read(grammar.CHAR)

      if not symbol == grammar.SINGLEQUOTE:
         return {grammar.ERROR: error.BIG_CHAR % (line + 1)}
      else:
         lexeme += symbol

      token = {grammar.TOKEN: "<%s;ch>" % (lexeme)}

   else:
      while True:         
         symbol = fp.read(grammar.CHAR)

         if len(symbol) == 0:
            return {grammar.ERROR: error.STRING_EOF % (line + 1)}

         lexeme += symbol

         if symbol == grammar.DOUBLEQUOTE:
            token = {grammar.TOKEN: "<%s;string>" % (lexeme)}
            break

   return token
# ------------------------------------------------------------------------------


def get_token(fp):
   skip_blank(fp)
   symbol = fp.read(grammar.CHAR)
   token = {}
   global line

   if symbol in grammar.QUOTES:
      token = is_string_char_value(fp, symbol)

   elif symbol in grammar.FORBIDDEN:
      token = {grammar.ERROR: error.FORBIDDEN_SYMBOL % (line + 1, symbol)}

   elif symbol.isalpha():      
      token = is_alpha(fp, symbol)

   elif symbol.isdigit():
      token = is_digit(fp, symbol)

   elif symbol in grammar.ARIT_OP:
      token = is_arithmetic_op(fp, symbol)

   elif symbol in grammar.REL_OP or symbol == '=' or symbol == '!':
      token = is_rel_op_or_attr(fp, symbol)

   elif symbol in grammar.SPEC_CHAR:
      token = is_special_char(fp, symbol)

   elif symbol in ['|', '&']:
      token = is_logic_op(fp, symbol)

   elif symbol == grammar.NEWLINE:
      token = {grammar.EOF: line}

   else:
      token = {grammar.ERROR: error.UNKNOWN % (line + 1)}

#   skip_blank(fp)

   return token, line

