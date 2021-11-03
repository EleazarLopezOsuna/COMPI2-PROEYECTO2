# Here we'll read all the code within the functions
# we'll create their 3 address code using the symbol table 
# generated in the first read, all the 3 address code generates in this file
from Models.SintacticNode import SintacticNode
from Models.Environment import Environment
class secondRead():

    def __init__(self, root, maxTemp, environment):
        self.root = root
        self.maxTemp = maxTemp + 1
        self.maxTag = 0
        self.actualTemp = 0
        self.code = 'func main(){\n'
        self.newLine = '\n'
        self.environment = environment

    def generateCode(self, root):
        if(root.nombre == 'INICIO' or root.nombre == 'INSTRUCCION'):
            for hijo in root.hijos:
                self.generateCode(hijo)
        elif(root.nombre == 'ASIGNACION'):
            if(len(root.hijos) == 6):
                # asignacion : IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo (6)
                if(root.getHijo(4).getHijo(0).nombre in ('INT64', 'FLOAT64', 'BOLEANO', 'CHAR', 'STRING')):
                    # Se almacena en stack
                    temporalValor = self.resolverExpresion(root.getHijo(2))

    def resolverExpresion(self, root:SintacticNode):
        print(root.nombre)
        if(root.nombre == 'EXPRESION'):
            return self.resolverExpresion(root.getHijo(0))
        elif(root.nombre == 'SUMA'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' + ' + 'T' + str(operador2) + ';' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'RESTA'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' - ' + 'T' + str(operador2) + ';' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'MULTIPLICACION'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' * ' + 'T' + str(operador2) + ';' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'DIVISION'):
            operador1 = self.resolverExpresion(root.getHijo(0))
            operador2 = self.resolverExpresion(root.getHijo(2))
            self.code += '\tif (T' + str(operador2) + ' == 0) {goto L' + str(self.maxTag) + '} //Error division by 0' + self.newLine
            self.code += '\tT' + str(self.actualTemp) + ' = T' + str(operador1) + ' + ' + 'T' + str(operador2) + ';' + self.newLine
            self.code += '\tgoto L' + str((self.maxTag + 1)) + ';' + self.newLine
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.maxTag += 1
            self.code += '\t\tT' + str(self.actualTemp) + ' = 0 //Set return value to 0' + self.newLine
            self.code += '\t\tDivisionBy0() // Call error message' + self.newLine
            self.code += '\tL' + str(self.maxTag) + ':' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1) # Retorno el numero del temporal en el que se almaceno el resultado
        elif(root.nombre == 'ENTERO'):
            self.code += '\tT' + str(self.actualTemp) + ' = ' + str(root.valor) + '; //Value' + self.newLine
            self.actualTemp += 1
            return (self.actualTemp - 1)
    #def resolverExpresionStack(self, root):
        
    #def resolverExpresionHeap(self, root):
