# ===== LIBROS =====
cod_libro = [1, 2, 3, 4]
titulo_libro = [
    "Cien años de soledad",
    "Don Quijote de la Mancha",
    "1984",
    "El Principito"
]
autor_libro = [
    "Gabriel García Márquez",
    "Miguel de Cervantes",
    "George Orwell",
    "Antoine de Saint-Exupéry"
]
fecha_publicacion = [1967, 1605, 1949, 1943]
stock_disponible = [3, 5, 2, 4]

# ===== USUARIOS =====
cod_usuario = [1, 2, 3]
nombre_usuario = [
    "Juan Pérez",
    "María González",
    "Carlos Soto"
]

# ===== PRESTAMOS =====
cod_prestamo = [1, 2]
prestamo_cod_usuario = [1, 2]
prestamo_cod_libro = [3, 1]
fecha_prestamo = [
    "2026-04-20",
    "2026-04-21"
]

# ===== FLAGS =====
exit_flag = False


# ===== UTIL =====
def generar_codigo(lista):
    return len(lista) + 1


def buscar_indice_libro_por_id(codigo):
    if codigo in cod_libro:
        return cod_libro.index(codigo)
    return -1


# ===== FUNCIONES =====
def agregar_libro():
    try:
        titulo = input("Ingrese título del libro: ")
        autor = input("Ingrese autor del libro: ")
        fecha = int(input("Ingrese el año de publicación: "))
        stock = int(input("Ingrese la cantidad disponible: "))

        codigo = generar_codigo(cod_libro)

        cod_libro.append(codigo)
        titulo_libro.append(titulo)
        autor_libro.append(autor)
        fecha_publicacion.append(fecha)
        stock_disponible.append(stock)

        print("Libro agregado correctamente")

    except ValueError:
        print("Error: datos inválidos")

def consultar_catalogo():
    if not cod_libro:
        print("No hay libros registrados")
        return

    for i in range(len(cod_libro)):
        print(f"[{cod_libro[i]}] {titulo_libro[i]} - {autor_libro[i]} "
              f"({fecha_publicacion[i]}) | Stock: {stock_disponible[i]}")


def buscar_libro():
    texto = input("Ingrese título o autor a buscar: ").lower()
    encontrado = False

    for i in range(len(cod_libro)):
        if texto in titulo_libro[i].lower() or texto in autor_libro[i].lower():
            print(f"[{cod_libro[i]}] {titulo_libro[i]} - {autor_libro[i]}")
            encontrado = True

    if not encontrado:
        print("No se encontraron resultados")


def prestar_libro():
    try:
        id_libro = int(input("Ingrese código del libro: "))
        indice = buscar_indice_libro_por_id(id_libro)

        if indice == -1:
            print("Libro no encontrado")
            return

        if stock_disponible[indice] <= 0:
            print("No hay stock disponible")
            return

        usuario = input("Ingrese nombre del usuario: ")
        fecha = input("Ingrese fecha de préstamo: ")

        # registrar usuario (simple)
        cod_u = generar_codigo(cod_usuario)
        cod_usuario.append(cod_u)
        nombre_usuario.append(usuario)

        # registrar préstamo
        cod_p = generar_codigo(cod_prestamo)
        cod_prestamo.append(cod_p)
        prestamo_cod_usuario.append(cod_u)
        prestamo_cod_libro.append(id_libro)
        fecha_prestamo.append(fecha)

        stock_disponible[indice] -= 1

        print("Préstamo realizado con éxito")

    except ValueError:
        print("Entrada inválida")


def devolver_libro():
    try:
        id_libro = int(input("Ingrese código del libro a devolver: "))

        for i in range(len(prestamo_cod_libro)):
            if prestamo_cod_libro[i] == id_libro:
                indice_libro = buscar_indice_libro_por_id(id_libro)

                stock_disponible[indice_libro] += 1

                # eliminar préstamo (IMPORTANTE: borrar en todas las listas)
                cod_prestamo.pop(i)
                prestamo_cod_usuario.pop(i)
                prestamo_cod_libro.pop(i)
                fecha_prestamo.pop(i)

                print("Libro devuelto correctamente")
                return

        print("No se encontró préstamo para ese libro")

    except ValueError:
        print("Entrada inválida")


def ver_prestamos():
    if not cod_prestamo:
        print("No hay préstamos registrados")
        return

    for i in range(len(cod_prestamo)):
        print(f"Préstamo {cod_prestamo[i]} | Libro ID: {prestamo_cod_libro[i]} "
              f"| Usuario ID: {prestamo_cod_usuario[i]} | Fecha: {fecha_prestamo[i]}")


def estadisticas():
    total_libros = len(cod_libro)
    total_prestamos = len(cod_prestamo)
    stock_total = sum(stock_disponible) if stock_disponible else 0

    print("===== ESTADÍSTICAS =====")
    print(f"Total libros: {total_libros}")
    print(f"Total préstamos activos: {total_prestamos}")
    print(f"Stock total disponible: {stock_total}")


# ===== MENU =====
def mostrar_menu():
    print("\n##### SISTEMA BIBLIOTECA #####")
    print("1- Registrar nuevo libro")
    print("2- Prestar Libro")
    print("3- Devolver Libro")
    print("4- Consultar catálogo")
    print("5- Buscar libro")
    print("6- Ver Préstamos")
    print("7- Estadísticas")
    print("0- Salir")
    print("#" * 30)


def main():
    global exit_flag

    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    print("#"*30, "\n")

    if opcion == "0":
        exit_flag = True

    elif opcion == "1":
        agregar_libro()

    elif opcion == "2":
        prestar_libro()

    elif opcion == "3":
        devolver_libro()

    elif opcion == "4":
        consultar_catalogo()

    elif opcion == "5":
        buscar_libro()

    elif opcion == "6":
        ver_prestamos()

    elif opcion == "7":
        estadisticas()

    else:
        print("Opción inválida")


# ===== RUN =====
if __name__ == "__main__":
    while not exit_flag:
        main()