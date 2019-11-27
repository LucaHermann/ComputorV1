import ply.lex as lex  # lexer
import ply.yacc as yacc  # parser
import sys

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
    'SQRTROOT',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_UNKW = r'X'
t_EQUALS = r'='
t_SQRTROOT = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = r' '

# def method for lexer


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


def p_calc(p):
    '''
    calc : expression
        | empty
    '''
    print(p[1])


def p_expression(p):
    '''
    expression : expression MULTIPLY expression
              | expression MINUS expression
              | expression PLUS expression
              | expression DIVIDE expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_expression_int_float(p):
    '''
    expression : INT
              | FLOAT
    '''
    p[0] = p[1]


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("something went wrong illegal character[parser]")
    p.parser.skip(1)


parser = yacc.yacc()
# take user input


while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)
