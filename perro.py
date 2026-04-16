class Perro:

    def __init__(self, nombre):
        self.nombre = nombre
        self.trucos = []    # crea una nueva lista vacía para cada perro

    def agregar_truco(self, truco):
        self.trucos.append(truco)

def main():
    firulais = Perro('Firulais')
    cholito = Perro('Cholito')
    
    firulais.agregar_truco('rodar')
    cholito.agregar_truco('dar la pata')
    print('trucos de firulais: ', firulais.trucos)
    print('trucos de cholito: ', cholito.trucos)
    
while True:
    main()
    if input("otra vez? s/n").lower()=="n":break