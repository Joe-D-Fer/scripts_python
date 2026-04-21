nombre = input("Escriba nombre del alumno o 'salir' para terminar: ")

while nombre.lower() != "salir":
    
    print("*********Bienvenido***********")
    print (nombre)

    # NOTA 1
    while True:
        nota_1 = float(input("Ingrese nota 1: "))
        if 1 <= nota_1 <= 7:
            break
        else:
            print("Error: la nota debe estar entre 1 y 7")

    # NOTA 2
    while True:
        nota_2 = float(input("Ingrese nota 2: "))
        if 1 <= nota_2 <= 7:
            break
        else:
            print("Error: la nota debe estar entre 1 y 7")

    # NOTA 3
    while True:
        nota_3 = float(input("Ingrese nota 3: "))
        if 1 <= nota_3 <= 7:
            break
        else:
            print("Error: la nota debe estar entre 1 y 7")

    # NOTA 4
    while True:
        nota_4 = float(input("Ingrese nota 4: "))
        if 1 <= nota_4 <= 7:
            break
        else:
            print("Error: la nota debe estar entre 1 y 7")

    # NOTA 5
    while True:
        nota_5 = float(input("Ingrese nota 5: "))
        if 1 <= nota_5 <= 7:
            break
        else:
            print("Error: la nota debe estar entre 1 y 7")

    promedio = (nota_1 + nota_2 + nota_3 + nota_4 + nota_5) / 5

    print(f"El promedio de {nombre} es {promedio:.2f}")
    print("*********RESULTADO***********")

    if promedio >= 4:
        print("Felicidades, Usted ha aprobado, salga a celebrar ")
    else:
        print("Usted ha reprobado, salga a ahogar las penas")

    print("\n")

    # volver a pedir nombre al final del ciclo
    nombre = input("Escriba nombre del alumno (o 'salir' para terminar): ")

print("Programa terminado")