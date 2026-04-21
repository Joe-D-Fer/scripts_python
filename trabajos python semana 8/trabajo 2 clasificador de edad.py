while True:
    print(" ******** BIENVENIDO********")
    entrada = input("Ingrese su edad o escriba 'salir' para terminar: ")

    if entrada.lower() == "salir":
        print("Programa terminado.")
        break

    try:
        edad = int(entrada)

        if edad < 0:
            print("Error: la edad debe ser un número positivo.")
        else:
            # Clasificación
            if edad <= 12:
                print("Categoría: Niño")
            elif edad <= 17:
                print("Categoría: Adolescente")
            elif edad <= 59:
                print("Categoría: Adulto")
            else:
                print("Categoría: Adulto mayor")

    except ValueError:
        print("Error: debe ingresar un número válido o 'salir'.")
      