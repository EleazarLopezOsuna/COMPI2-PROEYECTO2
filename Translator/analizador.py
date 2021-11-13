# Gramatica para primer proyecto 
# Compiladores 2
# Eleazar Jared Lopez Osuna
# 201700893
from Models.SintacticNode import SintacticNode
import sys
import os
import re
from Models.Error import Error
from Models.GDA import GDA
from Models.lineaCodigo import lineaCodigo
from .optimizacionSimple import optimizacionSimple
sys.setrecursionlimit(10000)

errores = []
global contador
contador = 0
global tabla
tabla = GDA()
simple = optimizacionSimple()

reservadas = {
    'package': 'resPackage',
    'import':'resImport',
    'fmt':'resFmt',
    'math':'resMath',
    'var':'resVar',
    'func':'resFunc',
    'if':'resIf',
    'goto':'resGoto',
    'Mod':'resMod',
    'Printf':'resPrintf',
    'main':'resMain',
    'int':'resInt',
    'float64':'resFloat64',
    'return':'resReturn'
}

tokens = [
    'DOSPUNTOS',
    'IGUAL',
    'PUNTOCOMA',
    'COMA',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'PUNTO',
    'CORCHETEA',
    'CORCHETEC',
    'LLAVEA',
    'LLAVEC',
    'PARENTESISA',
    'PARENTESISC',
    'ENTERO',
    'CADENA',
    'FLOTANTE',
    'IDENTIFICADOR'
] + list(reservadas.values())

t_DOSPUNTOS         = r'\:'
t_IGUAL             = r'\='
t_PUNTOCOMA         = r'\;'
t_COMA              = r'\,'
t_SUMA              = r'\+'
t_RESTA             = r'\-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'\/'
t_MAYOR             = r'\>'
t_MENOR             = r'\<'
t_MAYORIGUAL        = r'\>\='
t_MENORIGUAL        = r'\<\='
t_IGUALIGUAL        = r'\=\='
t_DIFERENTE         = r'\!\='
t_PUNTO             = r'\.'
t_CORCHETEA         = r'\['
t_CORCHETEC         = r'\]'
t_LLAVEA            = r'\{'
t_LLAVEC            = r'\}'
t_PARENTESISA       = r'\('
t_PARENTESISC       = r'\)'

def t_FLOTANTE(t):
    r'-?\d+\.\d+'
    global contador
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'-?\d+'
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

t_ignore_LINEA = r'\/\/.*\n'

t_ignore = "\t| |\r"

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
lexerx = lex.lex()

def p_init(t):
    'init : resPackage resMain import import arreglo arreglo variable variable listaInstrucciones'
    t[0] = tabla
    global contador

def p_import(t):
    'import : resImport PARENTESISA CADENA PARENTESISC PUNTOCOMA'
    linea = t[1] + 'import (' + str(t[3]) + ');'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_arreglo(t):
    'arreglo : resVar IDENTIFICADOR CORCHETEA ENTERO CORCHETEC resFloat64 PUNTOCOMA'
    linea = t[1] + 'var ' + str(t[2]) + '[' + str(t[4]) + '] float64;'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_variable(t):
    'variable : resVar listaVariable resFloat64 PUNTOCOMA'
    linea = t[1] + 'var ' + str(t[2]) + ' float64;'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_listaVariable_1(t):
    'listaVariable : listaVariable COMA IDENTIFICADOR'
    t[0] = str(t[1]) + ', ' + str(t[3])
    global contador

def p_listaVariable_2(t):
    'listaVariable : IDENTIFICADOR'
    t[0] = t[1]
    global contador

def p_listaInstrucciones_1(t):
    'listaInstrucciones : listaInstrucciones instruccion'
    global contador

def p_listaInstrucciones_2(t):
    'listaInstrucciones : instruccion'
    global contador
    
def p_instruccion_1(t):
    'instruccion : function'
    global contador
    
def p_instruccion_2(t):
    'instruccion : temporal PUNTOCOMA'
    global contador
    
def p_instruccion_3(t):
    'instruccion : etiqueta'
    global contador
    
def p_instruccion_4(t):
    'instruccion : ir PUNTOCOMA'
    global contador
    
def p_instruccion_5(t):
    'instruccion : evaluacion'
    global contador   

def p_instruccion_6(t):
    'instruccion : imprimir PUNTOCOMA'
    global contador  

def p_instruccion_7(t):
    'instruccion : llamar PUNTOCOMA'
    global contador

def p_instruccion_8(t):
    'instruccion : acceso PUNTOCOMA'
    global contador

def p_instruccion_9(t):
    'instruccion : resReturn PUNTOCOMA'
    linea = 'return;'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_instriccion_10(t):
    'instruccion : LLAVEC'
    linea = '}'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_function(t):
    'function : resFunc IDENTIFICADOR PARENTESISA PARENTESISC LLAVEA'
    linea = 'func ' + str(t[1]) + '() {'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_function_2(t):
    'function : resFunc resMain PARENTESISA PARENTESISC LLAVEA'
    linea = 'func main() {'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_1(t):
    'temporal : IDENTIFICADOR IGUAL tipo'
    linea = t[1] + ' = ' + str(t[3]) + ';'
    #if (not str(t[1]).lower().startswith('t')) and (str(t[1]) == str(t[3])):
    #    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    #else:
    nuevaLinea = lineaCodigo(t[1], t[3], None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_2(t):
    'temporal : IDENTIFICADOR IGUAL IDENTIFICADOR CORCHETEA resInt PARENTESISA tipo PARENTESISC CORCHETEC'
    linea = t[1] + ' = ' + str(t[3]) + '[int(' + str(t[7]) + ')];'
    #if (not str(t[1]).lower().startswith('t')) and (str(t[1]) == str(t[3])):
    #    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    #else:
    nuevaLinea = lineaCodigo(t[1], t[3], '[]', t[7], linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_3(t):
    'temporal : IDENTIFICADOR IGUAL IDENTIFICADOR CORCHETEA tipo CORCHETEC'
    linea = t[1] + ' = ' + str(t[3]) + '[' + str(t[5]) + '];'
    #if (not str(t[1]).lower().startswith('t')) and (str(t[1]) == str(t[3])):
    #    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    #else:
    nuevaLinea = lineaCodigo(t[1], t[3], '[]', t[5], linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_4(t):
    'temporal : IDENTIFICADOR IGUAL tipo operador tipo'
    linea = t[1] + ' = ' + str(t[3]) + ' ' + str(t[4]) + ' ' + str(t[5]) + ';'
    #if (not str(t[1]).lower().startswith('t')) and (str(t[1]) == str(t[3])):
    #    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    #else:
    nuevaLinea = lineaCodigo(t[1], t[3], t[4], t[5], linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_5(t):
    'temporal : IDENTIFICADOR IGUAL resMath PUNTO resMod PARENTESISA tipo COMA tipo PARENTESISC'
    linea = t[1] + ' = math.Mod(' + str(t[7]) + ', ' + str(t[9]) + ');'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_temporal_6(t):
    'temporal : IDENTIFICADOR IGUAL RESTA tipo'
    linea = t[1] + ' = -' + str(t[4]) + ';'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_tipo_1(t):
    'tipo : ENTERO'
    t[0] = t[1]
    global contador

def p_tipo_2(t):
    'tipo : FLOTANTE'
    t[0] = t[1]
    global contador

def p_tipo_3(t):
    'tipo : IDENTIFICADOR'
    t[0] = t[1]
    global contador

def p_operador_1(t):
    'operador : SUMA'
    t[0] = t[1]
    global contador

def p_operador_2(t):
    'operador : RESTA'
    t[0] = t[1]
    global contador

def p_operador_3(t):
    'operador : MULTIPLICACION'
    t[0] = t[1]
    global contador

def p_operador_4(t):
    'operador : DIVISION'
    t[0] = t[1]
    global contador

def p_operador_5(t):
    'operador : MAYOR'
    t[0] = t[1]
    global contador

def p_operador_6(t):
    'operador : MENOR'
    t[0] = t[1]
    global contador

def p_operador_7(t):
    'operador : MAYORIGUAL'
    t[0] = t[1]
    global contador

def p_operador_8(t):
    'operador : MENORIGUAL'
    t[0] = t[1]
    global contador

def p_operador_9(t):
    'operador : IGUALIGUAL'
    t[0] = t[1]
    global contador

def p_operador_10(t):
    'operador : DIFERENTE'
    t[0] = t[1]
    global contador

def p_etiqueta(t):
    'etiqueta : IDENTIFICADOR DOSPUNTOS'
    linea = 'L' + str(t[1]) + ':'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_ir(t):
    'ir : resGoto IDENTIFICADOR'
    linea = 'goto L' + str(t[2]) + ';'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_evaluacion(t):
    'evaluacion : resIf PARENTESISA tipo operador tipo PARENTESISC LLAVEA resGoto IDENTIFICADOR PUNTOCOMA LLAVEC'
    linea = 'if(' + str(t[3]) + ' ' + str(t[4]) + ' ' + str(t[5]) + ') {goto ' + str(t[9]) + ';}'
    nuevaLinea = lineaCodigo(t[9], t[3], t[4], t[5], linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_imprimir(t):
    'imprimir : resFmt PUNTO resPrintf PARENTESISA CADENA COMA tipo PARENTESISC'
    linea = 'fmt.Printf(' + str(t[5]) + ', ' + str(t[7]) + ');'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_imprimir_2(t):
    'imprimir : resFmt PUNTO resPrintf PARENTESISA CADENA COMA IDENTIFICADOR CORCHETEA resInt PARENTESISA tipo PARENTESISC CORCHETEC PARENTESISC'
    linea = 'fmt.Printf(' + str(t[5]) + ', ' + str(t[7]) + '[int(' + str(t[11]) + ')]);'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_imprimir_3(t):
    'imprimir : resFmt PUNTO resPrintf PARENTESISA CADENA COMA IDENTIFICADOR CORCHETEA tipo CORCHETEC PARENTESISC'
    linea = 'fmt.Printf(' + str(t[5]) + ', ' + str(t[7]) + '[' + str(t[9]) + ']);'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_imprimir_4(t):
    'imprimir : resFmt PUNTO resPrintf PARENTESISA CADENA COMA resInt PARENTESISA tipo PARENTESISC PARENTESISC'
    linea = 'fmt.Printf(' + str(t[5]) + ', int(' + str(t[9]) + '));'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_llamar(t):
    'llamar : IDENTIFICADOR PARENTESISA PARENTESISC'
    linea = str(t[1]) + '();'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_acceso_1(t):
    'acceso : IDENTIFICADOR CORCHETEA resInt PARENTESISA tipo PARENTESISC CORCHETEC IGUAL tipo'
    linea = str(t[1]) + '[int(' + str(t[5]) + ')] = ' + str(t[9]) + ';'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

def p_acceso_2(t):
    'acceso : IDENTIFICADOR CORCHETEA tipo CORCHETEC IGUAL tipo'
    linea = str(t[1]) + '[' + str(t[3]) + '] = ' + str(t[6]) + ';'
    nuevaLinea = lineaCodigo(None, None, None, None, linea)
    simple.agregar(nuevaLinea)
    tabla.agregar(nuevaLinea)
    global contador

import ply.yacc as yacc
from Models.Symbol import Symbol
from Models.Symbol import EnumType
from Models.Environment import Environment
parserx = yacc.yacc()

def getErrores():
    return errores

def parsear(codigo):
    global errores
    global lexerx
    global parserx
    errores = []
    global contador
    lexerx = lex.lex(reflags = re.IGNORECASE)
    parserx = yacc.yacc()
    root = parserx.parse(codigo)
    #root.imprimir()
    #print(root.optimizar())
    retorno = []
    cadenaConsola = ''
    return cadenaConsola