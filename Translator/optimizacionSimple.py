from Models.lineaCodigo import lineaCodigo
class optimizacionSimple():

    def __init__(self):
        self.tabla = []
        self.optimizado = []

    def agregar(self, linea:lineaCodigo):
        self.tabla.append(linea)

    def optimizar(self):
        contador = 1
        item:lineaCodigo
        for item in self.tabla:
            contador += 1
            if item.y != None and item.z != None:
                if item.op in ('+', '-'):
                    if str(item.z) == '0':
                        if str(item.y) == str(item.x):
                            print('Optimizacion por mirilla - Regla 6. Se elimino la linea ' + item.linea, ' en fila ', contador)
                            self.tabla.remove(item)
                        else:
                            print('Optimizacion por mirilla - Regla 7 en fila ', contador)
                            item.modificada = 1
                            item.op = None
                            item.z = None
                elif item.op in ('/', '*'):
                    if str(item.z) == '1':
                        if str(item.y) == str(item.x):
                            print('Optimizacion por mirilla - Regla 6. Se elimino la linea ' + item.linea, ' en fila ', contador)
                            self.tabla.remove(item)
                        else:
                            print('Optimizacion por mirilla - Regla 7 en fila ', contador)
                            item.modificada = 1
                            item.op = None
                            item.z = None
                    elif str(item.z) == '2' and str(item.op) == '*':
                        item.z = item.y
                        print('Optimizacion por mirilla - Regla 8 en fila ', contador)
                        item.modificada = 1
                    elif str(item.z) == '0' and str(item.op) == '/':
                        item.z = None
                        item.op = None
                        item.y = '0'
                        print('Optimizacion por mirilla - Regla 8 en fila ', contador)
                        item.modificada = 1
                    elif str(item.y) == '0' and str(item.op) == '/':
                        item.z = None
                        item.op = None
                        item.y = '0'
                        print('Optimizacion por mirilla - Regla 6 en fila ', contador)
                        item.modificada = 1
    
    def imprimirOptimizado(self):
        resultado = ''
        item:lineaCodigo
        for item in self.tabla:
            if item.modificada == 0:
                resultado += item.linea + '\n'
        return resultado

                    