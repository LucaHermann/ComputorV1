import ply.lex as lex  # lexer
import ply.yacc as yacc  # parser
import sys

# suivant la puissance de l'inconnu (1er, 2eme ou pas de puissance(0))
# l'inconnu est rangée dans degrees a lindex correspondant
degrees = [0, 0, 0]

# def c_store(p):

# Liste des noms de tokens.
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'UNKW',
    'LPAREN',
    'RPAREN',
)

# definitions des regles regexpr pour les tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = r' '


def t_UNKW(t):
    r'X(\^?[0-9]?)'
    if t.value == "X":
        t.value = "X^1"
    return t
# si dans l'expression je trouve une inconnue


def t_NUMBER(t):
    r'-?\d*\.?\d+'
    if ("." in t.value):
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_error(t):
    print("something went wrong in lexer")
    t.lexer.skip(1)
# si dans l'expression je trouve une erreur


lexer = lex.lex()
# creation du lexer

# definition de regles de calculs primaires
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)


def p_findFactor(p):
    '''
    expression : NUMBER MULTIPLY UNKW
    '''
    degrees[int(p[3].split('^')[1])] += p[1]
    p[0] = 0
    print('--degrees in findFactor-- :', degrees)
# si mon expression est multiplier par une inconnue je recupere linconnu et la classe dans degrees


def p_addPlus(p):
    '''
    expression : expression PLUS NUMBER MULTIPLY UNKW
    '''
    degrees[int(p[5].split('^')[1])] += p[3]
    print('--degrees in addPlus-- :', degrees)


def p_addMinus(p):
    '''
    expression : expression MINUS NUMBER MULTIPLY UNKW
    '''
    degrees[int(p[5].split('^')[1])] += p[3]
    print('--degrees in addMinus-- :', degrees)


def p_expression(p):
    '''
    expression : NUMBER MULTIPLY NUMBER
              | NUMBER MINUS NUMBER
              | NUMBER PLUS NUMBER
              | NUMBER DIVIDE NUMBER
              | NUMBER UNKW NUMBER
    '''
    p[0] = (p[1], p[2], p[3])
    print('p_expression', p[1], p[2])


def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = p[1]


def p_error(p):
    print("something went wrong in parser [{}]".format(p))
    p.parser.skip(1)


parser = yacc.yacc()
# equivalence d'un main


while True:
    try:
        s = input('')
    except EOFError:
        break
    if ('=' in s):
        first, second = s.split('=')
        parser.parse(first)
        parser.parse(second)
        degrees = [0, 0, 0]
    else:
        print("input got the wrong format please input other calculs")
