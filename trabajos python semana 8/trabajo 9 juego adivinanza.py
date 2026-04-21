import random

jugar = "si"

while jugar.lower() == "si":
    numero_secreto = random.randint(1, 100)
    intentos = 0
    max_intentos = 7
    adivinado = False

    print("\n--- JUEGO DE ADIVINANZA ---")
    print("Adivina el número entre 1 y 100")
    print("Tienes", max_intentos, "intentos")

    while intentos < max_intentos and not adivinado:
        try:
            numero = int(input("Ingresa un número: "))
            intentos += 1

            if numero == numero_secreto:
                adivinado = True
            elif numero < numero_secreto:
                print("El número secreto es MAYOR")
            else:
                print("El número secreto es MENOR")

        except ValueError:
            print("Por favor ingresa un número válido")

    if adivinado:
        print("\n¡FELICIDADES! Adivinaste el número")
    else:
        print("\nPerdiste. El número era:", numero_secreto)

    print("Intentos usados:", intentos)

    jugar = input("\n¿Quieres jugar nuevamente? (si/no): ")

print("Gracias por jugar")