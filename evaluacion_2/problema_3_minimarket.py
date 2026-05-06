import os
# ------------------ FUNCIONES ------------------

def cargar_inventario():
    global inventario
    try:
        with open("inventario.txt", "r") as f:
            inventario = []
            for linea in f:
                nombre, precio, stock = linea.strip().split(";")
                inventario.append({
                    "nombre": nombre,
                    "precio": float(precio),
                    "stock": int(stock)
                })
        print("Inventario cargado correctamente")
    except:
        print("Error al cargar inventario")
    input("Presione ENTER para continuar...")


def ver_inventario():
    os.system("cls" if os.name == "nt" else "clear")
    print("INVENTARIO")
    print("-----------")

    if not inventario:
        print("Inventario vacío")
    else:
        for p in inventario:
            print(f"{p['nombre']} - ${p['precio']} - Stock: {p['stock']}")

    input("\nPresione ENTER para continuar...")


def registrar_venta():
    global ventas_dia

    if not inventario:
        print("Debe cargar el inventario primero")
        input("ENTER para continuar...")
        return

    print("\nPRODUCTOS DISPONIBLES")
    print("----------------------")

    for i, p in enumerate(inventario):
        print(f"{i+1}. {p['nombre']} (${p['precio']}) Stock: {p['stock']}")

    try:
        opcion = int(input("\nSeleccione producto: "))
        if opcion < 1 or opcion > len(inventario):
            print("Opción inválida")
            input("ENTER...")
            return

        cantidad = int(input("Cantidad: "))
        if cantidad <= 0:
            print("Cantidad inválida")
            input("ENTER...")
            return

        producto = inventario[opcion - 1]

        if cantidad > producto["stock"]:
            print("Stock insuficiente")
        else:
            total = cantidad * producto["precio"]
            producto["stock"] -= cantidad

            ventas_dia.append({
                "nombre": producto["nombre"],
                "cantidad": cantidad,
                "total": total
            })

            print(f"Venta realizada. Total: ${total}")

    except:
        print("Error en los datos ingresados")

    input("Presione ENTER para continuar...")


def ver_resumen():
    print("\nRESUMEN DEL DÍA")
    print("----------------")

    total_general = 0

    if not ventas_dia:
        print("No hay ventas registradas")
    else:
        for v in ventas_dia:
            print(f"{v['nombre']} x{v['cantidad']} = ${v['total']}")
            total_general += v["total"]

        print("----------------")
        print(f"TOTAL: ${total_general}")

    input("\nPresione ENTER para continuar...")


def cerrar_caja():
    total_general = 0

    with open("resumen_dia.txt", "w") as f:
        for v in resumen_dia:
            linea = f"{v['nombre']},{v['cantidad']},{v['total']}\n"
            f.write(linea)
            total_general += v["total"]

        f.write(f"TOTAL,{total_general}")

    print("Caja cerrada y guardada correctamente")
    input("Presione ENTER para continuar...")


# ------------------ MENÚ PRINCIPAL ------------------

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("=== SISTEMA MINIMARKET ===")
        print("1. Cargar inventario desde archivo")
        print("2. Registrar venta")
        print("3. Ver inventario")
        print("4. Ver resumen del día")
        print("5. Cerrar caja y guardar")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

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
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")


# ------------------ EJECUCIÓN ------------------
if __name__ == "__main__":
    inventario = []
    resumen_dia = []
    main()