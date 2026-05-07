"""
Sistema de gestión de inventario.

Este programa permite:
- Agregar productos al inventario.
- Buscar productos por código.
- Visualizar el inventario completo.
- Calcular el valor total del inventario.
- Mostrar productos con bajo stock.
- Identificar el producto más caro.

Cada producto se almacena como una tupla con la estructura:
(codigo, nombre, precio, stock)
"""


def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario un número entero validado.

    Args:
        mensaje (str): Texto que se mostrará al solicitar el dato.
        minimo (int, opcional): Valor mínimo permitido.
        maximo (int, opcional): Valor máximo permitido.

    Returns:
        int: Número entero validado ingresado por el usuario.
    """

    while True:
        try:
            valor = int(input(mensaje))

            # Validar límite mínimo
            if minimo is not None and valor < minimo:
                print(f"Error: Debe ingresar un número mayor o igual a {minimo}.")
                continue

            # Validar límite máximo
            if maximo is not None and valor > maximo:
                print(f"Error: Debe ingresar un número menor o igual a {maximo}.")
                continue

            return valor

        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


# ------------------ FUNCIONES ------------------

def agregar_producto():
    """
    Agrega un nuevo producto al inventario.

    Solicita código, nombre, precio y stock.
    Además, valida que el código no exista previamente.
    """

    global inventario

    print("\n=== AGREGAR PRODUCTO ===")

    codigo = input("Ingrese código: ").strip().upper()

    # Verificar si el código ya existe
    for producto in inventario:
        if producto[0] == codigo:
            print("Error: El código ya existe.")
            return

    nombre = input("Ingrese nombre del producto: ").strip().lower()

    # Solicitar datos numéricos validados
    precio = pedir_entero("Ingrese precio: ", minimo=1)
    stock = pedir_entero("Ingrese stock: ", minimo=0)

    # Agregar producto al inventario
    inventario.append((codigo, nombre, precio, stock))

    print("Producto agregado correctamente.")


def buscar_producto():
    """
    Busca un producto en el inventario utilizando su código.

    Si el producto existe, muestra su información.
    En caso contrario, informa que no fue encontrado.
    """

    global inventario

    print("\n=== BUSCAR PRODUCTO ===")

    codigo_buscar = input("Ingrese código del producto: ").strip().upper()

    encontrado = False

    # Recorrer inventario buscando coincidencia
    for codigo, nombre, precio, stock in inventario:

        if codigo == codigo_buscar:

            print("\nProducto encontrado:")
            print(f"Código : {codigo}")
            print(f"Nombre : {nombre.capitalize()}")
            print(f"Precio : ${precio:,.0f}")
            print(f"Stock  : {stock}")

            encontrado = True
            break

    if not encontrado:
        print("Producto no encontrado.")


def calcular_valor_total():
    """
    Calcula y muestra el valor total del inventario.

    El cálculo corresponde a:
    precio * stock de cada producto.
    """

    global inventario

    total = 0

    # Sumar el valor total de cada producto
    for _, _, precio, stock in inventario:
        total += precio * stock

    print(f"\nValor total del inventario: ${total:,.0f}")


def mostrar_productos_bajo_stock():
    """
    Muestra los productos con stock igual o inferior a 5 unidades.
    """

    global inventario

    print("\n=== PRODUCTOS CON BAJO STOCK ===")

    encontrados = False

    # Buscar productos con stock bajo
    for codigo, nombre, _, stock in inventario:

        if stock <= 5:
            print(f"{codigo} | {nombre.capitalize()} | Stock: {stock}")
            encontrados = True

    if not encontrados:
        print("No hay productos con bajo stock.")


def mostrar_producto_mas_caro():
    """
    Identifica y muestra el producto con el precio más alto.
    """

    global inventario

    # Validar que existan productos
    if not inventario:
        print("El inventario está vacío.")
        return

    producto_caro = inventario[0]

    # Comparar precios para encontrar el más caro
    for producto in inventario:

        if producto[2] > producto_caro[2]:
            producto_caro = producto

    codigo, nombre, precio, stock = producto_caro

    print("\n=== PRODUCTO MÁS CARO ===")
    print(f"Código : {codigo}")
    print(f"Nombre : {nombre.capitalize()}")
    print(f"Precio : ${precio:,.0f}")
    print(f"Stock  : {stock}")


def ver_inventario():
    """
    Muestra todos los productos almacenados en el inventario
    en formato tabla.
    """

    global inventario

    print("\n" + "=" * 60)
    print(f"{'Código':<12} | {'PRODUCTO':<20} | {'PRECIO':<12} | {'STOCK':<10}")
    print("-" * 60)

    # Verificar si el inventario está vacío
    if not inventario:
        print("El inventario está vacío.")

    else:
        # Recorrer y mostrar cada producto
        for _, (codigo, nombre, precio, stock) in enumerate(inventario):

            precio_display = f"${precio:,.0f}"

            # Mostrar indicador si no hay stock
            if stock == 0:
                stock_display = "[AGOTADO]"
            else:
                stock_display = str(stock)

            print(f"{codigo:<12} | {nombre.capitalize():<20} | {precio_display:<12} | {stock_display:<10}")

    print("=" * 60)


# ------------------ MENÚ PRINCIPAL ------------------

def main():
    """
    Ejecuta el menú principal del sistema.

    Permite acceder a todas las funcionalidades
    mediante opciones numéricas.
    """

    while True:

        print("\n=== SISTEMA INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Ver inventario")
        print("3. Buscar producto")
        print("4. Calcular valor total")
        print("5. Mostrar productos bajo stock")
        print("6. Mostrar producto más caro")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        # Validar opción ingresada
        while opcion not in ["1", "2", "3", "4", "5", "6", "0"]:
            opcion = input("Opción inválida. Ingrese una opción válida: ").strip()

        # Ejecutar opción seleccionada
        if opcion == "1":
            agregar_producto()

        elif opcion == "2":
            ver_inventario()

        elif opcion == "3":
            buscar_producto()

        elif opcion == "4":
            calcular_valor_total()

        elif opcion == "5":
            mostrar_productos_bajo_stock()

        elif opcion == "6":
            mostrar_producto_mas_caro()

        elif opcion == "0":
            print("\n¡Hasta luego!")
            break


# ------------------ EJECUCIÓN ------------------

if __name__ == "__main__":

    # Inventario inicial:
    # (codigo, nombre, precio, stock)
    inventario = [
        ("P001", "lápiz", 500, 20),
        ("P002", "cuaderno", 2500, 3),
        ("P003", "mochila", 25000, 8)
    ]

    # Iniciar programa
    main()