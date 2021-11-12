class OptimizationTable():
    
    def __init__(self):
        self.items = []

    def insertar(self, previous, new, line, time, rule):
        self.items.append([previous, new, line, time, rule])
