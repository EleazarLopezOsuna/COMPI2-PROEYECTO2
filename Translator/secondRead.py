# Here we'll read all the code within the functions
# we'll create their 3 address code using the symbol table 
# generated in the first read, all the 3 address code generates in this file
from enum import Enum
from Models.SintacticNode import SintacticNode
from Models.Environment import Environment
from Models.Symbol import EnumType, Symbol
from Models.OptimizationTable import OptimizationTable
class secondRead():

    def __init__(self, root, maxTemp, environment):
        self.root = root
        self.maxTemp = maxTemp + 1
        self.maxTag = 0
        self.actualTemp = maxTemp
        self.relative = 18
        self.absolute = 18
        self.heap = 0
        self.code = ''
        self.newLine = '\n'
        self.environment = environment
        self.salidaFuncion = 0
        self.environmentList = []
        self.environmentList.append(self.environment)
        self.contadorLineas = 194
        self.optimizationTable = OptimizationTable()
        self.inFunction = 0

    def startTranslation(self, root):
        self.inFunction = 1
        self.firstRead(root, self.environment)
        self.code += 'func main(){' + self.newLine
        self.contadorLineas += 1
        self.code += '\tSP = 18;' + self.newLine
        self.contadorLineas += 1
        self.inFunction = 0
        nuevoEntorno = Environment(self.environment, 'main')
        self.environmentList.append(nuevoEntorno)
        self.generateCode(root, nuevoEntorno)
        self.code += '}' + self.newLine
        self.contadorLineas += 1

    def firstRead(self, root, actual):
        if(root.nombre == 'INICIO' or root.nombre == 'INSTRUCCION'):
            for hijo in root.hijos:
                self.firstRead(hijo, actual)
        elif(root.nombre == 'DECLARARFUNCION'):
            self.ejecutarDeclararFuncion(root, actual)

    def generateCode(self, root, actual):
        if(root.nombre == 'INICIO' or root.nombre == 'INSTRUCCION'):
            for hijo in root.hijos:
                self.generateCode(hijo, actual)
        elif(root.nombre == 'LLAMADAFUNCION'):
            if(root.getHijo(0).nombre == 'PRINT'):
                self.ejecutarPrint(root, actual)
            elif(root.getHijo(0).nombre == 'PRINTLN'):
                self.ejecutarPrint(root, actual)
                self.code += '\tfmt.Printf("%' + 'c", 10); //New line' + self.newLine
                self.contadorLineas += 1
            else:
                self.ejecutarLlamadaFuncion(root, actual)
        elif(root.nombre == 'ASIGNACION'):
            self.ejecutarAsignacion(root, actual)
        elif(root.nombre == 'BLOQUEIF'):
            self.ejecutarIf(root, actual)
        elif(root.nombre == 'FOR'):
            self.ejecutarFor(root, actual)
        elif(root.nombre == 'SWHILE'):
            self.ejecutarWhile(root, actual)
        elif(root.nombre == 'INSTRUCCIONCONTINUE'):
            self.code += '\tgoto L' + str(self.continueTag) + '; //Go to loop start' + self.newLine
            self.contadorLineas += 1
        elif(root.nombre == 'INSTRUCCIONBREAK'):
            self.code += '\tgoto L' + str(self.breakTag) + '; //Go to loop exit' + self.newLine
            self.contadorLineas += 1
        elif(root.nombre == 'RETORNO'):
            self.ejecutarRetorno(root, actual)

    def ejecutarRetorno(self, root, actual):
        operador1 = self.resolverExpresion(root.getHijo(1), actual)
        self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
        self.contadorLineas += 1
        self.actualTemp += 1
        self.code += '\tSTACK[int(T' + str(self.actualTemp - 1) + ')] = T' + str(operador1) + '; //Set return value' + self.newLine
        self.contadorLineas += 1 
        self.code += '\tgoto L' + str(self.salidaFuncion) + '; //Go to end of function' + self.newLine
        self.contadorLineas += 1

    def ejecutarLlamadaFuncion(self, root, actual):
        if(len(root.hijos) == 4):
            # Sin parametros
            nombreFuncion = root.getHijo(0).valor
            resultado = actual.buscar(nombreFuncion)
            size = 0

            # Guardando los temporales
            if(self.inFunction == 1):
                for entorno in self.environmentList:
                    if(entorno.nombre == nombreFuncion):
                        self.code += '// Empieza almacenamiento de parametros' + self.newLine
                        size = len(entorno.tabla)
                        for i in range(self.primerTemporalFuncion, self.actualTemp):
                            self.code += '\tSTACK[int(SP)] = T' + str(i) + '; //Almacenamos el temporal ' + str(i) + self.newLine
                            self.contadorLineas += 1
                            self.code += '\tSP = SP + 1; //Update SP' + self.newLine
                            self.contadorLineas += 1
                            size += 1
            self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save actual environment' + self.newLine
            self.contadorLineas += 1
            valorTemporal = self.actualTemp
            self.actualTemp += 1
            self.code += '\tSP = ' + str(resultado.relative) + '; //Set new environment' + self.newLine
            self.contadorLineas += 1
            self.code += '\t' + nombreFuncion + '(); //Call function ' + nombreFuncion + self.newLine
            self.contadorLineas += 1
            self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Get return position' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str(self.actualTemp - 1) +')]; // Get return value' + self.newLine
            retorno = self.actualTemp
            self.contadorLineas += 1
            self.actualTemp += 1
            #self.code += '\tSP = T' + str(valorTemporal) + '; //Get previous environment back' + self.newLine
            #self.contadorLineas += 1

            # Recuperando los temporales
            if(self.inFunction == 1):
                for entorno in self.environmentList:
                    if(entorno.nombre == nombreFuncion):
                        self.code += '// Empieza almacenamiento de parametros' + self.newLine
                        size = len(entorno.tabla)
                        for i in range(self.primerTemporalFuncion, self.actualTemp):
                            self.code += '\tSTACK[int(SP)] = T' + str(i) + '; //Almacenamos el temporal ' + str(i) + self.newLine
                            self.contadorLineas += 1
                            self.code += '\tSP = SP + 1; //Update SP' + self.newLine
                            self.contadorLineas += 1
                            size += 1
            self.tipoDato = resultado.functionType
            return retorno
        elif(len(root.hijos) == 5):
            # Con parametros
            nombreFuncion = root.getHijo(0).valor
            resultado = actual.buscar(nombreFuncion)
            size = 0
            # Guardando los temporales
            if(self.inFunction == 1):
                self.ultimoTemporalFuncion = self.actualTemp
                self.code += '// Empieza almacenamiento de parametros' + self.newLine
                for i in range(self.primerTemporalFuncion, self.ultimoTemporalFuncion):
                    self.code += '\tSTACK[int(SP)] = T' + str(i) + '; //Almacenamos el temporal ' + str(i) + self.newLine
                    self.contadorLineas += 1
                    if i < (self.ultimoTemporalFuncion - 1):
                        self.code += '\tSP = SP + 1; //Update SP' + self.newLine
                        self.contadorLineas += 1
                    size += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                self.entornoNuevo = self.actualTemp
                self.actualTemp += 1
                self.contadorLineas += 1
                self.code += '\tSP = SP - ' + str(size - 1) + '; //Reset environment' + self.newLine
                self.contadorLineas += 1
                self.code += '// Termina almacenamiento de parametros' + self.newLine
                self.contadorLineas += 1
            contador = 1
            if(resultado.functionType == None):
                contador = 0
            for hijo in root.getHijo(2).hijos:
                if(hijo.nombre == 'EXPRESION'):
                    operador1 = self.resolverExpresion(hijo, actual)
                    tipoOperador1 = self.tipoDato
                    if(tipoOperador1 in (EnumType.entero, EnumType.flotante, EnumType.boleano)):
                        self.code += '\tT' + str(self.actualTemp) + ' = T' + str(self.entornoNuevo) + ' + ' + str(contador) + '; // Set position for variable' + self.newLine
                        self.actualTemp += 1
                        self.contadorLineas += 1
                        self.code += '\tSTACK[int(T' + str(self.actualTemp - 1) + ')] = T' + str(operador1) + '; // Set parameter value' + self.newLine
                        self.contadorLineas += 1
                        contador += 1
                    else:
                        self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save start of new string' + self.newLine
                        posHeap = self.actualTemp
                        self.actualTemp += 1
                        self.contadorLineas += 1
                        self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + '; // Set position for variable' + self.newLine
                        caracter = self.actualTemp
                        self.actualTemp += 1
                        self.contadorLineas += 1
                        self.code += '\tT' + str(self.actualTemp) + ' = T' + str(self.actualTemp - 1) + '; //Start pos' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\tL' + str(self.maxTag) + ': //Loop tag' + self.newLine
                        tagLoop = self.maxTag
                        self.maxTag += 1
                        self.contadorLineas += 1
                        self.code += '\t\tT' + str(caracter) + ' = HEAP[int(T' + str(self.actualTemp) + ')]; //Get caracter' + self.newLine
                        self.contadorLineas += 1
                        tagSalida = self.maxTag
                        self.maxTag += 1
                        self.code += '\t\tif (T' + str(caracter) + ' == 36) {goto L' + str(tagSalida) + ';} //End of string' + self.newLine
                        self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                        self.contadorLineas += 1
                        self.code += '\t\tHEAP[int(HP)] = T' + str(caracter) + '; //Insert character in heap' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\t\tHP = HP + 1; //Increase hp' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\t\tT' + str(self.actualTemp) + ' = T' + str(self.actualTemp) + ' + 1; //Increase index' + self.newLine
                        self.actualTemp += 1
                        self.contadorLineas += 1
                        self.code += '\t\tgoto L' + str(tagLoop) + '; //Go back to loop' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\tL' + str(tagSalida) + ': //End of loop' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\tHEAP[int(HP)] = 36; //Add end of string' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\tHP = HP + 1; //Increase hp' + self.newLine
                        self.contadorLineas += 1
                        self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(contador) + '; // Set position for variable' + self.newLine
                        self.actualTemp += 1
                        self.contadorLineas += 1
                        self.code += '\tSTACK[int(T' + str(self.actualTemp - 1) + ')] = T' + str(posHeap) + '; // Set parameter value' + self.newLine
                        self.contadorLineas += 1
                        contador += 1
            # Finaliza paso de variables
            self.code += '\tSP = T' + str(self.entornoNuevo) + '; //New environment' + self.newLine
            self.contadorLineas += 1
            self.code += '\t' + nombreFuncion + '(); //Call function ' + nombreFuncion + self.newLine
            self.contadorLineas += 1
            self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Get return position' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str(self.actualTemp - 1) +')]; // Get return value' + self.newLine
            retorno = self.actualTemp
            self.contadorLineas += 1
            self.actualTemp += 1
            # Recuperando los temporales
            if(self.inFunction == 1):
                self.code += '// Empieza recuperacion de parametros' + self.newLine
                for i in range(self.primerTemporalFuncion, self.ultimoTemporalFuncion):
                    self.code += '\tT' + str(i) + ' = STACK[int(SP)]; //Almacenamos el temporal ' + str(i) + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(i) + ' = STACK[int(T' + str(i) +')]; //Almacenamos el temporal ' + str(i) + self.newLine
                    self.contadorLineas += 1
                    if i < (self.ultimoTemporalFuncion - 1):
                        self.code += '\tSP = SP - 1; //Update SP' + self.newLine
                        self.contadorLineas += 1
                self.code += '// Termina recuperacion de parametros' + self.newLine
            self.tipoDato = resultado.functionType
            return retorno

    def ejecutarDeclararFuncion(self, root, actual):
        nombreFuncion = root.getHijo(1).valor
        if(len(root.hijos) == 7):
            # Funcion sin parametros y sin retorno
            temporalRelative = self.relative
            self.relative = 0
            nuevoEntorno = self.generarParametros(root.getHijo(3), nombreFuncion, None, root.getHijo(1).linea, root.getHijo(1).columna, actual)
            self.environmentList.append(nuevoEntorno)
            self.code += 'func ' + nombreFuncion + '(){' + self.newLine
            self.contadorLineas += 1
            self.salidaFuncion = self.maxTag
            self.maxTag += 1
            actual.insertar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, self.obtenerTipo(root.getHijo(4).getHijo(0).nombre)
                            ))
            self.primerTemporalFuncion = self.actualTemp
            self.generateCode(root.getHijo(4), nuevoEntorno)
            self.relative = temporalRelative
            actual.modificar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, None
                            ))
            self.relative += len(nuevoEntorno.tabla)
            self.code += '\tSP = SP + ' + str(len(nuevoEntorno.tabla)) + '; //Increase SP' + self.newLine
            self.contadorLineas += len(nuevoEntorno.tabla)
            self.code += '\tgoto L' + str(self.salidaFuncion) + '; //Goto end of function' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(self.salidaFuncion) + ': //End of function' + self.newLine
            self.contadorLineas += 1
            self.maxTag += 1
            self.code += '}' + self.newLine
            self.contadorLineas += 1
        elif(len(root.hijos) == 8):
            if(root.getHijo(4).nombre == 'TIPO'):
                # Funcion sin parametros pero tiene retorno
                tipoFuncion = self.obtenerTipo(root.getHijo(4).getHijo(0).nombre)
                temporalRelative = self.relative
                self.relative = 0
                nuevoEntorno = self.generarParametros(root.getHijo(3), nombreFuncion, tipoFuncion, root.getHijo(1).linea, root.getHijo(1).columna, actual)
                self.environmentList.append(nuevoEntorno)
                self.code += 'func ' + nombreFuncion + '(){' + self.newLine
                self.contadorLineas += 1
                self.relative = len(nuevoEntorno.tabla)
                self.salidaFuncion = self.maxTag
                self.maxTag += 1
                actual.insertar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, self.obtenerTipo(root.getHijo(4).getHijo(0).nombre)
                            ))
                self.primerTemporalFuncion = self.actualTemp
                self.generateCode(root.getHijo(5), nuevoEntorno)
                self.relative = temporalRelative
                actual.modificar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, self.obtenerTipo(root.getHijo(4).getHijo(0).nombre)
                            ))
                self.relative += len(nuevoEntorno.tabla)
                self.code += '\tSP = SP + ' + str(len(nuevoEntorno.tabla)) + '; //Increase SP' + self.newLine
                self.contadorLineas += len(nuevoEntorno.tabla)
                self.code += '\tgoto L' + str(self.salidaFuncion) + '; //Goto end of function' + self.newLine
                self.contadorLineas += 1
                self.code += '\tL' + str(self.salidaFuncion) + ': //End of function' + self.newLine
                self.contadorLineas += 1
                self.maxTag += 1
                self.code += '}' + self.newLine
                self.contadorLineas += 1
            else:
                # Funcion con parametros pero sin retorno
                temporalRelative = self.relative
                self.relative = 0
                nuevoEntorno = self.generarParametros(root.getHijo(3), nombreFuncion, None, root.getHijo(1).linea, root.getHijo(1).columna, actual)
                self.environmentList.append(nuevoEntorno)
                self.code += 'func ' + nombreFuncion + '(){' + self.newLine
                self.contadorLineas += 1
                self.relative = len(nuevoEntorno.tabla)
                self.salidaFuncion = self.maxTag
                self.maxTag += 1
                actual.insertar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, None
                            ))
                self.primerTemporalFuncion = self.actualTemp
                self.generateCode(root.getHijo(5), nuevoEntorno)
                self.relative = temporalRelative
                actual.modificar(nombreFuncion, Symbol(
                            EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, None
                            ))
                self.relative += len(nuevoEntorno.tabla)
                self.code += '\tSP = SP + ' + str(len(nuevoEntorno.tabla)) + '; //Increase SP' + self.newLine
                self.contadorLineas += len(nuevoEntorno.tabla)
                self.code += '\tgoto L' + str(self.salidaFuncion) + '; //Goto end of function' + self.newLine
                self.contadorLineas += 1
                self.code += '\tL' + str(self.salidaFuncion) + ': //End of function' + self.newLine
                self.contadorLineas += 1
                self.maxTag += 1
                self.code += '}' + self.newLine
                self.contadorLineas += 1
        elif(len(root.hijos) == 9):
            # Funcion con parametros y con retorno
            tipoFuncion = self.obtenerTipo(root.getHijo(5).getHijo(0).nombre)
            temporalRelative = self.relative
            self.relative = 0
            nuevoEntorno = self.generarParametros(root.getHijo(3), nombreFuncion, tipoFuncion, root.getHijo(1).linea, root.getHijo(1).columna, actual)
            self.environmentList.append(nuevoEntorno)
            self.code += 'func ' + nombreFuncion + '(){' + self.newLine
            self.contadorLineas += 1
            self.relative = len(nuevoEntorno.tabla)
            self.salidaFuncion = self.maxTag
            self.maxTag += 1
            actual.insertar(nombreFuncion, Symbol(
                EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, tipoFuncion
                ))
            self.primerTemporalFuncion = self.actualTemp
            self.generateCode(root.getHijo(6), nuevoEntorno)
            self.relative = temporalRelative
            actual.modificar(nombreFuncion, Symbol(
                EnumType.funcion, 'Funcion', None, '', '', self.absolute, self.relative, len(nuevoEntorno.tabla),'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, tipoFuncion
                ))
            self.relative += 1
            self.code += '\tSP = SP + 1; //Increase SP' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(self.salidaFuncion) + '; //Goto end of function' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(self.salidaFuncion) + ': //End of function' + self.newLine
            self.contadorLineas += 1
            self.maxTag += 1
            self.code += '}' + self.newLine
            self.contadorLineas += 1

    def generarParametros(self, root, nombreFuncion, tipoRetorno, linea, columna, actual):
        contador = 0
        environment = Environment(actual, nombreFuncion)
        if(tipoRetorno != None):
            environment.insertar('Retorno', Symbol(
                tipoRetorno, 'Retorno', None, '', '', '', contador, 1,'', linea, columna, environment.nombre, None
                ))
            contador += 1
        for hijo in root.hijos:
            if(hijo.nombre == 'PARAMETRO'):
                nombreParametro = hijo.getHijo(0).valor
                tipoParametro = self.obtenerTipo(hijo.getHijo(2).getHijo(0).nombre)
                environment.insertar(nombreParametro, Symbol(
                    tipoParametro, 'Parameter', None, '', '', '', contador, 1,'', hijo.getHijo(0).linea, hijo.getHijo(0).columna, environment.nombre, None
                    ))
                contador += 1
        return environment

    def ejecutarWhile(self, root, actual):
        self.continueTag = inicioCiclo = self.maxTag
        self.maxTag += 1
        self.code += '\tL' + str(inicioCiclo) + ': //Loop start' + self.newLine
        self.contadorLineas += 1
        inicio = self.resolverExpresion(root.getHijo(1), actual)
        self.breakTag = salidaCiclo = self.maxTag
        self.maxTag += 1
        self.code += '\t\tif (T' + str(inicio) + ' == 0) {goto L' + str(salidaCiclo) + ';}' + self.newLine
        self.contadorLineas += 1
        self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
        self.generateCode(root.getHijo(2), actual)
        self.code += '\t\tgoto L' + str(inicioCiclo) + ';' + self.newLine
        self.contadorLineas += 1
        self.code += '\tL' + str(salidaCiclo) + ': ' + self.newLine
        self.contadorLineas += 1

    def ejecutarFor(self, root, actual):
        if(len(root.getHijo(3).hijos) == 3):
            # For para rango
            nombreVariable = root.getHijo(1).valor
            resultado = actual.buscar(nombreVariable)
            if(resultado == None):
                actual.insertar(nombreVariable, Symbol(EnumType.entero, 'Variable', None, '', '', '', self.relative, 1,'', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, None))
                self.relative += 1
                #self.code += '\tSP = SP + 1; //Increase SP' + self.newLine
                #self.contadorLineas += 1
            posicionVariable = (self.relative - 1)
            inicio = self.resolverExpresion(root.getHijo(3).getHijo(0), actual)
            tipoInicio = self.tipoDato
            final = self.resolverExpresion(root.getHijo(3).getHijo(2), actual)
            tipoFinal = self.tipoDato
            if(tipoInicio == EnumType.entero and tipoFinal == EnumType.entero):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(inicio) + '; //Set variable initial value' + self.newLine
                temporalValor = self.actualTemp
                self.actualTemp += 1
                self.code += '\tL' + str(self.maxTag) + ': //Tag to loop' + self.newLine
                self.contadorLineas += 1
                self.continueTag = inicioCiclo = self.maxTag
                self.maxTag += 1
                self.breakTag = salidaCiclo = self.maxTag
                self.maxTag += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(posicionVariable) + ';' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tSTACK[int(' + str(self.actualTemp - 1) + ')] = T' + str(temporalValor) + '; //Set variable initial value' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tif (T' + str(temporalValor) + ' == T' + str(final) + ') {goto L' + str(salidaCiclo) + ';}' + self.newLine
                self.contadorLineas += 1
                self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                self.actualTemp += 1
                self.generateCode(root.getHijo(4), actual)
                self.code += '\t\tT' + str(temporalValor) + ' = T' + str(temporalValor) + ' + 1; //Update variable' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tgoto L' + str(inicioCiclo) + '; //Loop return' + self.newLine
                self.contadorLineas += 1
                self.code += '\tL' + str(salidaCiclo) + ': //End of loop' + self.newLine
                self.contadorLineas += 1
            else:
                # Reportar error
                print('')
        elif(len(root.getHijo(3).hijos) == 1):
            nombreVariable = root.getHijo(1).valor
            resultado = actual.buscar(nombreVariable)
            if(resultado == None):
                actual.insertar(nombreVariable, Symbol(EnumType.caracter, 'Variable', None, '', '', '', self.relative, 1, '', root.getHijo(1).linea, root.getHijo(1).columna, actual.nombre, None))
                self.relative += 1
                #self.code += '\tSP = SP + 1; //Increase SP' + self.newLine
                #self.contadorLineas += 1
            posicionVariable = (self.relative - 1)
            temporalValor = self.resolverExpresion(root.getHijo(3), actual)
            self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(posicionVariable) + '; //Set variable position' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.code += '\tL' + str(self.maxTag) + ': //Tag to loop' + self.newLine
            self.contadorLineas += 1
            self.code += '\tT' + str(self.actualTemp) + ' = HEAP[int(T' + str(temporalValor) + ')]; //Get heap value' + self.newLine
            self.contadorLineas += 1
            self.code += '\tSTACK[int(T' + str(self.actualTemp - 1) + ')] = T' + str(self.actualTemp) + '; //Set variable value' + self.newLine
            self.contadorLineas += 1
            self.inicioCiclo = self.maxTag
            self.maxTag += 1
            self.salidaCiclo = self.maxTag
            self.maxTag += 1
            self.code += '\t\tif (T' + str(self.actualTemp) + ' == 36) {goto L' + str(self.salidaCiclo) + ';}' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.actualTemp += 1
            self.generateCode(root.getHijo(4), actual)
            self.code += '\t\tT' + str(temporalValor) + ' = T' + str(temporalValor) + ' + 1; //Update variable' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tgoto L' + str(self.inicioCiclo) + '; //Loop return' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(self.salidaCiclo) + ': //End of loop' + self.newLine
            self.contadorLineas += 1

    def ejecutarIf(self, root, actual):
        temporalValor = self.resolverExpresion(root.getHijo(1), actual)
        tipoExpresion = self.tipoDato
        if(len(root.hijos) == 5):
            # Es un if sin else y sin elseif
            if(tipoExpresion == EnumType.boleano):
                etiquetaFalsa = self.maxTag
                self.maxTag += 1
                self.code += '\tif (T' + str(temporalValor) + ' == 0) {goto L' + str(etiquetaFalsa) + ';} // Condicion Falsa' + self.newLine
                self.contadorLineas += 1
                self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                self.generateCode(root.getHijo(2), actual)
                self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
                self.contadorLineas += 1
            else:
                # Reportar error
                print('')
        elif(len(root.hijos) == 6):
            if(root.getHijo(3).nombre == 'ELSEIF'):
                # Es un if con elseif
                if(tipoExpresion == EnumType.boleano):
                    self.etiquetaSalida = self.maxTag
                    self.maxTag += 1
                    etiquetaFalsa = self.maxTag
                    self.maxTag += 1
                    self.code += '\tif (T' + str(temporalValor) + ' == 0) {goto L' + str(etiquetaFalsa) + ';} // Condicion Falsa' + self.newLine
                    self.contadorLineas += 1
                    self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                    self.generateCode(root.getHijo(2), actual)
                    self.code += '\tgoto L' + str(self.etiquetaSalida) + '; //Exit tag' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
                    self.contadorLineas += 1
                    self.ejecutarElseIf(root.getHijo(3), actual)
                    self.code += '\tL' + str(self.etiquetaSalida) + ': ' + self.newLine
                    self.contadorLineas += 1
            elif(root.getHijo(3).nombre == 'ELSE'):
                # Es un if con else y sin elseif
                if(tipoExpresion == EnumType.boleano):
                    etiquetaFalsa = self.maxTag
                    self.maxTag += 1
                    etiquetaSalida = self.maxTag
                    self.maxTag += 1
                    self.code += '\tif (T' + str(temporalValor) + ' == 0) {goto L' + str(etiquetaFalsa) + ';} // Condicion verdadera' + self.newLine
                    self.contadorLineas += 1
                    self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                    self.generateCode(root.getHijo(2), actual)
                    self.code += '\tgoto L' + str(etiquetaSalida) + '; // Salimos de la condicion verdadera' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
                    self.contadorLineas += 1
                    self.generateCode(root.getHijo(3).getHijo(1), actual)
                    self.code += '\tL' + str(etiquetaSalida) + ': ' + self.newLine
                    self.contadorLineas += 1
                else:
                    # Reportar error
                    print('')

    def ejecutarElseIf(self, root, actual):
        if(root.valor == 'ELSEIF'):
            temporalValor = self.resolverExpresion(root.getHijo(1), actual)
            tipoExpresion = self.tipoDato
            if(tipoExpresion == EnumType.boleano):
                etiquetaFalsa = self.maxTag
                self.maxTag += 1
                self.code += '\tif (T' + str(temporalValor) + ' == 0) {goto L' + str(etiquetaFalsa) + ';} // Condicion Falsa' + self.newLine
                self.contadorLineas += 1
                self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                self.generateCode(root.getHijo(2), actual)
                self.code += '\tgoto L' + str(self.etiquetaSalida) + '; //Exit tag' + self.newLine
                self.contadorLineas += 1
                self.code += '\tL' + str(etiquetaFalsa) + ': ' + self.newLine
                self.contadorLineas += 1
            else:
                # Reportar error
                print('')
        elif(root.valor == 'ELSE'):
            self.generateCode(root.getHijo(1), actual)
        for hijo in root.hijos:
            self.ejecutarElseIf(hijo, actual)
            
    def ejecutarPrint(self, root, actual):
        for hijo in root.getHijo(2).hijos:
            if(hijo.nombre == 'EXPRESION'):
                temporalValor = self.resolverExpresion(hijo, actual)
                tipoExpresion = self.tipoDato
                if(tipoExpresion == EnumType.cadena):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSP = 3; //Change environment' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSTACK[int(SP)] = T' + str(temporalValor) + '; //Give start value to the function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tstringPrint(); //Call function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSP = T' + str(self.actualTemp) + '; //Set back the previous environment' + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                elif(tipoExpresion == EnumType.caracter):
                    self.code += '\tfmt.Printf("%' + 'c", int(T' + str(temporalValor) + ')); //Give start value to the function' + self.newLine
                    self.contadorLineas += 1
                elif(tipoExpresion == EnumType.entero or tipoExpresion == EnumType.boleano):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    self.contadorLineas += 1
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save environment' + self.newLine
                    self.contadorLineas += 1
                    hpActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tif (T' + str(temporalValor) + ' >= 0) {goto L' + str(self.maxTag) + ';} // Number is positive' + self.newLine
                    self.contadorLineas += 1
                    self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                    self.code += '\tHEAP[int(HP)] = 45; //Add negative symbol to string' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tHP = HP + 1; //Increase HP' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(temporalValor) + ' = -T' + str(temporalValor) + '; //Set number as positive' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tL' + str(self.maxTag) + ': ' + self.newLine
                    self.contadorLineas += 1
                    self.maxTag += 1
                    self.code += '\t\tSP = 14; //Change environment to intToString function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tT' + str(self.actualTemp) + ' = SP + 1; //Stack position for number' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Set number value in stack' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tintToString(); //Call function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tT' + str(self.actualTemp) + ' = STACK[int(SP)]; //Get return value' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tSP = 3; //Change environment to stringPrint function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tSTACK[int(SP)] = T' + str(hpActual) + '; //Give start value to the function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tstringPrint(); //Call function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\t\tSP = T' + str(entornoActual) + '; //Set back the previous environment' + self.newLine
                    self.contadorLineas += 1

    def ejecutarAsignacion(self, root, actual):
        if(len(root.hijos) == 6):
            # asignacion : IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo (6)
            if(root.getHijo(4).getHijo(0).nombre in ('INT64', 'FLOAT64', 'BOLEANO', 'CHAR', 'STRING')):
                nombreVariable = root.getHijo(0).valor
                hijo = root.getHijo(4).getHijo(0)
                resultado = actual.buscar(nombreVariable)
                if(resultado == None):
                    # La variable no existe, debemos crear una
                    if hijo.nombre in ('CHAR', 'STRING'):
                        actual.insertar(nombreVariable, Symbol(
                            self.obtenerTipo(hijo.nombre), 'Variable', None, '', '', self.absolute, self.relative, 1,'', hijo.linea, hijo.columna, actual.nombre, None
                            ))
                    else:
                        actual.insertar(nombreVariable, Symbol(
                            self.obtenerTipo(hijo.nombre), 'Variable', None, '', '', self.absolute, self.relative, 1, '', hijo.linea, hijo.columna, actual.nombre, None
                         ))
                    temporalValor = self.resolverExpresion(root.getHijo(2), actual)
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(self.relative) + '; //Get variable relative position' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                    self.relative += 1
                    self.code += '\tSP = SP + 1; //Increase SP' + self.newLine
                    self.contadorLineas += 1
                else:
                    # La variable si existe debemos modificarla
                    temporalValor = self.resolverExpresion(root.getHijo(2), actual)
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(resultado.relative) + '; //Get variable relative positivon' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
        elif(len(root.hijos) == 4 and root.getHijo(1).nombre == 'IGUAL'):
            # asignacion : IDENTIFICADOR IGUAL expresion (4)
            nombreVariable = root.getHijo(0).valor
            resultado = actual.buscar(nombreVariable)
            if(resultado == None):
                # Reportar error, la variable no existe. Para crearla se debe de indicar un tipo
                print('')
            else:
                # La variable si existe debemos modificarla
                temporalValor = self.resolverExpresion(root.getHijo(2), actual)
                self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(resultado.relative) + '; //Get variable relative positivon' + self.newLine
                self.contadorLineas += 1
                self.code += '\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Stack position for variable: ' + nombreVariable + self.newLine
                self.contadorLineas += 1
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

    def resolverExpresion(self, root:SintacticNode, actual):
        if(root.nombre == 'EXPRESION'):
            if(len(root.hijos) == 3 and root.getHijo(0).nombre == 'PARENTESISA'):
                return self.resolverExpresion(root.getHijo(1), actual)
            return self.resolverExpresion(root.getHijo(0), actual)
        elif(root.nombre == 'SUMA'):
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' + ' + 'T' + str(operador2) + ';' + self.newLine
                self.contadorLineas += 1
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
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' - ' + 'T' + str(operador2) + ';' + self.newLine
                self.contadorLineas += 1
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
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador2 = self.tipoDato
            if((tipoOperador1 == EnumType.entero in (EnumType.entero, EnumType.flotante)) and (tipoOperador2 == EnumType.entero in (EnumType.entero, EnumType.flotante))):
                self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' * ' + 'T' + str(operador2) + ';' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                if(tipoOperador1 == EnumType.flotante or tipoOperador2 == EnumType.flotante):
                    self.tipoDato = EnumType.flotante
                else:
                    self.tipoDato = EnumType.entero
                return (self.actualTemp - 1)
            elif(tipoOperador1 == EnumType.cadena and tipoOperador2 == EnumType.cadena):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                self.contadorLineas += 1
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSP = 0; //Set stringConcat environment' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                self.contadorLineas += 1
                posicionBase = self.actualTemp
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 2; //Set exponent position' + self.newLine
                self.contadorLineas += 1
                posicionExponente = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSTACK[int(T' + str(posicionBase) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                self.contadorLineas += 1
                self.code += '\tSTACK[int(T' + str(posicionExponente) + ')] = T' + str(operador2) + '; //Set exponent value in stack' + self.newLine
                self.contadorLineas += 1
                self.code += '\tstringConcat(); //Call function' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                self.contadorLineas += 1
                self.tipoDato = tipoOperador1
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                return 0
        elif(root.nombre == 'DIVISION'):
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            self.code += '\tif (T' + str(operador2) + ' == 0) {goto L' + str(self.maxTag) + '} //Error division by 0' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' / ' + 'T' + str(operador2) + ';' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str((self.maxTag + 1)) + ';' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.contadorLineas += 1
            self.maxTag += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 0 //Set return value to 0' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tDivisionBy0() // Call error message' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.flotante
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'IGUALDAD'):
            self.code += '//Start -> Area of operation EQUAL' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' == T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation EQUAL' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'DIFERENCIA'):
            self.code += '//Start -> Area of operation NOT EQUAL' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' != T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation NOT EQUAL' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MAYOR'):
            self.code += '//Start -> Area of operation GREATER' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' > T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation GREATER' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MENOR'):
            self.code += '//Start -> Area of operation LESS' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' < T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation LESS' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MAYORIGUAL'):
            self.code += '//Start -> Area of operation GREATER OR EQUAL' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' >= T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation GREATER OR EQUAL' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'MENORIGUAL'):
            self.code += '//Start -> Area of operation LESS OR EQUAL' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' <= T' + str(operador2) + ') {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation LESS OR EQUAL' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'OR'):
            self.code += '//Start -> Area of operation OR' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tif (T' + str(operador2) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation OR' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'AND'):
            self.code += '//Start -> Area of operation AND' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif(T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            self.code += '\t\tif (T' + str(operador2) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation AND' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'NOT'):
            self.code += '//Start -> Area of operation NOT' + self.newLine
            self.contadorLineas += 1
            operador1 = self.resolverExpresion(root.getHijo(1), actual)
            etiquetaVerdadera = self.maxTag
            self.maxTag += 1
            etiquetaSalida = self.maxTag
            self.maxTag += 1
            self.code += '\tif (T' + str(operador1) + ' == 1) {' + 'goto L' + str(etiquetaVerdadera) + ';} //goto true tag' + self.newLine
            self.contadorLineas += 1
            self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
            self.code += '\tT' + str(self.actualTemp) + ' = 1;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tgoto L' + str(etiquetaSalida) + '; //Goto exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaVerdadera) + ': //True tag' + self.newLine
            self.contadorLineas += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 0;' + self.newLine
            self.contadorLineas += 1
            self.code += '\tL' + str(etiquetaSalida) + ': //Exit tag' + self.newLine
            self.contadorLineas += 1
            self.code += '//End -> Area of operation NOT' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            return (self.actualTemp - 1)
        elif(root.nombre == 'POTENCIA'):
            operador1 = self.resolverExpresion(root.getHijo(0), actual)
            tipoOperador1 = self.tipoDato
            operador2 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador2 = self.tipoDato
            if(tipoOperador1 == EnumType.entero or tipoOperador1 == EnumType.flotante):
                if(tipoOperador2 == EnumType.entero):
                    # Operar numberPower
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    self.contadorLineas += 1
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSP = 11; //Set numberPower environment' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                    self.contadorLineas += 1
                    posicionBase = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 2; //Set exponent position' + self.newLine
                    self.contadorLineas += 1
                    posicionExponente = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSTACK[int(T' + str(posicionBase) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSTACK[int(T' + str(posicionExponente) + ')] = T' + str(operador2) + '; //Set exponent value in stack' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tnumberPower(); //Call function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                    self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                    self.contadorLineas += 1
                    self.tipoDato = tipoOperador1
                    return (self.actualTemp - 1)
                else:
                    # Reportar error
                    self.tipoDato = EnumType.error
                    print('')
            elif(tipoOperador1 == EnumType.cadena):
                if(tipoOperador2 == EnumType.entero):
                    self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                    self.contadorLineas += 1
                    entornoActual = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSP = 8; //Set stringTimes environment' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                    self.contadorLineas += 1
                    posicionBase = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 2; //Set exponent position' + self.newLine
                    self.contadorLineas += 1
                    posicionExponente = self.actualTemp
                    self.actualTemp += 1
                    self.code += '\tSTACK[int(T' + str(posicionBase) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tSTACK[int(T' + str(posicionExponente) + ')] = T' + str(operador2) + '; //Set exponent value in stack' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tstringTimes(); //Call function' + self.newLine
                    self.contadorLineas += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                    self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                    self.contadorLineas += 1
                    self.actualTemp += 1
                    self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                    self.contadorLineas += 1
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
            self.contadorLineas += 1
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'ENTERO'):
            self.code += '\tT' + str(self.actualTemp) + ' = ' + str(root.valor) + '; //Value' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.entero
            return (self.actualTemp - 1)
        elif(root.nombre == 'FLOTANTE'):
            self.code += '\tT' + str(self.actualTemp) + ' = ' + str(root.valor) + '; //Value' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.flotante
            return (self.actualTemp - 1)
        elif(root.nombre == 'CADENA'):
            self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save start position' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            for letra in str(root.valor):
                self.code += '\tHEAP[int(HP)] = ' + str(ord(letra)) + '; //Save character \'' + letra + '\' in heap' + self.newLine
                self.contadorLineas += 1
                self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
                self.contadorLineas += 1
                self.heap += 1
            self.code += '\tHEAP[int(HP)] = 36; //Add end of string' + self.newLine
            self.contadorLineas += 1
            self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
            self.contadorLineas += 1
            self.tipoDato = EnumType.cadena
            return (self.actualTemp - 1)
        elif(root.nombre == 'CARACTER'):
            self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save start position' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            for letra in str(root.valor):
                self.code += '\tHEAP[int(HP)] = ' + str(ord(letra)) + '; //Save character \'' + letra + '\' in heap' + self.newLine
                self.contadorLineas += 1
                self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
                self.contadorLineas += 1
                self.heap += 1
            self.code += '\tHEAP[int(HP)] = 36; //Add end of string' + self.newLine
            self.contadorLineas += 1
            self.code += '\tHP = HP + 1; //Increase heap' + self.newLine
            self.contadorLineas += 1
            self.tipoDato = EnumType.caracter
            return (self.actualTemp - 1)
        elif(root.nombre == 'TRUE'):
            self.code += '\tT' + str(self.actualTemp) + ' = 1; //Value' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'FALSE'):
            self.code += '\tT' + str(self.actualTemp) + ' = 0; //Value' + self.newLine
            self.contadorLineas += 1
            self.actualTemp += 1
            self.tipoDato = EnumType.boleano
            return (self.actualTemp - 1)
        elif(root.nombre == 'IDENTIFICADOR'):
            nombreVariable = root.valor
            resultado = actual.buscar(nombreVariable)
            if(resultado != None):
                self.code += '\tT' + str(self.actualTemp) + ' = SP + ' + str(resultado.relative) + '; //Set variable position' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str(self.actualTemp - 1) + ')]; //Guardamos el valor de la variable' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.tipoDato = resultado.type
                return (self.actualTemp - 1)
            #Reportar error, la variable no existe
            self.tipoDato = EnumType.error
            return 0
        elif(root.nombre == 'HACERLOWERCASE'):
            operador1 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador1 = self.tipoDato
            if(tipoOperador1 == EnumType.cadena):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                self.contadorLineas += 1
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSP = 4; //Set lowerCase environment' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                self.contadorLineas += 1
                posicionCadena = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSTACK[int(T' + str(posicionCadena) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                self.contadorLineas += 1
                self.code += '\tstringLowerCase(); //Call function' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                self.contadorLineas += 1
                self.tipoDato = tipoOperador1
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                print('')
        elif(root.nombre == 'HACERUPPERCASE'):
            operador1 = self.resolverExpresion(root.getHijo(2), actual)
            tipoOperador1 = self.tipoDato
            if(tipoOperador1 == EnumType.cadena):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                self.contadorLineas += 1
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSP = 6; //Set uppercase environment' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 1; //Set base position' + self.newLine
                self.contadorLineas += 1
                posicionCadena = self.actualTemp
                self.actualTemp += 1
                self.code += '\tSTACK[int(T' + str(posicionCadena) + ')] = T' + str(operador1) + '; //Set base value in stack' + self.newLine
                self.contadorLineas += 1
                self.code += '\tstringUpperCase(); //Call function' + self.newLine
                self.code += '\tT' + str(self.actualTemp) + ' = SP + 0; //Set return position' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = STACK[int(T' + str((self.actualTemp - 1)) + ')]; //Get return value' + self.newLine
                self.contadorLineas += 1
                self.actualTemp += 1
                self.code += '\tSP = T' + str(entornoActual) + '; //Get environment back' + self.newLine
                self.contadorLineas += 1
                self.tipoDato = tipoOperador1
                return (self.actualTemp - 1)
            else:
                # Reportar error
                self.tipoDato = EnumType.error
                print('')
        elif(root.nombre == 'NEGATIVO'):
            operador1 = self.resolverExpresion(root.getHijo(1), actual)
            self.code += '\tT' + str(operador1) + ' = -1 * T' + str(operador1) + '; //Set number as negative' + self.newLine
            self.contadorLineas += 1
            return operador1
        elif(root.nombre == 'LLAMADAFUNCION'):
            root.addHijo(SintacticNode("", "", 0, 0, root.numero * 2))
            return self.ejecutarLlamadaFuncion(root, actual)
        elif(root.nombre == 'CONVERTIRSTRING'):
            operador1 = self.resolverExpresion(root.getHijo(2), actual)
            temporalValor = operador1
            tipoOperador1 = self.tipoDato
            if(tipoOperador1 == EnumType.entero):
                self.code += '\tT' + str(self.actualTemp) + ' = SP; //Save environment' + self.newLine
                self.contadorLineas += 1
                entornoActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tT' + str(self.actualTemp) + ' = HP; //Save environment' + self.newLine
                self.contadorLineas += 1
                hpActual = self.actualTemp
                self.actualTemp += 1
                self.code += '\tif (T' + str(temporalValor) + ' >= 0) {goto L' + str(self.maxTag) + ';} // Number is positive' + self.newLine
                self.contadorLineas += 1
                self.optimizationTable.insertar('', '', self.contadorLineas, 'Creacion de codigo', 'Mirilla - Regla 3')
                self.code += '\tHEAP[int(HP)] = 45; //Add negative symbol to string' + self.newLine
                self.contadorLineas += 1
                self.code += '\tHP = HP + 1; //Increase HP' + self.newLine
                self.contadorLineas += 1
                self.code += '\tT' + str(temporalValor) + ' = -T' + str(temporalValor) + '; //Set number as positive' + self.newLine
                self.contadorLineas += 1
                self.code += '\tL' + str(self.maxTag) + ': ' + self.newLine
                self.contadorLineas += 1
                self.maxTag += 1
                self.code += '\t\tSP = 14; //Change environment to intToString function' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tT' + str(self.actualTemp) + ' = SP + 1; //Stack position for number' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tSTACK[int(T' + str(self.actualTemp) + ')] = T' + str(temporalValor) + '; //Set number value in stack' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tintToString(); //Call function' + self.newLine
                self.contadorLineas += 1
                self.code += '\t\tT' + str(self.actualTemp) + ' = STACK[int(SP)]; //Get return value' + self.newLine
                self.actualTemp += 1
                self.contadorLineas += 1
                self.code += '\t\tSP = T' + str(entornoActual) + '; //Set back the previous environment' + self.newLine
                self.contadorLineas += 1
                self.tipoDato = EnumType.cadena
                return (hpActual)
        else:
            self.tipoDato = None
            print(root.nombre)