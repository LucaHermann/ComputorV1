import ply.lex as lex  # lexer
import ply.yacc as yacc  # parser
import sys

# calculs
degrees = [0, 0, 0]

# def c_store(p):

# List of token names.
tokens = (
    'INT',
    'FLOAT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'UNKW',
    'EQUALS',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = r' '

# def method for lexer


def t_UNKW(t):
    r'X(\^?[0-9]?)'
    if t.value == "X":
        t.value = "X^1"
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'\d\.\d+'
    t.value = float(t.value)
    return t


def t_error(t):
    print("something went wrong illegal character[lexer]")
    t.lexer.skip(1)


lexer = lex.lex()

# def method for the parser

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)


def p_findFactor(p):
    '''
    expression : expression MULTIPLY UNKW
    '''
    degrees[int(p[3].split('^')[1])] += p[1]
    print(p[1], p[3])
    p[0] = 0


def p_addplus(p):
  '''
  expression : expression PLUS expression MULTIPLY UNKW
  '''

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
              | expression MINUS expression
              | expression PLUS expression
              | expression DIVIDE expression
              | expression UNKW expression
              | expression EQUALS expression
    '''
    p[0] = (p[1], p[2], p[3])
    print(p[1], p[2])


def p_expression_int_float(p):
    '''
    expression : INT
              | FLOAT
    '''
    p[0] = p[1]


def p_error(p):
    print("something went wrong illegal character[{}]".format(p))
    p.parser.skip(1)


parser = yacc.yacc()
# take user input


while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)
    degrees = [0, 0, 0]
