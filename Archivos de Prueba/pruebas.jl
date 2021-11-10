# Declaracion de variables
# Normales
    # asignacion : IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo (6)
        variable1 = 2 ^ 6 :: Int64;
        variable1 = 24 :: Int64;
        variable2 = variable1 :: Int64;
        varriable3 = 23.34 :: Float64;
        variable4 = false || true :: Bool;
        variable5 = lowercase("HHOLA") :: String;
        variable6 = uppercase(variable5) :: String;

    # asignacion : IDENTIFICADOR accesoFS IGUAL expresion (5)

    # asignacion : IDENTIFICADOR dimension IGUAL expresion (5)

    # asignacion : IDENTIFICADOR DOBLEPUNTOS tipo (4)

    # asignacion : IDENTIFICADOR (2)

    # asignacion : IDENTIFICADOR IGUAL expresion (4)
        variable1 = 2 ^ 6 :: Int64;
        variable2 = 2 :: Int64;
        variable2 = variable1;

    # Print y Println
        val1 = 1::Int64;
        val2 = 10::Int64;
        println("Probando declaracion de variables");
        println(val1, " ", val2);
        println("---------------------------------");
        val1 = val1 + 41 + 82 - 10 + 0 * 2 ^ 2;
        val2 = 11 * 1 - 33;
        println("Probando asignación de variables y aritmeticas");
        println(val1, " ", val2);
        println("---------------------------------");

    # If
        variable1 = 2 ::Int64;
        variable2 = 3 ::Int64;
        if (variable1 > variable2) 
            println("IF CORRECTO");
        end;

        variable1 = 2 ::Int64;
        variable2 = 3 ::Int64;
        if (variable1 > variable2) 
            println("variable1 es mayor a variable2");
        else
            println("variable1 es menor a variable2");
        end;

        variable1 = 4 ::Int64;
        if (variable1 == 1) 
            println("variable1 es 1");
        elseif (variable1 == 2)
            println("variable1 es 2");
        elseif (variable1 == 3)
            println("variable1 es 3");
        elseif (variable1 == 4)
            println("variable1 es 4");
        else
            println("variable1 es otro");
        end;