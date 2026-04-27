# Sistema de gestión de notas

estudiantes = []
notas = []
print("********** bienvenido al sistema de gestión de notas **********\n")
while True:
    nombre = input("Ingrese el nombre del estudiante (o 'salir' para terminar): ")
    
    if nombre.lower() == "salir":
        break

    try:
        nota = float(input("Ingrese la nota (1.0 a 7.0): "))
        
        if nota < 1.0 or nota > 7.0:
            print("⚠️ La nota debe estar entre 1.0 y 7.0\n")
            continue

        estudiantes.append(nombre)
        notas.append(nota)

    except ValueError:
        print("⚠️ Debe ingresar un número válido\n")

# Verificar que haya datos
if len(notas) == 0:
    print("No se ingresaron datos.")
else:
    # Nota más alta y más baja
    max_nota = max(notas)
    min_nota = min(notas)

    indice_max = notas.index(max_nota)
    indice_min = notas.index(min_nota)

    # Promedio
    promedio = sum(notas) / len(notas)

    # Aprobados y reprobados
    aprobados = 0
    reprobados = 0

    for n in notas:
        if n >= 4.0:
            aprobados += 1
        else:
            reprobados += 1

    # Resultados
    print("\n--- RESULTADOS ---")
    print(f"Estudiante con nota más alta: {estudiantes[indice_max]} ({max_nota})")
    print(f"Estudiante con nota más baja: {estudiantes[indice_min]} ({min_nota})")
    print(f"Promedio general del curso: {promedio:.2f}")
    print(f"Aprobados: {aprobados}")
    print(f"Reprobados: {reprobados}")