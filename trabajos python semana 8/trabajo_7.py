def calcular_imc(altura, peso):
    return (peso/(altura * altura))

def main():
    altura=float(input("ingrese su altura en metros:"))
    peso=float(input("ingrese su peso en kilos:"))
    print(f"su indice de IMC es: {calcular_imc(altura, peso):.2f}")

if __name__ == "__main__":
    main()