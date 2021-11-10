# Here we'll read all the code within the functions
# we'll create their 3 address code using the symbol table 
# generated in the first read, all the 3 address code generates in this file
from enum import Enum
from Models.SintacticNode import SintacticNode
from Models.Environment import Environment
from Models.Symbol import EnumType, Symbol
class secondRead():

    def __init__(self, root, maxTemp, environment):
        self.root = root
        self.maxTemp = maxTemp + 1
        self.maxTag = 0
        self.actualTemp = maxTemp
        self.relative = 18
        self.absolute = 18
        self.heap = 0
        self.code = 'func main(){\n'
        self.newLine = '\n'
        self.environment = environment

    def generateCode(self, root):
        if(root.nombre == 'INICIO' or root.nombre == 'INSTRUCCION'):
            for hijo in root.hijos:
                self.generateCode(hijo)
        elif(root.nombre == 'LLAMADAFUNCION'):
            if(root.getHijo(0).nombre == 'PRINT'):
                self.ejecutarPrint(root)
            elif(root.getHijo(0).nombre == 'PRINTLN'):
                self.ejecutarPrint(root)
                self.code += '\tfmt.Printf("%' + 'c", 10); //New line' + self.newLine
            else:
                print()
        elif(root.nombre == 'ASIGNACION'):
            self.ejecutarAsignacion(root)
        elif(root.nombre == 'BLOQUEIF'):
            self.ejecutarIf(root)

    def ejecutarIf(self, root):
        temporalValor = self.resolverExpresion(root.getHijo(1))
        tipoExpresion = self.tipoDato
        if(len(root.hijos) == 5):
            # Es un if sin else y sin elseif
            if(tipoExpresion == EnumType.boleano):
                etiquetaFalsa = self.maxTag
                self.maxTag += 1
                self.code += '\tif T' + str(temporalValor) + ' == 0 {goto L' + str(etiquetaFalsa) + ';} // Condicion Falsa' + self.newLine
                self.generateCode(root.getHijo(2))
                self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
            else:
                # Reportar error
                print('')
        elif(len(root.hijos) == 6):
            if(root.getHijo(3).nombre == 'ELSEIF'):
                # Es un if con elseif
                print('')
            elif(root.getHijo(3).nombre == 'ELSE'):
                # Es un if con else y sin elseif
                if(tipoExpresion == EnumType.boleano):
                    etiquetaFalsa = self.maxTag
                    self.maxTag += 1
                    etiquetaSalida = self.maxTag
                    self.maxTag += 1
                    self.code += '\tif T' + str(temporalValor) + ' == 0 {goto L' + str(etiquetaFalsa) + ';} // Condicion verdadera' + self.newLine
                    self.generateCode(root.getHijo(2))
                    self.code += '\tgoto L' + str(etiquetaSalida) + '; // Salimos de la condicion verdadera' + self.newLine
                    self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
                    self.generateCode(root.getHijo(3).getHijo(1))
                    self.code += '\tL' + str(etiquetaSalida) + ': ' + self.newLine
                else:
                    # Reportar error
                    print('')

            
    def ejecutarPrint(self, root):
        for hijo in root.getHijo(2).hijos:
            if(hijo.nombre == 'EXPRESION'):
                temporalValor = self.resolverExpresion(hijo)
                tipoExpresion = self.tipoDato
                if(tipoExpresion == EnumType.cadena or tipoExpresion == EnumType.caracter):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    self.code += '\tSP = 3; //Change environment' + self.newLine
                    self.code += '\tSTACK[int(SP)] = T' + str(temporalValor) + '; //Give start value to the function' + self.newLine
                    self.code += '\tstringPrint(); //Call function' + self.newLine
                    self.code += '\tSP = T' + str(self.actualTemp) + '; //Set back the previous environment' + self.newLine
                    self.actualTemp += 1
                elif(tipoExpresion == EnumType.entero or tipoExpresion == EnumType.boleano):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save environment' + self.newLine
                    hpActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tif(T' + str(temporalValor) + ' > 0) {goto L' + str(self.maxTag) + ';} // Number is positive' + self.newLine
                    self.code += '\tHEAP[int(HP)] = 45; //Add negative symbol to string' + self.newLine
                    self.code += '\tHP = HP + 1; //Increase HP' + self.newLine
                    self.code += '\tT' + str(temporalValor) + ' = -T' + str(temporalValor) + '; //Set number as positive' + self.newLine
                    self.code += '\tL' + str(self.maxTag) + ': ' + self.newLine
                    self.maxTag += 1
                    self.code += '\t\tSP = 14; //Change environment to intToString function' + self.newLine
                    self.code += '\t\tT' + str(self.actualTemp) + ' = SP + 1; //Stack position for number' + self.newLine
                    self.code += '\t\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Set number value in stack' + self.newLine
                    self.code += '\t\tintToString(); //Call function' + self.newLine
                    self.code += '\t\tT' + str(self.actualTemp) + ' = STACK[int(SP)]; //Get return value' + self.newLine
                    self.code += '\t\tSP = 3; //Change environment to stringPrint function' + self.newLine
                    self.code += '\t\tSTACK[int(SP)] = T' + str(hpActual) + '; //Give start value to the function' + self.newLine
                    self.code += '\t\tstringPrint(); //Call function' + self.newLine
                    self.code += '\t\tSP = T' + str(entornoActual) + '; //Set back the previous environment' + self.newLine

    def ejecutarAsignacion(self, root):
        if(len(root.hijos) == 6):
            # asignacion : IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo (6)
            if(root.getHijo(4).getHijo(0).nombre in ('INT64', 'FLOAT64', 'BOLEANO', 'CHAR', 'STRING')):
                nombreVariable = root.getHijo(0).valor
                hijo = root.getHijo(4).getHijo(0)
                resultado = self.environment.buscar(nombreVariable)
                if(resultado == None):
                    # La variable no existe, debemos crear una
                    if hijo.nombre in ('CHAR', 'STRING'):
                        self.environment.insertar(nombreVariable, Symbol(
                            self.obtenerTipo(hijo.nombre), 'Variable', None, '', '', self.absolute, self.relative, 1, self.heap, hijo.linea, hijo.columna, 'main'
                            ))
                    else:
                        self.environment.insertar(nombreVariable, Symbol(
                            self.obtenerTipo(hijo.nombre), 'Variable', None, '', '', self.absolute, self.relative, 1, '', hijo.linea, hijo.columna, 'main'
                         ))
                    temporalValor = self.resolverExpresion(root.getHijo(2))
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(self.relative) + '; //Get variable relative position' + self.newLine
                    self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                    self.actualTemp += 1
                    self.relative += 1
                else:
                    # La variable si existe debemos modificarla
                    temporalValor = self.resolverExpresion(root.getHijo(2))
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(resultado.relative) + '; //Get variable relative positivon' + self.newLine
                    self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                    self.actualTemp += 1
        elif(len(root.hijos) == 4 and root.getHijo(1).nombre == 'IGUAL'):
            # asignacion : IDENTIFICADOR IGUAL expresion (4)
            nombreVariable = root.getHijo(0).valor
            resultado = self.environment.buscar(nombreVariable)
            if(resultado == None):
                # Reportar error, la variable no existe. Para crearla se debe de indicar un tipo
                print('')
            else:
                # La variable si existe debemos modificarla
                temporalValor = self.resolverExpresion(root.getHijo(2))
                self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(resultado.relative) + '; //Get variable relative positivon' + self.newLine
                self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                self.actualTemp += 1

    def obtenerTipo(self, nombre):
        if nombre == 'INT64':
            return EnumType.entero
        if nombre == 'FLOAT64':
            return EnumType.flotante
        if nombre == 'BOLEANO':
            return EnumType.boleano
        if nombre == 'CHAR':
            return EnumType.caracter
        if nombre == 'STRING':
            return EnumType.cadena

    def resolverExpresion(self, root:SintacticNode):
        if(root.nombre == 'EXPRESION'):
            if(len(root.hijos) == 3 and root.getHijo(0).nombre == 'PARENTESISA'):
                return self.resolverExpresion(root.getHijo(1))
            return self.resolverExpresion(root.getHijo(0))
        elif(root.nombre == 'SUMA'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2))
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' + ' + 'T' + str(operador2) + ';' + self.newLine
                self.actualTemp += 1
                if(tipoOperador1 == EnumType.flotante or tipoOperador2 == EnumType.flotante):
                    self.tipoDato = EnumType.flotante
                else:
                    self.tipoDato = EnumType.entero
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                return 0
        elif(root.nombre == 'RESTA'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2))
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' - ' + 'T' + str(operador2) + ';' + self.newLine
                self.actualTemp += 1
                if(tipoOperador1 == EnumType.flotante or tipoOperador2 == EnumType.flotante):
                    self.tipoDato = EnumType.flotante
                else:
                    self.tipoDato = EnumType.entero
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                return 0
        elif(root.nombre == 'MULTIPLICACION'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2))
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' * ' + 'T' + str(operador2) + ';' + self.newLine
                self.actualTemp += 1
                if(tipoOperador1 == EnumType.flotante or tipoOperador2 == EnumType.flotante):
                    self.tipoDato = EnumType.flotante
                else:
                    self.tipoDato = EnumType.entero
                return (self.actualTemp - 1)
            elif(tipoOperador1 == EnumType.cadena and tipoOperador2 == EnumType.cadena):
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                return 0
        elif(root.nombre == 'DIVISION'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            self.code += '\tif (T' + str(operador2) + ' == 0) {goto L' + str(self.maxTag) + '} //Error division by 0' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' / ' + 'T' + str(operador2) + ';' + self.newLine
            self.code += '\tgoto L' + str((self.maxTag + 1)) + ';' + self.newLine
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.maxTag += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 0 //Set return value to 0' + self.newLine
            self.code += '\t\tDivisionBy0() // Call error message' + self.newLine
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.flotante
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'IGUALDAD'):
            self.code += '//Start -> Area of operation EQUAL' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' == T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation EQUAL' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'DIFERENCIA'):
            self.code += '//Start -> Area of operation NOT EQUAL' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' != T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation NOT EQUAL' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MAYOR'):
            self.code += '//Start -> Area of operation GREATER' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' > T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation GREATER' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MENOR'):
            self.code += '//Start -> Area of operation LESS' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' < T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation LESS' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MAYORIGUAL'):
            self.code += '//Start -> Area of operation GREATER OR EQUAL' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' >= T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation GREATER OR EQUAL' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MENORIGUAL'):
            self.code += '//Start -> Area of operation LESS OR EQUAL' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' <= T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation LESS OR EQUAL' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'OR'):
            self.code += '//Start -> Area of operation OR' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tif(T' + str(operador2) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation OR' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'AND'):
            self.code += '//Start -> Area of operation AND' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            self.code += '\t\tif(T' + str(operador2) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation AND' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'NOT'):
            self.code += '//Start -> Area of operation NOT' + self.newLine
            operador1 = self.resolverExpresion(root.getHijo(1))
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.code += '\t\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.code += '//End -> Area of operation NOT' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1)
        elif(root.nombre == 'POTENCIA'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2))
            tipoOperador2 = self.tipoDato
            if(tipoOperador1 == EnumType.entero or tipoOperador1 == EnumType.flotante):
                if(tipoOperador2 == EnumType.entero):
                    # Operar numberPower
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSP = 11; //Set numberPower environment' + self.newLine
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                    posicionBase = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 2; //Set exponent position' + self.newLine
                    posicionExponente = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSTACK[int(T' + str(posicionBase) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                    self.code += '\tSTACK[int(T' + str(posicionExponente) + ')] = T' + str(operador2) + '; //Set exponent value in stack' + self.newLine
                    self.code += '\tnumberPower(); //Call function' + self.newLine
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                    self.actualTemp += 1
                    self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                    self.tipoDato = tipoOperador1
                    return (self.actualTemp - 1)
                else:
                    # Reportar error
                    self.tipoDato = EnumType.error
                    print('')
            elif(tipoOperador1 == EnumType.cadena):
                if(tipoOperador2 == EnumType.entero):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSP = 8; //Set stringTimes environment' + self.newLine
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                    posicionBase = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 2; //Set exponent position' + self.newLine
                    posicionExponente = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSTACK[int(T' + str(posicionBase) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                    self.code += '\tSTACK[int(T' + str(posicionExponente) + ')] = T' + str(operador2) + '; //Set exponent value in stack' + self.newLine
                    self.code += '\tstringTimes(); //Call function' + self.newLine
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                    self.actualTemp += 1
                    self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                    self.tipoDato = tipoOperador1
                    return (self.actualTemp - 1)
                else:
                    # Reportar error
                    self.tipoDato = EnumType.error
                    print('')
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                print('')
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' + ' + 'T' + str(operador2) + ';' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'ENTERO'):
            self.code += '\tT' + str(self.actualTemp) + ' = ' + str(root.valor) + '; //Value' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.entero
            return (self.actualTemp - 1)
        elif(root.nombre == 'FLOTANTE'):
            self.code += '\tT' + str(self.actualTemp) + ' = ' + str(root.valor) + '; //Value' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.flotante
            return (self.actualTemp - 1)
        elif(root.nombre == 'CADENA'):
            self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save start position' + self.newLine
            self.actualTemp += 1
            for letra in str(root.valor):
                self.code += '\tHEAP[int(HP)] = ' + str(ord(letra)) + '; //Save character \'' + letra + '\' in heap' + self.newLine
                self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
                self.heap += 1
            self.code += '\tHEAP[int(HP)] = 36; //Add end of string' + self.newLine
            self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
            self.tipoDato = EnumType.cadena
            return (self.actualTemp - 1)
        elif(root.nombre == 'CARACTER'):
            self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save start position' + self.newLine
            self.actualTemp += 1
            for letra in str(root.valor):
                self.code += '\tHEAP[int(HP)] = ' + str(ord(letra)) + '; //Save character \'' + letra + '\' in heap' + self.newLine
                self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
                self.heap += 1
            self.code += '\tHEAP[int(HP)] = 36; //Add end of string' + self.newLine
            self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
            self.tipoDato = EnumType.caracter
            return (self.actualTemp - 1)
        elif(root.nombre == 'TRUE'):
            self.code += '\tT' + str(self.actualTemp) + ' = 1; //Value' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'FALSE'):
            self.code += '\tT' + str(self.actualTemp) + ' = 0; //Value' + self.newLine
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'IDENTIFICADOR'):
            nombreVariable = root.valor
            resultado = self.environment.buscar(nombreVariable)
            if(resultado != None):
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[' + str(resultado.relative) + ']; //Guardamos el valor de la variable' + self.newLine
                self.actualTemp += 1
                self.tipoDato = resultado.type
                return (self.actualTemp - 1)
            #Reportar error, la variable no existe
            self.tipoDato = EnumType.error
            return 0
        elif(root.nombre == 'HACERLOWERCASE'):
            operador1 = self.resolverExpresion(root.getHijo(2))
            tipoOperador1 = self.tipoDato
            if(tipoOperador1 == EnumType.cadena):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSP = 4; //Set lowerCase environment' + self.newLine
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                posicionCadena = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSTACK[int(T' + str(posicionCadena) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                self.code += '\tstringLowerCase(); //Call function' + self.newLine
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                self.actualTemp += 1
                self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                self.tipoDato = tipoOperador1
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                print('')
        elif(root.nombre == 'HACERUPPERCASE'):
            operador1 = self.resolverExpresion(root.getHijo(2))
            tipoOperador1 = self.tipoDato
            if(tipoOperador1 == EnumType.cadena):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSP = 6; //Set uppercase environment' + self.newLine
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                posicionCadena = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSTACK[int(T' + str(posicionCadena) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                self.code += '\tstringUpperCase(); //Call function' + self.newLine
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                self.actualTemp += 1
                self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                self.tipoDato = tipoOperador1
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                print('')
        else:
            print(root.nombre)
            
    #def resolverExpresionStack(self, root):
        
    #def resolverExpresionHeap(self, root):
