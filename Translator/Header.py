# At the moment stack looks like
# absolute | relative | name            | variable
# 0        |    0     | stringConcat    | return
# 1        |    1     | stringConcat    | string 1
# 2        |    2     | stringConcat    | string 2
#-------------------------------------------------------
# 3        |    0     | stringPrint     | string
#-------------------------------------------------------
# 4        |    0     | stringLowerCase | return
# 5        |    1     | stringLowerCase | string
#-------------------------------------------------------
# 6        |    0     | stringUpperCase | return
# 7        |    1     | stringUpperCase | string
#-------------------------------------------------------
# 8        |    0     | stringTimes     | return
# 9        |    1     | stringTimes     | string
# 10       |    2     | stringTimes     | number
#-------------------------------------------------------
# 11       |    0     | numberPower     | return
# 12       |    1     | numberPower     | base
# 13       |    2     | numberPower     | exponent
#-------------------------------------------------------
# 14       |    0     | intToString     | return
# 15       |    1     | intToString     | number
#-------------------------------------------------------
# 16       |    0     | OutOfBounds     | number
#-------------------------------------------------------
# 17       |    0     | DivisionBy0     | number
from .DefaultFunctions import DefaultFunctions
from Models.Environment import Environment
from Models.Symbol import Symbol, EnumType

class Header():

    def __init__(self, numeroTemporales):
        self.numeroTemporales = numeroTemporales
        self.codigo = ''
        self.nuevaLinea = '\n'
        self.environment = Environment(None, 'Global')
        self.environmentList = []
        self.environmentList.append(self.environment)

    def generarCodigo(self):
        self.codigo = 'package main' + self.nuevaLinea
        self.codigo += 'import ("fmt");' + self.nuevaLinea
        self.codigo += 'var STACK[1000000] float64;' + self.nuevaLinea
        self.codigo += 'var HEAP[1000000] float64;' + self.nuevaLinea
        self.codigo += 'var SP, HP float64;' + self.nuevaLinea
        for i in range(self.numeroTemporales + 1):
            if (i == 0):
                self.codigo += 'var T' + str(i)
            elif (i == self.numeroTemporales):
                self.codigo += ', T' + str(i) + ' float64;' + self.nuevaLinea
            else:
                self.codigo += ', T' + str(i)
        defaultFunctions = DefaultFunctions()
        self.codigo += defaultFunctions.stringConcat
        self.codigo += defaultFunctions.stringPrint
        self.codigo += defaultFunctions.stringLowerCase
        self.codigo += defaultFunctions.stringUpperCase
        self.codigo += defaultFunctions.stringTimes
        self.codigo += defaultFunctions.numberPower
        self.codigo += defaultFunctions.operateSum
        self.codigo += defaultFunctions.operateDif
        self.codigo += defaultFunctions.operateMul
        self.codigo += defaultFunctions.operateDiv
        self.codigo += defaultFunctions.intToString
        self.codigo += defaultFunctions.OutOfBounds
        self.codigo += defaultFunctions.DivisionBy0
        # type, role, atributes, lower, upper, absolute, relative, size, reference, row, column, root

        # String Concat
        stringConcatEnv = Environment(self.environment, 'stringConcat')
        stringConcatEnv.insertar('return', Symbol(
            EnumType.cadena, 'Return', None, '', '', '', 0, 1, '', '', '', 'stringConcat'
            ))
        stringConcatEnv.insertar('String1', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'stringConcat'
            ))
        stringConcatEnv.insertar('String2', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 2, 1, '', '', '', 'stringConcat'
            ))
        self.environment.insertar('stringConcat', Symbol(
            EnumType.funcion, 'Funtion', stringConcatEnv, '', '', 0, 0, 3, '', '', '', 'Global'
            ))

        # String Print
        strinPrintEnv = Environment(self.environment, 'strinPrint')
        strinPrintEnv.insertar('String1', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 0, 1, '', '', '', 'stringConcat'
            ))
        self.environment.insertar('strinPrint', Symbol(
            EnumType.funcion, 'Funtion', strinPrintEnv, '', '', 3, 3, 1, '', '', '', 'Global'
            ))

        # String Lower Case
        stringLowerCaseEnv = Environment(self.environment, 'stringLowerCase')
        stringLowerCaseEnv.insertar('return', Symbol(
            EnumType.cadena, 'Return', None, '', '', '', 0, 1, '', '', '', 'stringLowerCase'
            ))
        stringLowerCaseEnv.insertar('String1', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'stringLowerCase'
            ))
        self.environment.insertar('stringLowerCase', Symbol(
            EnumType.funcion, 'Funtion', stringLowerCaseEnv, '', '', 4, 4, 2, '', '', '', 'Global'
            ))

        # String Upper Case
        stringUpperCaseEnv = Environment(self.environment, 'stringUpperCase')
        stringUpperCaseEnv.insertar('return', Symbol(
            EnumType.cadena, 'Return', None, '', '', '', 0, 1, '', '', '', 'stringUpperCase'
            ))
        stringUpperCaseEnv.insertar('String1', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'stringUpperCase'
            ))
        self.environment.insertar('stringUpperCase', Symbol(
            EnumType.funcion, 'Funtion', stringUpperCaseEnv, '', '', 6, 6, 2, '', '', '', 'Global'
            ))

        # String Times
        stringTimesEnv = Environment(self.environment, 'stringTimes')
        stringTimesEnv.insertar('return', Symbol(
            EnumType.cadena, 'Return', None, '', '', '', 0, 1, '', '', '', 'stringTimes'
            ))
        stringTimesEnv.insertar('String1', Symbol(
            EnumType.cadena, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'stringTimes'
            ))
        stringTimesEnv.insertar('Number1', Symbol(
            EnumType.entero, 'Parameter', None, '', '', '', 2, 1, '', '', '', 'stringTimes'
            ))
        self.environment.insertar('stringTimes', Symbol(
            EnumType.funcion, 'Funtion', stringTimesEnv, '', '', 8, 8, 3, '', '', '', 'Global'
            ))

        # Number power
        numberPowerEnv = Environment(self.environment, 'numberPower')
        numberPowerEnv.insertar('return', Symbol(
            EnumType.flotante, 'Return', None, '', '', '', 0, 1, '', '', '', 'numberPower'
            ))
        numberPowerEnv.insertar('Base', Symbol(
            EnumType.flotante, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'numberPower'
            ))
        numberPowerEnv.insertar('Exponent', Symbol(
            EnumType.entero, 'Parameter', None, '', '', '', 2, 1, '', '', '', 'numberPower'
            ))
        self.environment.insertar('numberPower', Symbol(
            EnumType.funcion, 'Funtion', numberPowerEnv, '', '', 11, 11, 3, '', '', '', 'Global'
            ))

        # Int to String
        intToStringEnv = Environment(self.environment, 'intToString')
        intToStringEnv.insertar('return', Symbol(
            EnumType.flotante, 'Return', None, '', '', '', 0, 1, '', '', '', 'intToString'
            ))
        intToStringEnv.insertar('Numero', Symbol(
            EnumType.flotante, 'Parameter', None, '', '', '', 1, 1, '', '', '', 'intToString'
            ))
        self.environment.insertar('intToString', Symbol(
            EnumType.funcion, 'Funtion', intToStringEnv, '', '', 14, 14, 2, '', '', '', 'Global'
            ))

        # Out of bounds
        self.environment.insertar('OutOfBounds', Symbol(
            EnumType.funcion, 'Funtion', None, '', '', 16, 16, 1, '', '', '', 'Global'
            ))
        
        # Division by 0
        self.environment.insertar('DivisionBy0', Symbol(
            EnumType.funcion, 'Funtion', None, '', '', 17, 17, 1, '', '', '', 'Global'
            ))