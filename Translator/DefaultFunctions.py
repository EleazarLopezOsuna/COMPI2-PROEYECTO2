class DefaultFunctions():
    
    def __init__(self):
        self.OutOfBounds = ''
        self.DivisionBy0 = ''
        self.stringConcat = ''
        self.stringPrint = ''
        self.nuevaLinea = '\n'
        self.GenerateStringConcat()
        self.GenerateDivisionBy0()
        self.GenerateOutOfBounds()
        self.GenerateStringPrint()

    def GenerateStringConcat(self):
        self.stringConcat = 'func stringConcat(){' + self.nuevaLinea
        self.stringConcat += '\tT0 = SP + 1 //Get the position of fist string in stack' + self.nuevaLinea
        self.stringConcat += '\tT0 = STACK[int(T0)] //Get the heap position of first string' + self.nuevaLinea
        self.stringConcat += '\tT1 = HP //Save first position of new string' + self.nuevaLinea
        self.stringConcat += '\tL0: //First loop tag' + self.nuevaLinea
        self.stringConcat += '\t\tT2 = HEAP[int(T0)] //Get character in heap' + self.nuevaLinea
        self.stringConcat += '\t\tif(T2 == 36) {goto L1} //Heap character is $' + self.nuevaLinea
        self.stringConcat += '\t\tHEAP[int(HP)] = T2 //Save character into heap' + self.nuevaLinea
        self.stringConcat += '\t\tHP = HP + 1 //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = T0 + 1 //T0 increses' + self.nuevaLinea
        self.stringConcat += '\t\tgoto L0 //Go back to first loop' + self.nuevaLinea
        self.stringConcat += '\tL1:' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = SP + 2 //Get the position of second string in stack' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = STACK[int(T0)] //Get the heap position of first string' + self.nuevaLinea
        self.stringConcat += '\t\tL2: //Second loop tag' + self.nuevaLinea
        self.stringConcat += '\t\t\tT2 = HEAP[int(T0)] //Get character in heap' + self.nuevaLinea
        self.stringConcat += '\t\t\tif(T2 == 36) {goto L3} //Heap character is $' + self.nuevaLinea
        self.stringConcat += '\t\t\tHEAP[int(HP)] = T2 //Save character into heap' + self.nuevaLinea
        self.stringConcat += '\t\t\tHP = HP + 1 //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\t\tT0 = T0 + 1 //T0 increses' + self.nuevaLinea
        self.stringConcat += '\t\t\tgoto L2 //Go back to second loop' + self.nuevaLinea
        self.stringConcat += '\tL3: //Exit tag' + self.nuevaLinea
        self.stringConcat += '\t\tHEAP[int(HP)] = 36 //Add end of string to heap' + self.nuevaLinea
        self.stringConcat += '\t\tHP = HP + 1 //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = SP + 0 //Get return position' + self.nuevaLinea
        self.stringConcat += '\t\tSTACK[int(T0)] = T1 //Save heap position of the new string into stack' + self.nuevaLinea
        self.stringConcat += '\t\treturn //Go back' + self.nuevaLinea
        self.stringConcat += '}' + self.nuevaLinea

    def GenerateStringPrint(self):
        self.stringConcat += 'func stringPrint(){' + self.nuevaLinea
        self.stringConcat += '\tT0 = SP + 0 //Get initial position of the string' + self.nuevaLinea
        self.stringConcat += '\tT0 = STACK[int(T0)] //Obtenemos el primer caracter de la cadena' + self.nuevaLinea
        self.stringConcat += '\tL0: //Loop tag' + self.nuevaLinea
        self.stringConcat += '\t\tT1 = HEAP[int(T0)] //Get heap character' + self.nuevaLinea
        self.stringConcat += '\t\tif(T1 == 36) {goto L1} //Heap character is $' + self.nuevaLinea
        self.stringConcat += '\t\tfmt.Printf("%' + 'c", int(T1)) //Character print' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = T0 + 1 //T0 increses' + self.nuevaLinea
        self.stringConcat += '\t\tgoto L0 //Go back to loop' + self.nuevaLinea
        self.stringConcat += '\tL1: //Exit tag' + self.nuevaLinea
        self.stringConcat += '\t\treturn //Go back' + self.nuevaLinea
        self.stringConcat += '}' + self.nuevaLinea

    def GenerateOutOfBounds(self):
        self.OutOfBounds = 'func OutOfBounds(){' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 79); //O' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 117); //u' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 116); //t' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 111); //o' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 102); //f' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 66); //B' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 111); //o' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 117); //u' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 110); //n' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 100); //d' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 115); //s' + self.nuevaLinea
        self.OutOfBounds += '\treturn;' + self.nuevaLinea
        self.OutOfBounds += '}' + self.nuevaLinea

    def GenerateDivisionBy0(self):
        self.OutOfBounds = 'func DivisionBy0(){' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 68); //D' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 118); //v' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 115); //s' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 111); //o' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 110); //n' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 98); //b' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 121); //y' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.OutOfBounds += '\tfmt.Printf("%' + 'c", 48); //0' + self.nuevaLinea
        self.OutOfBounds += '\treturn;' + self.nuevaLinea
        self.OutOfBounds += '}' + self.nuevaLinea