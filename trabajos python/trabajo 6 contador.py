contador = 0
numero = 1  # valor inicial distinto de 0 para entrar al while

while numero != 0:
    numero = int(input("Ingrese un número entero (0 para salir): "))

    if numero != 0:
        contador += 1

        # Par o impar
        if numero % 2 == 0:
            print("El número es PAR")
        else:
            print("El número es IMPAR")

        # Positivo, negativo o cero
        if numero > 0:
            print("El número es POSITIVO")
        elif numero < 0:
            print("El número es NEGATIVO")

        print("----------------------")

print("Programa finalizado")
print("Cantidad de números evaluados:", contador)