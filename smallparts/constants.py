# -*- coding: utf-8 -*-

"""

smallparts.constants - common constants

"""


#
# Single character constants
#

AMPERSAND = '&'
ASTERISK = '*'
AT = '@'
BLANK = SPACE = SP = ' '
BRACE_OPEN = '{'
BRACE_CLOSE = '}'
COLON = ':'
COMMA = ','
CARRIAGE_RETURN = CR = '\r'
DASH = '-'
DOT = '.'
DOUBLE_QUOTE = '"'
EMPTY = ''
EQUALS = '='
HASH = POUND = '#'
LINEFEED = LF = NEWLINE = NL = '\n'
PERCENT = '%'
PIPE = '|'
PLUS_SIGN = '+'
QUESTION_MARK = '?'
SEMICOLON = ';'
SINGLE_QUOTE = "'"
SLASH = '/'
TILDE = '~'
UNDERSCORE = '_'

#
# Compound constants
#

COLON_BLANK = COLON + BLANK
COMMA_BLANK = COMMA + BLANK
CRLF = CR + LF

#
# Numeric constants
#

ZERO = 0
ONE = 1
FIRST_INDEX = ZERO
SECOND_INDEX = ONE
LAST_INDEX = -1

#
# Encodings
#

ASCII = 'ascii'
CP1252 = 'cp1252'
UTF_8 = 'utf-8'

#
# Functional constants
#

MODE_APPEND = 'a+'
MODE_APPEND_BINARY = 'a+b'
MODE_READ = 'r'
MODE_READ_BINARY = 'rb'
MODE_WRITE = 'w'
MODE_WRITE_BINARY = 'wb'

YES = 'yes'
NO = 'no'

XML_1_0 = '1.0'
XML_1_1 = '1.1'

#
# Return codes
#

RC_ERROR = 1
RC_OK = 0


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
