def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))

            if minimo is not None and valor < minimo:
                print(f"Error: Debe ingresar un número mayor o igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Error: Debe ingresar un número menor o igual a {maximo}.")
                continue

            return valor

        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


def cargar_inventario():
    global nombres, precios, stocks
    try:
        with open("inventario.txt", "r") as f:
            # Saltamos la primera línea (encabezado)
            next(f)

            # Reiniciamos las listas para evitar duplicados si se llama la función varias veces
            nombres = []
            precios = []
            stocks = []

            for num_linea, linea in enumerate(f, start=2):
                try:
                    # Separamos los datos por el punto y coma
                    nombre, precio, stock = linea.strip().split(";")

                    # Agregamos cada dato a su lista correspondiente
                    nombres.append(nombre)
                    precios.append(float(precio))
                    stocks.append(int(stock))

                except ValueError:
                    print(f"Error de formato en la línea {num_linea}: '{linea.strip()}'")

        cantidad = len(nombres)
        print(f"\nInventario cargado correctamente. Se encontraron {cantidad} productos.")

    except FileNotFoundError:
        print("Error: El archivo 'inventario.txt' no existe.")
    except PermissionError:
        print("Error: No tienes permisos para leer 'inventario.txt'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def ver_inventario():
    global nombres, precios, stocks

    print("\n" + "="*50)
    print(f"{'N°':<3} | {'PRODUCTO':<20} | {'PRECIO':<12} | {'STOCK':<10}")
    print("-" * 50)

    # Verificamos si hay productos cargados
    if not nombres:
        print("El inventario está vacío.")
    else:
        # Recorremos las listas usando el índice
        for i in range(len(nombres)):
            nombre = nombres[i]
            precio = f"${precios[i]:,.0f}"

            # Lógica para la etiqueta [AGOTADO]
            if stocks[i] == 0:
                stock_display = "[AGOTADO]"
            else:
                stock_display = str(stocks[i])

            # Formateamos la línea con alineación
            print(f"{i+1:<3} | {nombre.capitalize():<20} | {precio:<12} | {stock_display:<10}")

    print("="*50)


def registrar_venta():
    global nombres, precios, stocks
    global productos_vendidos, cantidades_vendidas, subtotales
    global cerrar_caja_flag

    print("\n--- REGISTRAR VENTA ---")
    busqueda = input("Ingrese el nombre del producto: ").strip().lower()

    # 1. Buscar el producto (sin distinguir mayúsculas/minúsculas)
    indice_encontrado = -1
    for i in range(len(nombres)):
        if nombres[i].lower() == busqueda:
            indice_encontrado = i
            break

    # 2. Validar existencia
    if indice_encontrado == -1:
        print(f"Error: El producto '{busqueda}' no existe en el inventario.")
        return

    if stocks[indice_encontrado] == 0:
        print(f"El producto '{nombres[indice_encontrado]}' está agotado.")
        return

    # 3. Si existe, pedir cantidad
    cantidad = pedir_entero(
        f"Cantidad deseada (Stock actual: {stocks[indice_encontrado]}): ",
        minimo=1,
        maximo=stocks[indice_encontrado]
    )

    # 4. Procesar venta
    # Descontar stock
    stocks[indice_encontrado] -= cantidad

    # Calcular subtotal
    precio_unitario = precios[indice_encontrado]
    subtotal = precio_unitario * cantidad

    # Registrar en listas de ventas
    productos_vendidos.append(nombres[indice_encontrado])
    cantidades_vendidas.append(cantidad)
    subtotales.append(subtotal)

    # Si se había cerrado caja antes, ahora hay ventas nuevas sin guardar
    cerrar_caja_flag = False

    # 5. Mostrar boleta simple
    print("\n" + "="*30)
    print("        BOLETA DE VENTA")
    print("="*30)
    print(f"Producto:    {nombres[indice_encontrado].capitalize()}")
    print(f"Cantidad:    {cantidad}")
    print(f"Precio Unit: ${precio_unitario:,.0f}")
    print("-" * 30)
    print(f"Subtotal:       ${subtotal:,.0f}")
    print("="*30)


def ver_resumen():
    global productos_vendidos, cantidades_vendidas, subtotales

    print("\n" + "="*50)
    print(f"{'VENTAS DEL DÍA':^50}")  # Título centrado
    print("="*50)

    # 1. Verificar si hay ventas registradas
    if not productos_vendidos:
        print("\n   Aún no se han registrado ventas.\n")
    else:
        print(f"{'N°':<3} | {'PRODUCTO':<20} | {'CANTIDAD':<10} | {'SUBTOTAL':<12}")
        print("-" * 50)

        total_recaudado = 0

        # 2. Recorrer las listas de ventas
        for i in range(len(productos_vendidos)):
            producto = productos_vendidos[i]
            cantidad = cantidades_vendidas[i]
            subtotal = subtotales[i]

            # Acumulamos para el total general
            total_recaudado += subtotal

            # Imprimimos la fila de la tabla
            print(f"{i+1:<3} | {producto.capitalize():<20} | {cantidad:<10} | ${subtotal:<12,.0f}")

        # 3. Mostrar el total recaudado al final
        print("-" * 50)
        print(f"{'TOTAL RECAUDADO:':<33} ${total_recaudado:,.0f}")

    print("="*50)


def cerrar_caja():
    global productos_vendidos, cantidades_vendidas, subtotales
    global cerrar_caja_flag

    # 1. Verificar si hubo ventas antes de generar el archivo
    if not productos_vendidos:
        print("\nNo se puede cerrar caja: No hay ventas registradas hoy.")
        return

    try:
        with open("resumen_dia.txt", "w", encoding="utf-8") as f:
            # Escribir encabezados en el archivo
            f.write("="*50 + "\n")
            f.write(f"{'RESUMEN DE VENTAS DEL DÍA':^50}\n")
            f.write("="*50 + "\n")
            f.write(f"{'N°':<3} | {'PRODUCTO':<20} | {'CANTIDAD':<10} | {'SUBTOTAL':<12}\n")
            f.write("-" * 50 + "\n")

            total_recaudado = 0

            # 2. Recorrer las listas y escribir cada línea
            for i in range(len(productos_vendidos)):
                producto = productos_vendidos[i]
                cantidad = cantidades_vendidas[i]
                subtotal = subtotales[i]
                total_recaudado += subtotal

                f.write(f"{i+1:<3} | {producto.capitalize():<20} | {cantidad:<10} | ${subtotal:<12,.0f}\n")

            # 3. Escribir el total final
            f.write("-" * 50 + "\n")
            f.write(f"{'TOTAL RECAUDADO:':<33} ${total_recaudado:,.0f}\n")
            f.write("="*50 + "\n")

        cerrar_caja_flag = True  # Indicamos que se ha cerrado caja
        print("\nCaja cerrada. Resumen guardado en 'resumen_dia.txt'")

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


def confirmar_salida():
    global productos_vendidos, cerrar_caja_flag

    # Caso 1: No hay ventas o la caja ya se cerró
    if not productos_vendidos or cerrar_caja_flag:
        print("\nSaliendo del sistema...")
        return True

    # Caso 2: Hay ventas sin guardar
    print("\n" + "!"*45)
    print(" ADVERTENCIA: Hay ventas que no se han guardado.")
    print("!"*45)

    while True:
        res = input("¿Desea cerrar caja antes de salir? (s/n/cancelar): ").lower().strip()

        if res == "s":
            cerrar_caja()
            return True  # Sale después de guardar

        elif res == "n":

            while True:
                confirmar = input("¿Está SEGURO de que desea salir sin guardar? (s/n): ").lower().strip()

                if confirmar == "s":
                    print("Saliendo sin guardar...")
                    return True

                elif confirmar == "n":
                    return False  # El usuario se arrepintió, vuelve al menú

                else:
                    print("Opción no válida. Escriba 's' o 'n'.")

        elif res == "cancelar":
            return False  # Regresa al menú

        else:
            print("Opción no válida. Escriba 's', 'n' o 'cancelar'.")


# ------------------ MENÚ PRINCIPAL ------------------

def main():
    while True:

        print("\n=== SISTEMA MINIMARKET ===")
        print("1. Cargar inventario desde archivo")
        print("2. Registrar venta")
        print("3. Ver inventario actual")
        print("4. Ver resumen de ventas del día")
        print("5. Cerrar caja y guardar resumen")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        while opcion not in ["1", "2", "3", "4", "5", "0"]:
            opcion = input("Opción inválida. Ingrese una opción válida: ").strip()

        if opcion == "1":
            cargar_inventario()

        elif opcion == "2":
            registrar_venta()

        elif opcion == "3":
            ver_inventario()

        elif opcion == "4":
            ver_resumen()

        elif opcion == "5":
            cerrar_caja()

        elif opcion == "0":
            if confirmar_salida():
                print("\n¡Hasta luego!")
                break  # Rompe el ciclo while True y termina el programa


# ------------------ EJECUCIÓN ------------------
if __name__ == "__main__":
    # Listas globales para almacenar datos
    nombres = []
    precios = []
    stocks = []
    productos_vendidos = []
    cantidades_vendidas = []
    subtotales = []
    resumen_dia = []
    cerrar_caja_flag = False  # flag para controlar el cierre de caja

    cargar_inventario()  # Cargamos el inventario al iniciar el programa
    main()