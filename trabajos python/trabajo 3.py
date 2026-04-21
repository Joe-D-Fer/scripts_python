while True:
    print("\n--- CONVERSOR DE TEMPERATURA ---")
    print("1. Celsius a Fahrenheit")
    print("2. Fahrenheit a Celsius")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        celsius = float(input("Ingrese la temperatura en Celsius: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"Resultado: {fahrenheit:.2f} °F")

    elif opcion == "2":
        fahrenheit = float(input("Ingrese la temperatura en Fahrenheit: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"Resultado: {celsius:.2f} °C")

    elif opcion == "3":
        print("Programa finalizado")
        break

    else:
        print("Opción inválida, intente nuevamente")