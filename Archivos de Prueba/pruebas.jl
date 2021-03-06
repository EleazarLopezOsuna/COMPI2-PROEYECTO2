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

        cadena1 = "Hola " :: String;
        cadena2 = "esta es una prueba" :: String;
        println(cadena1 * cadena2);

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

        for i in 1:10
            println(i);
        end;

        output = "" :: String;
        for i in 0:9

            output = "";
            for j in 0:(10 - i)
                output = output * " ";
            end;
        
            for k in 0:i 
                output = output * "* ";
            end;
            println(output);
        
        end;

        for l in "Cama"
            println(l);
        end;

        variable1 = "Prueba for con string" :: String;
        for m in variable1
            println(m);
        end;

        a = -1 :: Int64;
        while (a < 5)
            a = a + 1;
            if a == 3
                print("a");
                continue;
            elseif a == 4
                println("b");
                break;
            end;
            print("El valor de a es: ", a, ", ");
        end;


        index = -2 :: Int64;
        index = index + 1;

        while (index != 12)
            global index = index + 1;
            if (index == 0 || index == 1 || index == 11 || index == 12) 
                println("*********************************************************************************************************");
            elseif (index == 2) 
                println("**********  ***************  ******                 ******                 ******              **********");
            elseif (index >= 3 && index <= 5) 
                println("**********  ***************  ******  *********************  *************  ******  **********************");
            elseif (index == 6) 
                println("**********  ***************  ******                 ******                 ******  **********************");
            elseif (index >= 7 && index <= 9) 
                println("**********  ***************  ********************   ******  *************  ******  **********************");
            elseif (index == 10) 
                println("**********                   ******                 ******  *************  ******              **********");
            end;
        end;

        # Funciones sin parametros
            # Sin retorno
            function holaMundo()
                println("Hola mundo desde una funcion sin parametros");
            end;
            
            # Con retorno
            function pruebaRetorno()::String
                cadena = "Este es un retorno"::String;
                return cadena;
            end;
        
        # Funciones con parametros
            # Sin retorno
            function holaMundo(uno::String, dos::String, tres::String)
                println("Hola mundo desde una funcion sin parametros");
            end;
            
            # Con retorno
            function holaMundo(uno::String, dos::String, tres::String)::String
                cadena = "Este es un retorno"::String;
                return cadena;
            end;

        # Llamada a funciones sin recursividad
            # Sin retorno
                # Sin parametros
                function sinParametros()
                    cadena1 = "Hola mundo desde una funcion sin parametros" ::String;
                    cadena2 = "Cadena2" ::String;
                    println(cadena2);
                end;
                sinParametros();

                # Con parametro
                function conParametros(uno::String, dos::String, tres::String)
                    println(string(uno) * " mundo desde una " * dos * " con " * tres);
                end;
                conParametros("Hola", "funcion", "parametros");
            
            # Con retorno
                # Sin parametros
                function sinParametrosRetorno()::String
                    cadena = "Hola mundo desde una funcion sin parametros pero con retorno" ::String;
                    return cadena;
                end;
                variable1 = sinParametrosRetorno()::String;
                variable2 = "Prueba"::String;
                println(variable2);

                # Con parametro
                function conParametrosRetorno(uno::String, dos::String, tres::String)::String
                    cadena = "Este es un retorno " * uno * dos * tres * " de una funcion con parametros"::String;
                    return cadena;
                end;
                conParametrosRetorno();



# Comprobar si un numero es par o impar
function verificarNumero(numero::Int64)::String
    if (numero%2 == 0)
        return "El numero: " * numero * " es par";
    else
        return "El numero: " * numero * " es impar";
    end;
end;
print(verificarNumero(23));



function verificarNumero()::String
    numero = 23::Int64;
  if (numero == 0)
      return "El numero: " * string(numero) * " es par";
  else
      return "El numero: " * string(numero) * " es impar";
  end;
end;
print(verificarNumero());








function conParametros(uno::Int64, dos::Int64, tres::Int64)
    println(string(uno) * " mundo desde una " * string(dos) * " con " * string(tres));
end;
conParametros(1, 2, 3);


function conParametros(uno::Int64, dos::Int64, tres::Int64)::Int64
    println(string(uno) * " mundo desde una " * string(dos) * " con " * string(tres));
  	return uno * dos + tres;
end;
println(string(conParametros(1, 2, 3)));

function conParametros(uno::Int64, dos::Int64, tres::Int64)::Int64
    println(string(uno) * " mundo desde una " * string(dos) * " con " * string(tres));
  	variable = uno * dos + tres ::Int64;
  	return variable;
end;
println(conParametros(1, 2, 3));

function conParametros(uno::String, dos::String, tres::String)
    println(uno * " mundo desde una " * dos * " con " * tres);
end;
conParametros("Hola", "funcion", "parametros");



function fibonacci(numero::Int64)::Int64
    if (numero > 1)
        return fibonacci(numero - 1) + fibonacci(numero - 2);
    elseif (numero == 1)
        return 1;
    elseif (numero == 0)
        return 0;
    end;
end;
function verFibonacci(numero::Int64)
    for i in 0:(numero - 1)
        print(fibonacci(i), " ");
    end;
end;
# Deberia de imprimir: 0 1 1 2 3 5 8 13 21 34        
verFibonacci(10);