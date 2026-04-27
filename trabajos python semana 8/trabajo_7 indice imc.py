
print(" ******** BIENVENIDO********")



def calcular_imc(altura, peso):
    return (peso/(altura * altura))

def main():
    altura=float(input("ingrese su altura en metros:"))
    peso=float(input("ingrese su peso en kilos:"))
    print(f"su indice de IMC es: {calcular_imc(altura, peso):.2f}")

    resultado = calcular_imc(altura, peso)

    if resultado <= 18.5:
        print ("esta bajo peso")
    elif resultado <= 24.9:
        print ("Peso normal")
    elif resultado <= 29.9:
        print ("sobre peso")
    else:
        print ("obesidad")
if __name__ == "__main__":
    salir= False
    while not salir:
        main()
        if input("continuar (s/n):")=="n": salir=True




