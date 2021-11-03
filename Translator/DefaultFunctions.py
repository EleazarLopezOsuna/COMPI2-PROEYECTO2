class DefaultFunctions():
    
    def __init__(self):
        self.OutOfBounds = ''
        self.DivisionBy0 = ''
        self.stringConcat = ''
        self.stringPrint = ''
        self.stringLowerCase = ''
        self.stringUpperCase = ''
        self.stringTimes = ''
        self.numberPower = ''
        self.operateSum = ''
        self.operateDif = ''
        self.operateMul = ''
        self.operateDiv = ''
        self.intToString = ''
        self.nuevaLinea = '\n'
        self.GenerateStringConcat()
        self.GenerateDivisionBy0()
        self.GenerateOutOfBounds()
        self.GenerateStringPrint()
        self.GenerateLowerCase()
        self.GenerateUpperCase()
        self.GenerateStringTimes()
        self.GenerateNumberPower()
        self.GenerateIntToString()

    def GenerateStringConcat(self):
        self.stringConcat = 'func stringConcat(){' + self.nuevaLinea
        self.stringConcat += '\tT0 = SP + 1; //Get the position of fist string in stack' + self.nuevaLinea
        self.stringConcat += '\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringConcat += '\tT1 = HP; //Save first position of new string' + self.nuevaLinea
        self.stringConcat += '\tL0: //First loop tag' + self.nuevaLinea
        self.stringConcat += '\t\tT2 = HEAP[int(T0)]; //Get character in heap' + self.nuevaLinea
        self.stringConcat += '\t\tif(T2 == 36) {goto L1;} //Heap character is $' + self.nuevaLinea
        self.stringConcat += '\t\tHEAP[int(HP)] = T2; //Save character into heap' + self.nuevaLinea
        self.stringConcat += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringConcat += '\t\tgoto L0; //Go back to first loop' + self.nuevaLinea
        self.stringConcat += '\tL1:' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = SP + 2; //Get the position of second string in stack' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringConcat += '\t\tL2: //Second loop tag' + self.nuevaLinea
        self.stringConcat += '\t\t\tT2 = HEAP[int(T0)]; //Get character in heap' + self.nuevaLinea
        self.stringConcat += '\t\t\tif(T2 == 36) {goto L3;} //Heap character is $' + self.nuevaLinea
        self.stringConcat += '\t\t\tHEAP[int(HP)] = T2; //Save character into heap' + self.nuevaLinea
        self.stringConcat += '\t\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringConcat += '\t\t\tgoto L2; //Go back to second loop' + self.nuevaLinea
        self.stringConcat += '\tL3: //Exit tag' + self.nuevaLinea
        self.stringConcat += '\t\tHEAP[int(HP)] = 36; //Add end of string to heap' + self.nuevaLinea
        self.stringConcat += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringConcat += '\t\tT0 = SP + 0; //Get return position' + self.nuevaLinea
        self.stringConcat += '\t\tSTACK[int(T0)] = T1; //Save heap position of the new string into stack' + self.nuevaLinea
        self.stringConcat += '\t\treturn; //Go back' + self.nuevaLinea
        self.stringConcat += '}' + self.nuevaLinea

    def GenerateStringPrint(self):
        self.stringPrint = 'func stringPrint(){' + self.nuevaLinea
        self.stringPrint += '\tT0 = SP + 0; //Get initial position of the string' + self.nuevaLinea
        self.stringPrint += '\tT0 = STACK[int(T0)]; //Obtenemos el primer caracter de la cadena' + self.nuevaLinea
        self.stringPrint += '\tL0: //Loop tag' + self.nuevaLinea
        self.stringPrint += '\t\tT1 = HEAP[int(T0)]; //Get heap character' + self.nuevaLinea
        self.stringPrint += '\t\tif(T1 == 36) {goto L1;} //Heap character is $' + self.nuevaLinea
        self.stringPrint += '\t\tfmt.Printf("%' + 'c", int(T1)); //Character print' + self.nuevaLinea
        self.stringPrint += '\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringPrint += '\t\tgoto L0; //Go back to loop' + self.nuevaLinea
        self.stringPrint += '\tL1: //Exit tag' + self.nuevaLinea
        self.stringPrint += '\t\treturn; //Go back' + self.nuevaLinea
        self.stringPrint += '}' + self.nuevaLinea

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
        self.DivisionBy0 = 'func DivisionBy0(){' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 68); //D' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 118); //v' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 115); //s' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 105); //i' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 111); //o' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 110); //n' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 98); //b' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 121); //y' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 32); // ' + self.nuevaLinea
        self.DivisionBy0 += '\tfmt.Printf("%' + 'c", 48); //0' + self.nuevaLinea
        self.DivisionBy0 += '\treturn;' + self.nuevaLinea
        self.DivisionBy0 += '}' + self.nuevaLinea

    def GenerateLowerCase(self):
        self.stringLowerCase = 'func stringLowerCase(){' + self.nuevaLinea
        self.stringLowerCase += '\tT0 = SP + 1; //Get the position of fist string in stack' + self.nuevaLinea
        self.stringLowerCase += '\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringLowerCase += '\tT1 = HP; //Save first position of new string' + self.nuevaLinea
        self.stringLowerCase += '\tL0: //Loop tag' + self.nuevaLinea
        self.stringLowerCase += '\t\tT2 = HEAP[int(T0)]; //Get character in heap' + self.nuevaLinea
        self.stringLowerCase += '\t\tif(T2 == 36) {goto L2;} //Heap character is $' + self.nuevaLinea
        self.stringLowerCase += '\t\tif(T2 < 65) {goto L1;} //Character < A' + self.nuevaLinea
        self.stringLowerCase += '\t\tif(T2 > 90) {goto L1;} //Character > Z' + self.nuevaLinea
        self.stringLowerCase += '\t\tT2 = T2 + 32; //Lower case' + self.nuevaLinea
        self.stringLowerCase += '\tL1: //No need to lower case tag' + self.nuevaLinea
        self.stringLowerCase += '\t\tHEAP[int(HP)] = T2; //Save character into heap' + self.nuevaLinea
        self.stringLowerCase += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringLowerCase += '\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringLowerCase += '\t\tgoto L0; //Go back to first loop' + self.nuevaLinea
        self.stringLowerCase += '\tL2:' + self.nuevaLinea
        self.stringLowerCase += '\t\tHEAP[int(HP)] = 36; //Add end of string to heap' + self.nuevaLinea
        self.stringLowerCase += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringLowerCase += '\t\tT0 = SP + 0; //Get return position' + self.nuevaLinea
        self.stringLowerCase += '\t\tSTACK[int(T0)] = T1; //Save heap position of the new string into stack' + self.nuevaLinea
        self.stringLowerCase += '\t\treturn; //Go back' + self.nuevaLinea
        self.stringLowerCase += '}' + self.nuevaLinea

    def GenerateUpperCase(self):
        self.stringUpperCase = 'func stringUpperCase(){' + self.nuevaLinea
        self.stringUpperCase += '\tT0 = SP + 1; //Get the position of fist string in stack' + self.nuevaLinea
        self.stringUpperCase += '\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringUpperCase += '\tT1 = HP; //Save first position of new string' + self.nuevaLinea
        self.stringUpperCase += '\tL0: //Loop tag' + self.nuevaLinea
        self.stringUpperCase += '\t\tT2 = HEAP[int(T0)]; //Get character in heap' + self.nuevaLinea
        self.stringUpperCase += '\t\tif(T2 == 36) {goto L2;} //Heap character is $' + self.nuevaLinea
        self.stringUpperCase += '\t\tif(T2 < 97) {goto L1;} //Character < A' + self.nuevaLinea
        self.stringUpperCase += '\t\tif(T2 > 122) {goto L1;} //Character > Z' + self.nuevaLinea
        self.stringUpperCase += '\t\tT2 = T2 - 32; //Lower case' + self.nuevaLinea
        self.stringUpperCase += '\tL1: //No need to lower case tag' + self.nuevaLinea
        self.stringUpperCase += '\t\tHEAP[int(HP)] = T2; //Save character into heap' + self.nuevaLinea
        self.stringUpperCase += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringUpperCase += '\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringUpperCase += '\t\tgoto L0; //Go back to first loop' + self.nuevaLinea
        self.stringUpperCase += '\tL2:' + self.nuevaLinea
        self.stringUpperCase += '\t\tHEAP[int(HP)] = 36; //Add end of string to heap' + self.nuevaLinea
        self.stringUpperCase += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringUpperCase += '\t\tT0 = SP + 0; //Get return position' + self.nuevaLinea
        self.stringUpperCase += '\t\tSTACK[int(T0)] = T1; //Save heap position of the new string into stack' + self.nuevaLinea
        self.stringUpperCase += '\t\treturn; //Go back' + self.nuevaLinea
        self.stringUpperCase += '}' + self.nuevaLinea

    def GenerateStringTimes(self):
        self.stringTimes = 'func stringTimes(){' + self.nuevaLinea
        self.stringTimes += '\tT0 = SP + 1; //Get the position of fist string in stack' + self.nuevaLinea
        self.stringTimes += '\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringTimes += '\tT1 = SP + 2; //Get the number position' + self.nuevaLinea
        self.stringTimes += '\tT1 = STACK[int(T1)]; //Get the number of times the string will repeat' + self.nuevaLinea
        self.stringTimes += '\tT2 = HP; //Save first position of new string' + self.nuevaLinea
        self.stringTimes += '\tL0: //First loop tag' + self.nuevaLinea
        self.stringTimes += '\t\tif (T1 < 1) {goto L3;} //Exits the loop' + self.nuevaLinea
        self.stringTimes += '\t\tL1: //First loop tag' + self.nuevaLinea
        self.stringTimes += '\t\t\tT3 = HEAP[int(T0)]; //Get character in heap' + self.nuevaLinea
        self.stringTimes += '\t\t\tif(T3 == 36) {goto L2;} //Heap character is $, leaves loop' + self.nuevaLinea
        self.stringTimes += '\t\t\tHEAP[int(HP)] = T3; //Save character into heap' + self.nuevaLinea
        self.stringTimes += '\t\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringTimes += '\t\t\tT0 = T0 + 1; //T0 increses' + self.nuevaLinea
        self.stringTimes += '\t\t\tgoto L1; //Go back to string loop' + self.nuevaLinea
        self.stringTimes += '\t\tL2:' + self.nuevaLinea
        self.stringTimes += '\t\t\tT1 = T1 - 1' + self.nuevaLinea
        self.stringTimes += '\t\t\tT0 = SP + 1; //Get the position of fist string in stack' + self.nuevaLinea
        self.stringTimes += '\t\t\tT0 = STACK[int(T0)]; //Get the heap position of first string' + self.nuevaLinea
        self.stringTimes += '\t\t\tgoto L0' + self.nuevaLinea
        self.stringTimes += '\tL3: //Exit tag' + self.nuevaLinea
        self.stringTimes += '\t\tHEAP[int(HP)] = 36; //Add end of string to heap' + self.nuevaLinea
        self.stringTimes += '\t\tHP = HP + 1; //Heap increses' + self.nuevaLinea
        self.stringTimes += '\t\tT0 = SP + 0; //Get return position' + self.nuevaLinea
        self.stringTimes += '\t\tSTACK[int(T0)] = T2; //Save heap position of the new string into stack' + self.nuevaLinea
        self.stringTimes += '\t\treturn; //Go back' + self.nuevaLinea
        self.stringTimes += '}' + self.nuevaLinea

    def GenerateNumberPower(self):
        self.stringTimes = 'func numberPower(){' + self.nuevaLinea
        self.stringTimes += '\tT0 = SP + 1; //Get base index' + self.nuevaLinea
        self.stringTimes += '\tT0 = STACK[int(T0)]; //Get base value' + self.nuevaLinea
        self.stringTimes += '\tT1 = SP + 2; //Get exponent index' + self.nuevaLinea
        self.stringTimes += '\tT1 = STACK[int(T1)]; //Get exponent value' + self.nuevaLinea
        self.stringTimes += '\tT2 = 1; //Set initial value' + self.nuevaLinea
        self.stringTimes += '\tL0: //Loop tag' + self.nuevaLinea
        self.stringTimes += '\t\tif(T1 < 1) {goto L1;} //Completed' + self.nuevaLinea
        self.stringTimes += '\t\tT2 = T2 * T0; //Previous value * Base' + self.nuevaLinea
        self.stringTimes += '\t\tT1 = T1 - 1; //Base - 1' + self.nuevaLinea
        self.stringTimes += '\t\tgoto L0; //Go back to loop' + self.nuevaLinea
        self.stringTimes += '\tL1: //Exit tag' + self.nuevaLinea
        self.stringTimes += '\t\tT0 = SP + 0; //Set return index' + self.nuevaLinea
        self.stringTimes += '\t\tSTACK[int(T0)] = T2; //Set return value' + self.nuevaLinea
        self.stringTimes += '\t\treturn; //Exit function' + self.nuevaLinea
        self.stringTimes += '}' + self.nuevaLinea

    def GenerateIntToString(self):
        self.intToString = 'func intToString(){' + self.nuevaLinea
        self.intToString += '\tT0 = SP + 1; //Get number position' + self.nuevaLinea
        self.intToString += '\tT0 = STACK[int(T0)]; //Get number' + self.nuevaLinea
        self.intToString += '\tT1 = T0; //Make a copy' + self.nuevaLinea
        self.intToString += '\tT2 = 1; //counter' + self.nuevaLinea
        self.intToString += '\tL0:' + self.nuevaLinea
        self.intToString += '\t\tif(T1 < 10) {goto L1;}' + self.nuevaLinea
        self.intToString += '\t\tT3 = float64(int64(T1) % 10); //temp%10' + self.nuevaLinea
        self.intToString += '\t\tT1 = T1 - T3; //temp -= temp%10' + self.nuevaLinea
        self.intToString += '\t\tT1 = T1 / 10; //temp /= 10' + self.nuevaLinea
        self.intToString += '\t\tT2 = T2 * 10; //contador *= 10' + self.nuevaLinea
        self.intToString += '\t\tgoto L0;' + self.nuevaLinea
        self.intToString += '\tL1:' + self.nuevaLinea
        self.intToString += '\t\tT3 = T1 + 48; //Get ascii for number' + self.nuevaLinea
        self.intToString += '\t\tHEAP[int(HP)] = T3' + self.nuevaLinea
        self.intToString += '\t\tHP = HP + 1' + self.nuevaLinea
        self.intToString += '\t\tif(T0 > 9) {goto L2;}' + self.nuevaLinea
        self.intToString += '\t\tgoto L3;' + self.nuevaLinea
        self.intToString += '\tL2:' + self.nuevaLinea
        self.intToString += '\t\tT1 = float64(int64(T0) % int64(T2)); //num %= contador' + self.nuevaLinea
        self.intToString += '\t\tT0 = SP + 1; //Get number position' + self.nuevaLinea
        self.intToString += '\t\tSTACK[int(T0)] = T1;' + self.nuevaLinea
        self.intToString += '\t\tintToString();' + self.nuevaLinea
        self.intToString += '\tL3:' + self.nuevaLinea
        self.intToString += '\t\treturn;' + self.nuevaLinea
        self.intToString += '}' + self.nuevaLinea
