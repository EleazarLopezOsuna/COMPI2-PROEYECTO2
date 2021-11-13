# Gramatica para primer proyecto 
# Compiladores 2
# Eleazar Jared Lopez Osuna
# 201700893
from Models.SintacticNode import SintacticNode
import sys
import os
import re
from Models.Error import Error
sys.setrecursionlimit(10000)

errores = []
global contador
contador = 0

reservadas = {
    'nothing': 'resNothing',
    'Int64':'resInt64',
    'Float64':'resFloat64',
    'Bool':'resBool',
    'Char':'resChar',
    'String':'resString',
    'log10':'resLog10',
    'log':'resLog',
    'sin':'resSin',
    'cos':'resCos',
    'tan':'resTan',
    'sqrt':'resSqrt',
    'true':'resTrue',
    'false':'resFalse',
    'parse':'resParse',
    'trunc':'resTrunc',
    'float':'resFloat',
    'string':'resStringFunc',
    'typeof':'resTypeof',
    'pop':'resPop',
    'length':'resLength',
    'push':'resPush',
    'print':'resPrint',
    'println':'resPrintln',
    'struct':'resStruct',
    'mutable':'resMutable',
    'end':'resEnd',
    'uppercase':'resUppercase',
    'lowercase':'resLowercase',
    'global':'resGlobal',
    'local':'resLocal',
    'function':'resFuncion',
    'if':'resIf',
    'elseif':'resElseif',
    'else':'resElse',
    'while':'resWhile',
    'for':'resFor',
    'break':'resBreak',
    'continue':'resContinue',
    'return':'resReturn',
    'in':'resIn'
}

tokens = [
    'DOBLEPUNTOS',
    'DOSPUNTOS',
    'IGUAL',
    'PUNTOCOMA',
    'COMA',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'POTENCIA',
    'MODULO',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'OR',
    'AND',
    'NOT',
    'PUNTO',
    'CORCHETEA',
    'CORCHETEC',
    'PARENTESISA',
    'PARENTESISC',
    'ENTERO',
    'FLOTANTE',
    'CADENA',
    'CARACTER',
    'IDENTIFICADOR'
] + list(reservadas.values())

t_DOBLEPUNTOS       = r'\:\:'
t_DOSPUNTOS         = r'\:'
t_IGUAL             = r'\='
t_PUNTOCOMA         = r'\;'
t_COMA              = r'\,'
t_SUMA              = r'\+'
t_RESTA             = r'\-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'\/'
t_POTENCIA          = r'\^'
t_MODULO            = r'\%'
t_MAYOR             = r'\>'
t_MENOR             = r'\<'
t_MAYORIGUAL        = r'\>\='
t_MENORIGUAL        = r'\<\='
t_IGUALIGUAL        = r'\=\='
t_DIFERENTE         = r'\!\='
t_OR                = r'\!\!\!'
t_AND               = r'\&\&'
t_NOT               = r'\!'
t_PUNTO             = r'\.'
t_CORCHETEA         = r'\['
t_CORCHETEC         = r'\]'
t_PARENTESISA       = r'\('
t_PARENTESISC       = r'\)'

def t_FLOTANTE(t):
    r'\d+\.\d+'
    global contador
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    global contador
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value,'IDENTIFICADOR')
    return t

def t_CADENA(t):
    r'(\".*?\")'
    global contador
    t.value = t.value[1:-1]
    return t

def t_CARACTER(t):
    r'(\'.\')'
    global contador
    t.value = t.value[1:-1]
    return t

t_ignore_LINEA = r'\#.*\n'

t_ignore_MULTI = r'\#=(.|\n)+?=\#'

t_ignore = "\t| |\n|\r"

def t_new_line(t):
    r'\n+'
    global contador
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(t)
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'DIVISION', 'MULTIPLICACION', 'MODULO'),
    ('left', 'POTENCIA'),
    ('right', 'NOT')
)

def p_init(t):
    'init : listaInstrucciones'
    global contador
    t[0] = SintacticNode("INICIO", "INICIO", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_listaInstrucciones_1(t):
    'listaInstrucciones : listaInstrucciones instruccion'
    global contador
    t[1].addHijo(t[2])
    t[0] = t[1]
                
def p_listaInstrucciones_2(t):
    'listaInstrucciones : instruccion'
    global contador
    t[0] = SintacticNode("INSTRUCCION", "INSTRUCCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_instruccion_1(t):
    'instruccion    : asignacion PUNTOCOMA'
    global contador
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0] = t[1]

def p_instruccion_2(t):
    'instruccion    : asignacionGlobal PUNTOCOMA'
    global contador
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0] = t[1]

def p_instruccion_3(t):
    'instruccion    : asignacionLocal PUNTOCOMA'
    global contador
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0] = t[1]

def p_instruccion_4(t):
    'instruccion    : llamadaFuncion PUNTOCOMA'
    global contador
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0] = t[1]

def p_instruccion_5(t):
    'instruccion    : struct'
    global contador
    t[0] = t[1]

def p_instruccion_6(t):
    'instruccion    : structMutable'
    global contador
    t[0] = t[1]

def p_instruccion_7(t):
    'instruccion    : declararFuncion'
    global contador
    t[0] = t[1]

def p_instruccion_8(t):
    'instruccion    : instruccionIf'
    global contador
    t[0] = t[1]

def p_instruccion_9(t):
    'instruccion    : instruccionWhile'
    global contador
    t[0] = t[1]

def p_instruccion_10(t):
    'instruccion    : instruccionFor'
    global contador
    t[0] = t[1]

def p_instruccion_11(t):
    'instruccion    : resBreak PUNTOCOMA'
    global contador
    t[0] = SintacticNode("INSTRUCCIONBREAK", "INSTRUCCIONBREAK", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("BREAK", "break", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1

def p_instruccion_12(t):
    'instruccion    : resContinue PUNTOCOMA'
    global contador
    t[0] = SintacticNode("INSTRUCCIONCONTINUE", "INSTRUCCIONCONTINUE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CONTINUE", "continue", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1

def p_instruccion_13(t):
    'instruccion    : retorno PUNTOCOMA'
    global contador
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0] = t[1]

def p_error(t):
    'instruccion    : error PUNTOCOMA'
    global contador
    errores.append(Error(t.lexer.lineno, find_column(input, t), "Lexico", "Error léxico: " + t.value[0]))
    t.lexer.skip(1)

def p_asignacionGlobal(t):
    'asignacionGlobal   : resGlobal asignacion'
    global contador
    t[0] = SintacticNode("GLOBAL", "GLOBAL", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("RESGLOBAL", "global", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_asignacionLocal(t):
    'asignacionLocal    : resLocal asignacion'
    global contador
    t[0] = SintacticNode("LOCAL", "LOCAL", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("RESLOCAL", "local", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_structMutable(t):
    'structMutable  : resMutable struct'
    global contador
    t[0] = SintacticNode("MUTABLE", "MUTABLE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("RESMUTABLE", "mutable", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_retorno(t):
    'retorno    : resReturn expresion'
    global contador
    t[0] = SintacticNode("RETORNO", "RETORNO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("RESRETORNO", "return", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_asignacion_1(t):
    'asignacion : IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IGUAL", "=", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])

def p_asignacion_2(t):
    'asignacion : IDENTIFICADOR IGUAL expresion'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IGUAL", "=", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_asignacion_3(t):
    'asignacion : IDENTIFICADOR accesoFS IGUAL expresion'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(SintacticNode("IGUAL", "=", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])

def p_asignacion_4(t):
    'asignacion : IDENTIFICADOR dimension IGUAL expresion'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(SintacticNode("IGUAL", "=", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])

def p_asignacion_5(t):
    'asignacion : IDENTIFICADOR DOBLEPUNTOS tipo'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_asignacion_6(t):
    'asignacion : IDENTIFICADOR DOBLEPUNTOS tipo IGUAL expresion'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("IGUAL", "=", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])

def p_asignacion_7(t):
    'asignacion : IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("ASIGNACION", "ASIGNACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_llamadaFuncion_1(t):
    'llamadaFuncion : IDENTIFICADOR PARENTESISA listaExpresiones PARENTESISC'
    global contador
    t[0] = SintacticNode("LLAMADAFUNCION", "LLAMADAFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_llamadaFuncion_2(t):
    'llamadaFuncion : IDENTIFICADOR PARENTESISA PARENTESISC'
    global contador
    t[0] = SintacticNode("LLAMADAFUNCION", "LLAMADAFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1

def p_llamadaFuncion_3(t):
    'llamadaFuncion : resPush NOT PARENTESISA expresion COMA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("LLAMADAFUNCION", "LLAMADAFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PUSH", "push", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("NOT", "!", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("COMA", ",", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1
    t[0].addHijo(t[6])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1

def p_llamadaFuncion_4(t):
    'llamadaFuncion : resPrint PARENTESISA listaExpresiones PARENTESISC'
    global contador
    t[0] = SintacticNode("LLAMADAFUNCION", "LLAMADAFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PRINT", "print", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_llamadaFuncion_5(t):
    'llamadaFuncion : resPrintln PARENTESISA listaExpresiones PARENTESISC'
    global contador
    t[0] = SintacticNode("LLAMADAFUNCION", "LLAMADAFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PRINTLN", "println", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_struct(t):
    'struct : resStruct IDENTIFICADOR bloqueStruct resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("STRUCT", "STRUCT", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("RESSTRUCT", "struct", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1

def p_declararFuncion_1(t):
    'declararFuncion    : resFuncion IDENTIFICADOR PARENTESISA listaParametros PARENTESISC listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("DECLARARFUNCION", "DECLARARFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1
    t[0].addHijo(t[6])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(8), find_column(input, t.slice[8]), contador))
    contador += 1

def p_declararFuncion_2(t):
    'declararFuncion    : resFuncion IDENTIFICADOR PARENTESISA PARENTESISC listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("DECLARARFUNCION", "DECLARARFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1

def p_declararFuncion_3(t):
    'declararFuncion    : resFuncion IDENTIFICADOR PARENTESISA listaParametros PARENTESISC DOBLEPUNTOS tipo listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("DECLARARFUNCION", "DECLARARFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1
    t[0].addHijo(t[7])
    t[0].addHijo(t[8])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(9), find_column(input, t.slice[9]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(10), find_column(input, t.slice[10]), contador))
    contador += 1

def p_declararFuncion_4(t):
    'declararFuncion    : resFuncion IDENTIFICADOR PARENTESISA PARENTESISC DOBLEPUNTOS tipo listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("DECLARARFUNCION", "DECLARARFUNCION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[6])
    t[0].addHijo(t[7])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(8), find_column(input, t.slice[8]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(9), find_column(input, t.slice[9]), contador))
    contador += 1

def p_instruccionIf_1(t):
    'instruccionIf  : resIf expresion listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("BLOQUEIF", "BLOQUEIF", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IF", "if", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1

def p_instruccionIf_2(t):
    'instruccionIf  : resIf expresion listaInstrucciones resElse listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("BLOQUEIF", "BLOQUEIF", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IF", "if", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    nodoElse = SintacticNode("ELSE", "ELSE", -1, -1, contador)
    contador += 1
    nodoElse.addHijo(SintacticNode("else", "else", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    nodoElse.addHijo(t[5])
    t[0].addHijo(nodoElse)
    t[0].addHijo(SintacticNode("END", "end", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1

def p_instruccionIf_3(t):
    'instruccionIf  : resIf expresion listaInstrucciones instruccionElseif resElse listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("BLOQUEIF", "BLOQUEIF", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IF", "if", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    nodoElse = SintacticNode("ELSE", "ELSE", -1, -1, contador)
    contador += 1
    nodoElse.addHijo(SintacticNode("else", "else", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1
    nodoElse.addHijo(t[6])
    t[4].addHijo(nodoElse)
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(8), find_column(input, t.slice[8]), contador))
    contador += 1

def p_instruccionIf_4(t):
    'instruccionIf  : resIf expresion listaInstrucciones instruccionElseif resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("BLOQUEIF", "BLOQUEIF", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IF", "if", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1

def p_instruccionElseif_1(t):
    'instruccionElseif  : instruccionElseif resElseif expresion listaInstrucciones'
    global contador
    nodoElseif = SintacticNode("ELSEIF", "ELSEIF", -1, -1, contador)
    contador += 1
    nodoElseif.addHijo(SintacticNode("ELSEIF", "elseif", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    nodoElseif.addHijo(t[3])
    nodoElseif.addHijo(t[4])
    t[1].addHijo(nodoElseif)
    t[0] = t[1]

def p_instruccionElseif_2(t):
    'instruccionElseif  : resElseif expresion listaInstrucciones'
    global contador
    t[0] = SintacticNode("ELSEIF", "ELSEIF", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("ELSEIF", "elseif", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])

def p_instruccionWhile(t):
    'instruccionWhile   : resWhile expresion listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("SWHILE", "SWHILE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("WHILE", "while", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1

def p_instruccionFor(t):
    'instruccionFor : resFor IDENTIFICADOR resIn expresion listaInstrucciones resEnd PUNTOCOMA'
    global contador
    t[0] = SintacticNode("FOR", "FOR", t.lineno(1), find_column(input, t.slice[1]), contador)
    contador += 1
    t[0].addHijo(SintacticNode("for", "for", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IN", "in", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])
    t[0].addHijo(t[5])
    t[0].addHijo(SintacticNode("END", "end", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(7), find_column(input, t.slice[7]), contador))
    contador += 1

def p_expresion_1(t):
    'expresion  : aritmetica'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_expresion_2(t):
    'expresion  : relacionales'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_expresion_3(t):
    'expresion  : logicas'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_expresion_4(t):
    'expresion  : nativa'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_expresion_5(t):
    'expresion  : resTrue'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("TRUE", "true", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_6(t):
    'expresion  : resFalse'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FALSE", "false", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_7(t):
    'expresion  : IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_8(t):
    'expresion  : ENTERO'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("ENTERO", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_9(t):
    'expresion  : CADENA'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CADENA", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_10(t):
    'expresion  : CARACTER'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CARACTER", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_11(t):
    'expresion  : FLOTANTE'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FLOTANTE", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_expresion_14(t):
    'expresion  : llamadaFuncion'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_expresion_15(t):
    'expresion  : CORCHETEA listaExpresiones CORCHETEC'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CORCHETEA", "[", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(SintacticNode("CORCHETEC", "]", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1

def p_expresion_16(t):
    'expresion  : IDENTIFICADOR accesoFS'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_expresion_17(t):
    'expresion  : llamadaFuncion accesoFS'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(t[2])

def p_expresion_19(t):
    'expresion  : PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1

def p_expresion_20(t):
    'expresion  : expresion DOSPUNTOS expresion'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("DOSPUNTOS", ":", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_expresion_21(t):
    'expresion  : IDENTIFICADOR dimension'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_expresion_22(t):
    'expresion   : resNothing'
    global contador
    t[0] = SintacticNode("EXPRESION", "EXPRESION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("NOTHING", "nothing", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_1(t):
    'tipo   : resInt64'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("INT64", "int64", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_2(t):
    'tipo   : resFloat64'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FLOAT64", "float64", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_3(t):
    'tipo   : resBool'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("BOLEANO", "bool", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_4(t):
    'tipo   : resChar'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CHAR", "char", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_5(t):
    'tipo   : resString'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("STRING", "string", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_tipo_6(t):
    'tipo   : IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("TIPO", "TIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_accesoFS_1(t):
    'accesoFS   : accesoFS PUNTO IDENTIFICADOR'
    global contador
    t[1].addHijo(SintacticNode("PUNTO", ".", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[1].addHijo(SintacticNode("IDENTIFICADOR", t[3], t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0] = t[1]

def p_accesoFS_2(t):
    'accesoFS   : PUNTO IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("ACCESOFS", "ACCESOFS", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PUNTO", ".", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[2], t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1

def p_listaParametros_1(t):
    'listaParametros    : listaParametros COMA IDENTIFICADOR'
    global contador
    t[1].addHijo(SintacticNode("COMA", ",", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    nodoParametro = SintacticNode("PARAMETRO", "PARAMETRO", -1, -1, contador)
    contador += 1
    nodoParametro.addHijo(SintacticNode("IDENTIFICADOR", t[3], t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[1].addHijo(nodoParametro)
    t[0] = t[1]

def p_listaParametros_2(t):
    'listaParametros    : listaParametros COMA IDENTIFICADOR DOBLEPUNTOS tipo'
    global contador
    t[1].addHijo(SintacticNode("COMA", ",", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    nodoParametro = SintacticNode("PARAMETRO", "PARAMETRO", -1, -1, contador)
    contador += 1
    nodoParametro.addHijo(SintacticNode("IDENTIFICADOR", t[3], t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    nodoParametro.addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    nodoParametro.addHijo(t[5])
    t[1].addHijo(nodoParametro)
    t[0] = t[1]

def p_listaParametros_3(t):
    'listaParametros    : IDENTIFICADOR DOBLEPUNTOS tipo'
    global contador
    t[0] = SintacticNode("LISTAPARAMETROS", "LISTAPARAMETROS", -1, -1, contador)
    contador += 1
    nodoParametro = SintacticNode("PARAMETRO", "PARAMETRO", -1, -1, contador)
    contador += 1
    nodoParametro.addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    nodoParametro.addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    nodoParametro.addHijo(t[3])
    t[0].addHijo(nodoParametro)

def p_listaParametros_4(t):
    'listaParametros    : IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("LISTAPARAMETROS", "LISTAPARAMETROS", -1, -1, contador)
    contador += 1
    nodoParametro = SintacticNode("PARAMETRO", "PARAMETRO", -1, -1, contador)
    contador += 1
    nodoParametro.addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(nodoParametro)

def p_bloqueStruct(t):
    'bloqueStruct   : bloqueStruct declaracionAtributo PUNTOCOMA'
    global contador
    t[1].addHijo(t[2])
    t[1].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0] = t[1]

def p_bloqueStruct_2(t):
    'bloqueStruct   : declaracionAtributo PUNTOCOMA'
    global contador
    t[0] = SintacticNode("BLOQUESTRUCT", "BLOQUESTRUCT", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("PUNTOCOMA", ";", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1

def p_declaracionAtributo_1(t):
    'declaracionAtributo    : IDENTIFICADOR DOBLEPUNTOS tipo'
    global contador
    t[0] = SintacticNode("ATRIBUTO", "ATRIBUTO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("DOBLEPUNTOS", "::", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_declaracionAtributo_2(t):
    'declaracionAtributo    : IDENTIFICADOR'
    global contador
    t[0] = SintacticNode("ATRIBUTO", "ATRIBUTO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1

def p_dimension_1(t):
    'dimension  : dimension CORCHETEA expresion CORCHETEC'
    global contador
    t[1].addHijo(SintacticNode("CORCHETEA", "[", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[1].addHijo(t[3])
    t[1].addHijo(SintacticNode("CORCHETEC", "]", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0] = t[1]

def p_dimension_2(t):
    'dimension  : CORCHETEA expresion CORCHETEC'
    global contador
    t[0] = SintacticNode("DIMENSION", "DIMENSION", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("CORCHETEA", "[", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])
    t[0].addHijo(SintacticNode("CORCHETEC", "]", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1

def p_listaAsignaciones(t):
    'listaAsignaciones  : listaAsignaciones COMA asignacion'
    global contador
    t[1].addHijo(SintacticNode("COMA", ",", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[1].addHijo(t[3])
    t[0] = t[1]

def p_listaAsignaciones_2(t):
    'listaAsignaciones  : asignacion'
    global contador
    t[0] = SintacticNode("LISTAASIGNACIONES", "LISTAASIGNACIONES", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

def p_aritmetica_1(t):
    'aritmetica : expresion SUMA expresion'
    global contador
    t[0] = SintacticNode("SUMA", "SUMA", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MAS", "+", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_2(t):
    'aritmetica : expresion RESTA expresion'
    global contador
    t[0] = SintacticNode("RESTA", "RESTA", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MENOS", "-", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_3(t):
    'aritmetica : expresion MULTIPLICACION expresion'
    global contador
    t[0] = SintacticNode("MULTIPLICACION", "MULTIPLICACION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("ASTERISCO", "*", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_4(t):
    'aritmetica : expresion DIVISION expresion'
    global contador
    t[0] = SintacticNode("DIVISION", "DIVISION", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("SLASH", "/", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_5(t):
    'aritmetica : expresion POTENCIA expresion'
    global contador
    t[0] = SintacticNode("POTENCIA", "POTENCIA", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("ACENTO", "^", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_6(t):
    'aritmetica : expresion MODULO expresion'
    global contador
    t[0] = SintacticNode("MODULO", "MODULO", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("PORCENTAJE", "%", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_aritmetica_7(t):
    'aritmetica : RESTA expresion'
    global contador
    t[0] = SintacticNode("NEGATIVO", "NEGATIVO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("MENOS", "-", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_nativa_1(t):
    'nativa : resLog10 PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("LOGNATURAL", "LOGNATURAL", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("LOG10", "log10", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_2(t):
    'nativa : resLog PARENTESISA expresion COMA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("LOGBASE", "LOGBASE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("LOG", "log", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("COMA", ",", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1

def p_nativa_3(t):
    'nativa : resSin PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("SENO", "SENO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("SIN", "sin", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_4(t):
    'nativa : resCos PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("COSENO", "COSENO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("COS", "cos", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_5(t):
    'nativa : resTan PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("TANGENTE", "TANGENTE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("TAN", "tan", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_6(t):
    'nativa : resSqrt PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("RAIZ", "RAIZ", t.lineno(1), find_column(input, t.slice[1]), contador)
    contador += 1
    t[0].addHijo(SintacticNode("SQRT", "sqrt", -1, -1, contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_7(t):
    'nativa : resParse PARENTESISA resInt64 COMA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("PARSEINT", "PARSEINT", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PARSE", "parse", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("INT64", "int64", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("COMA", ",", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1

def p_nativa_8(t):
    'nativa : resParse PARENTESISA resFloat64 COMA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("PARSEFLOAT", "PARSEFLOAT", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("PARSE", "parse", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("FLOAT64", "float64", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("COMA", ",", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1
    t[0].addHijo(t[5])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(6), find_column(input, t.slice[6]), contador))
    contador += 1

def p_nativa_9(t):
    'nativa : resTrunc PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("TRUNCAR", "TRUNCAR", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("TRUNC", "trunc", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_10(t):
    'nativa : resFloat PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("CONVERTIRFLOAT", "CONVERTIRFLOAT", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("FLOAT64", "float64", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_11(t):
    'nativa : resStringFunc PARENTESISA expresion PARENTESISC '
    global contador
    t[0] = SintacticNode("CONVERTIRSTRING", "CONVERTIRSTRING", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("STRING", "string", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_12(t):
    'nativa : resTypeof PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("OBTENERTIPO", "OBTENERTIPO", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("TYPEOF", "typeof", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_13(t):
    'nativa : resPop NOT PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("HACERPOP", "HACERPOP", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("POP", "pop", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("DIFERENTE", "!", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(3), find_column(input, t.slice[3]), contador))
    contador += 1
    t[0].addHijo(t[4])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(5), find_column(input, t.slice[5]), contador))
    contador += 1

def p_nativa_14(t):
    'nativa : resLength PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("OBTENERSIZE", "OBTENERSIZE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("LENGTH", "length", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_15(t):
    'nativa : resUppercase PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("HACERUPPERCASE", "HACERUPPERCASE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("UPPERCASE", "uppercase", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_nativa_16(t):
    'nativa : resLowercase PARENTESISA expresion PARENTESISC'
    global contador
    t[0] = SintacticNode("HACERLOWERCASE", "HACERLOWERCASE", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("LOWERCASE", "lowercase", t.lineno(1), find_column(input, t.slice[1]), contador))
    contador += 1
    t[0].addHijo(SintacticNode("PARENTESISA", "(", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])
    t[0].addHijo(SintacticNode("PARENTESISC", ")", t.lineno(4), find_column(input, t.slice[4]), contador))
    contador += 1

def p_relacionales_5(t):
    'relacionales   : expresion IGUALIGUAL expresion'
    global contador
    t[0] = SintacticNode("IGUALDAD", "IGUALDAD", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("IGUALQUE", "==", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_relacionales_6(t):
    'relacionales   : expresion DIFERENTE expresion'
    global contador
    t[0] = SintacticNode("DIFERENCIA", "DIFERENCIA", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("DIFERENTEA", "!=", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_relacionales_1(t):
    'relacionales   : expresion MAYOR expresion'
    global contador
    t[0] = SintacticNode("MAYOR", "MAYOR", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MAYORQUE", ">", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_relacionales_2(t):
    'relacionales   : expresion MENOR expresion'
    global contador
    t[0] = SintacticNode("MENOR", "MENOR", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MENORQUE", "<", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_relacionales_3(t):
    'relacionales   : expresion MAYORIGUAL expresion'
    global contador
    t[0] = SintacticNode("MAYORIGUAL", "MAYORIGUAL", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MAYORIGUALQUE", ">=", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_relacionales_4(t):
    'relacionales   : expresion MENORIGUAL expresion'
    global contador
    t[0] = SintacticNode("MENORIGUAL", "MENORIGUAL", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("MENORIGUALQUE", "<=", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_logicas_1(t):
    'logicas    : expresion OR expresion'
    global contador
    t[0] = SintacticNode("OR", "OR", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("BARRAS", "||", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_logicas_2(t):
    'logicas    : expresion AND expresion'
    global contador
    t[0] = SintacticNode("AND", "AND", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])
    t[0].addHijo(SintacticNode("AMPERSON", "&&", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[3])

def p_logicas_3(t):
    'logicas    : NOT expresion'
    global contador
    t[0] = SintacticNode("NOT", "NOT", -1, -1, contador)
    contador += 1
    t[0].addHijo(SintacticNode("NEGACION", "!", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[0].addHijo(t[2])

def p_listaExpresiones_1(t):
    'listaExpresiones   : listaExpresiones COMA expresion'
    global contador
    t[1].addHijo(SintacticNode("COMA", ",", t.lineno(2), find_column(input, t.slice[2]), contador))
    contador += 1
    t[1].addHijo(t[3])
    t[0] = t[1]

def p_listaExpresiones_2(t):
    'listaExpresiones   : expresion'
    global contador
    t[0] = SintacticNode("LISTAEXPRESIONES", "LISTAEXPRESIONES", -1, -1, contador)
    contador += 1
    t[0].addHijo(t[1])

import ply.yacc as yacc
from Grapher.Tree import Tree
from Models.Symbol import Symbol
from Models.Symbol import EnumType
from Models.Environment import Environment
from Translator.Header import Header
from Translator.secondRead import secondRead
from Translator.AnalizadorC3D import parsear
parser = yacc.yacc()

def getErrores():
    return errores

def parse(inp):
    global errores
    global lexer
    global parser
    errores = []
    global contador
    lexer = lex.lex(reflags = re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    arbol =  Tree()
    root = parser.parse(inp)
    resultado = arbol.getDot(root)
    header = Header(25)
    retorno = []
    second = secondRead(root, 4, header.environment)
    second.startTranslation(second.root)
    header.numeroTemporales = second.actualTemp
    header.generarCodigo()
    cadenaConsola = header.codigo
    cadenaConsola += second.code
    cadenaTemporal = re.sub(r'\/\/.*', '', cadenaConsola)
    cadenaTemporal = re.sub(r'\t', '', cadenaTemporal)
    cadenaPrueba = 'T0 = i + 1;'
    cadenaPrueba += 'T0 = STACK[T0];'
    cadenaPrueba += 'T0 = i + 2;'
    cadenaPrueba += 'T2 = HEAP[T0];'
    cadenaPrueba += 'if (T2 == 36) {goto L1;}'
    cadenaPrueba += 'T1 = T1 + 1;'
    cadenaPrueba += 'HP = HP + 1;'

    #cadenaPrueba = 'L1:'
    #cadenaPrueba += 't1 = 4 * i;'
    #cadenaPrueba += 't2 = a[t1];'
    #cadenaPrueba += 't3 = 4 * i;'
    #cadenaPrueba += 't4 = b[t3];'
    #cadenaPrueba += 't5 = t2 * t4;'
    #cadenaPrueba += 't6 = prod + t5;'
    #cadenaPrueba += 'prod = t6;'
    #cadenaPrueba += 't7 = i + 1;'
    #cadenaPrueba += 'i = t7;'
    #cadenaPrueba += 'if (i<=20) {goto L1;}'

    parsear(cadenaTemporal)
    #parsear(cadenaPrueba)
    if len(errores) == 0:
        # "Environment", "Name", "Type", "Role", "Lower", "Upper", "Absolute", "Relative", "Size", 
        # "Reference", "Row", "Column"
        for environment in second.environmentList:
            addItem(environment, retorno)
    return cadenaConsola, resultado[1], retorno, resultado[0]

def addItem(environment, retorno):
    environment:Environment
    variable:Symbol
    for key in environment.tabla:
        variable = environment.tabla[key]
        retorno.append([variable.root, key, str(variable.type).replace('EnumType.', ''), variable.role, variable.lower, 
        variable.upper, variable.absolute, variable.relative, variable.size, variable.reference, variable.row, variable.column, str(variable.functionType).replace('EnumType.', '')])
        if(variable.type == EnumType.funcion):
            if(variable.atributes != None):
                addItem(variable.atributes, retorno)