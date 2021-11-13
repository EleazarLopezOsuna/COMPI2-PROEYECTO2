from .filaGDA import filaGDA
from .lineaCodigo import lineaCodigo
class GDA():

    def __init__(self):
        self.tabla = []
        self.operadores = ['==', '+', '-', '*', '/', '<', '>', '<=', '>=', '!=', '[]']
    
    def agregar(self, linea:lineaCodigo):
        tipo = 0
        if(linea.x != None):
            if(linea.z == None and linea.op == None):
                tipo = 3
            elif(linea.z == None):
                tipo = 2
            else:
                tipo = 1
            self.pasoUno(linea, tipo)
            resultadoPasoDos = self.pasoDos(linea, tipo)
            #self.pasoTres(linea, resultadoPasoDos)
        else:
            self.tabla.append(filaGDA(linea.linea, len(self.tabla) + 1, None, None, None, None, None))

    def pasoUno(self, linea:lineaCodigo, tipo):
        nodoY = self.nodo(linea.y)
        if nodoY == None:
            self.tabla.append(filaGDA(linea.linea, len(self.tabla) + 1, linea.y, [linea.y], None, None, None))
        if(tipo == 1):
            nodoZ = self.nodo(linea.z)
            if nodoZ == None:
                self.tabla.append(filaGDA(linea.linea, len(self.tabla) + 1, linea.z, [linea.z], None, None, None))

    def pasoDos(self, linea:lineaCodigo, tipo):
        if tipo == 1:
            nodoY = self.nodo(linea.y)
            nodoZ = self.nodo(linea.z)
            nodoOp = self.nodoOperador(linea.op, nodoY, nodoZ)
            if nodoOp == None:
                nuevaFila = filaGDA(linea.linea, len(self.tabla) + 1, linea.op, None, nodoY, nodoZ, None)
                self.tabla.append(nuevaFila)
                nodoOp = nuevaFila.id
            return nodoOp
        if tipo == 2:
            nodoY = self.nodo(linea.y)
            nodoOp = self.nodoOperador(linea.op, nodoY, None)
            print(linea.op)
            if nodoOp == None:
                nuevaFila = filaGDA(linea.linea, len(self.tabla) + 1, linea.op, None, nodoY, None, None)
                self.tabla.append(nuevaFila)
                nodoOp = nuevaFila.id
            return nodoOp
        if tipo == 3:
            nodoY = self.nodo(linea.y)
            return nodoY

    def pasoTres(self, linea:lineaCodigo, nodoPasoDos):
        nodoX = self.nodo(linea.x)
        item:filaGDA
        if nodoX != None:
            for item in self.tabla:
                if item.id == nodoX:
                    item.asociados.remove(linea.x)
                    if item.equivalente != None:
                        item.equivalente.remove(linea.x)
                        if len(item.equivalente) == 0:
                            item.equivalente = None
                    if len(item.asociados) == 0:
                        item.asociados = None
            self.actualizarHijo(nodoX, nodoPasoDos)
        item:filaGDA
        for item in self.tabla:
            if item.id == nodoPasoDos:
                if item.asociados == None:
                    item.asociados = []
                item.asociados.append(linea.x)
                if(not str(linea.x).startswith('L')):
                    if item.equivalente == None:
                        item.equivalente = []
                    item.equivalente.append(linea.x)
            
    def actualizarHijo(self, nodoX, nodoPasoDos):
        item:filaGDA
        for item in self.tabla:
            if item.HI == nodoX:
                item.HI = nodoPasoDos
            if item.HD == nodoX:
                item.HD == nodoPasoDos

    def nodoOperador(self, etiqueta, HI, HD):
        item:filaGDA
        for item in self.tabla:
            if item.etiqueta == etiqueta:
                if item.HI == HI and item.HD == HD:
                    return item.id
        return None

    def nodo(self, etiqueta):
        item:filaGDA
        for item in self.tabla:
            if item.asociados != None:
                if etiqueta in item.asociados:
                    return item.id
            if item.equivalente != None:
                if etiqueta in item.equivalente:
                    return item.id
        return None

    def imprimir(self):
        item:filaGDA
        for item in self.tabla:
            #print(item.antigua, '     ',item.id, '     ', item.etiqueta, '     ', item.asociados, '     ', item.HI, '     ', item.HD, '     ', item.equivalente)
            print(item.id, '     ', item.etiqueta, '     ', item.asociados, '     ', item.HI, '     ', item.HD, '     ', item.equivalente)

    def obtenerIdentificadorFinal(self):
        item:filaGDA
        for item in self.tabla:
            if item.asociados != None:
                if len(item.asociados) > 1:
                    oficial = item.asociados[0]
                    for asociado in item.asociados:
                        if not str(asociado).lower().startswith('t'):
                            oficial = asociado
                    item.asociados = oficial
                    #item.equivalente = oficial
                elif len(item.asociados) == 1:
                    item.asociados = item.asociados[0]

    def optimizar(self):
        resultado = ''
        self.obtenerIdentificadorFinal()
        item:filaGDA
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

    def obtenerEtiqueta(self, hijo):
        item:filaGDA
        for item in self.tabla:
            if item.id == hijo:
                if item.etiqueta in self.operadores:
                    return item.asociados
                return item.etiqueta
