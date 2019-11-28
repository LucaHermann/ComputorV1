import ply.lex as lex
import ply.yacc as yacc
import sys

degrees = [0, 0, 0]

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'UNKW'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'

t_ignore = r' '


def t_UNKW(t):
    r'X(\^?[0-9]?)'
    if t.value == "X":
        t.value = "X^1"
    return t


def t_NUMBER(t):
    r'-?\d*\.?\d+'
    if ("." in t.value):
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_error(t):
    print("something went wrong in lexer[{}]".format(t))
    t.lexer.skip(1)


lexer = lex.lex(debug=1)


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


def p_addPlus(p):
    '''
    expression : expression PLUS NUMBER MULTIPLY UNKW
    '''
    degrees[int(p[5].split('^')[1])] += p[3]


def p_addMinus(p):
    '''
    expression : expression MINUS NUMBER MULTIPLY UNKW
    '''
    p[3] = -p[3]
    degrees[int(p[5].split('^')[1])] += p[3]


def p_expression(p):
    '''
      expression : NUMBER MULTIPLY NUMBER
              | NUMBER MINUS NUMBER
              | NUMBER PLUS NUMBER
              | NUMBER DIVIDE NUMBER
              | NUMBER UNKW NUMBER
    '''
    p[0] = (p[1], p[2], p[3])


def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = p[1]


def p_error(p):
    print("something went wrong in parser [{}]".format(p))


parser = yacc.yacc()


def c_calcTrinom(a, b, c):
    delta = b**2-4*a*c
    print("Delta = {}".format(delta))
    if delta > 0:
        x1 = ((-b + delta**0.5) / (2*a))
        x2 = ((-b - delta**0.5) / (2*a))
        print("positive discriminant: x1: {} x2: {}".format(x1, x2))
    elif delta == 0:
        x0 = -b/(2*a)
        print("discriminant equals to 0 x0: {}".format(x0))
    else:
        print("negative discriminant there is no solution")


def c_firstDegree(b, c):
    if c == 0:
        print("there is only one solution and the solution is x1 = 0")
    else:
        print("there is one solution and the solution is", float(-c/b))


while True:
    try:
        s = input('')
    except EOFError:
        break
    if not s:
        print("there is no equation please enter somethings..")
        break
    if '=' in s:
        first, second = s.split('=')
        parser.parse(first)
        degree_first = degrees
        degrees = [0, 0, 0]
        parser.parse(second)
        degree_second = degrees
        a = degree_first[2] - degree_second[2]
        b = degree_first[1] - degree_second[1]
        c = degree_first[0] - degree_second[0]
    if (a == 0 and b == 0 and c != 0):
        print("Really bro there is no solutions")
        break
    else:
        print("Forme réduite : {} * X^2 + {} * X^1 + {} * X^0 = 0".format(a, b, c))
    if a == 0 and b != 0:
        print("Équation du premier degré")
        c_firstDegree(b, c)
    elif (a == 0 and b == 0 and c == 0):
        print("Equation du degré 0")
    else:
        print("Équation du second degré")
        c_calcTrinom(a, b, c)
    degrees = [0, 0, 0]
