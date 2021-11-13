from Models.lineaCodigo import lineaCodigo
class optimizacionSimple():

    def __init__(self):
        self.tabla = []
        self.optimizado = []

    def agregar(self, linea:lineaCodigo):
        self.tabla.append(linea)

    def optimizar(self):
        item:lineaCodigo
        for item in self.tabla:
            if item.y != None and item.z != None:
                if item.op in ('+', '-'):
                    if str(item.z) == '0':
                        if str(item.y) == str(item.x):
                            self.tabla.remove(item)
                        else:
                            item.op = None
                            item.z = None
                if item.op in ('/', '*'):
                    if str(item.z) == '1':
                        if str(item.y) == str(item.x):
                            self.tabla.remove(item)
                        else:
                            item.op = None
                            item.z = None
                    elif str(item.z) == '2' and str(item.op) == '*':
                        item.z = item.y
                    elif str(item.z) == '0' and str(item.op) == '/':
                        item.z = None
                        item.op = None
                        item.y = '0'
                    elif str(item.y) == '0' and str(item.op) == '/':
                        item.z = None
                        item.op = None
                        item.y = '0'
    
    def imprimirOptimizado(self):
        resultado = ''
        self.obtenerIdentificadorFinal()
        for item in self.tabla:
            if item.id == None:
                resultado += item.antigua + '\n'
            else:
                if item.equivalente != None:
                    izquierdo = self.obtenerEtiqueta(item.HI)
                    derecho = self.obtenerEtiqueta(item.HD)
                    if str(item.etiqueta) == '[]':
                        resultado += str(item.asociados) + ' = ' + str(izquierdo) + '[int(' + str(derecho) + ')];\n'
                    else:
                        resultado += str(item.asociados) + ' = ' + str(izquierdo) + ' ' + str(item.etiqueta) + ' ' + str(derecho) + ';\n'
                elif str(item.asociados).startswith('L'):
                    izquierdo = self.obtenerEtiqueta(item.HI)
                    derecho = self.obtenerEtiqueta(item.HD)
                    resultado += 'if (' + str(izquierdo) + ' ' + str(item.etiqueta) + ' ' + str(derecho) + ') {goto ' + str(item.asociados) + ';}\n'
        return resultado

                    