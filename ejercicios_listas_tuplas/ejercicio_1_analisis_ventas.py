"""
Sistema de análisis de ventas diarias.

Este programa permite ingresar ventas diarias, validar datos y generar un
informe completo con métricas como total, promedio, mayor/menor venta,
cumplimiento de meta, rachas y gráfico simple en consola.
"""


def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario un número entero validado.

    Repite la solicitud hasta que el usuario ingrese un valor válido,
    respetando límites mínimo y máximo si están definidos.

    Args:
        mensaje (str): Texto mostrado al usuario.
        minimo (int, optional): Valor mínimo permitido.
        maximo (int, optional): Valor máximo permitido.

    Returns:
        int: Número entero válido ingresado por el usuario.
    """
    while True:
        try:
            valor = int(input(mensaje))

            # Validación de mínimo
            if minimo is not None and valor < minimo:
                print(f"Error: Debe ingresar un número >= {minimo}.")
                continue

            # Validación de máximo
            if maximo is not None and valor > maximo:
                print(f"Error: Debe ingresar un número <= {maximo}.")
                continue

            return valor

        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


# ------------------ FUNCIONES DE ANÁLISIS ------------------

def calcular_total_y_promedio(ventas):
    """
    Calcula el total y el promedio de ventas.

    Args:
        ventas (list): Lista de ventas diarias.

    Returns:
        tuple: (total, promedio)
    """
    total = sum(ventas)
    promedio = total / len(ventas)
    return total, promedio


def obtener_mayor_y_menor(ventas):
    """
    Obtiene la mayor y menor venta junto con su día correspondiente.

    Args:
        ventas (list): Lista de ventas diarias.

    Returns:
        tuple: (dia_mayor, mayor, dia_menor, menor)
    """
    mayor = max(ventas)
    menor = min(ventas)

    dia_mayor = ventas.index(mayor) + 1
    dia_menor = ventas.index(menor) + 1

    return dia_mayor, mayor, dia_menor, menor


def calcular_cumplimiento_meta(ventas, meta):
    """
    Calcula cuántos días se cumplió la meta y su porcentaje.

    Args:
        ventas (list): Ventas diarias.
        meta (int): Meta diaria de ventas.

    Returns:
        tuple: (dias_cumplidos, porcentaje)
    """
    dias_cumplidos = 0

    for venta in ventas:
        if venta >= meta:
            dias_cumplidos += 1

    porcentaje = (dias_cumplidos / len(ventas)) * 100

    return dias_cumplidos, porcentaje


def calcular_diferencia_meta(ventas, meta):
    """
    Calcula la diferencia entre ventas reales y meta total.

    Args:
        ventas (list): Ventas diarias.
        meta (int): Meta diaria.

    Returns:
        int: Diferencia total (positivo o negativo).
    """
    meta_total = meta * len(ventas)
    total_vendido = sum(ventas)

    return total_vendido - meta_total


def obtener_top_3(ventas):
    """
    Obtiene los 3 días con mayores ventas.

    Args:
        ventas (list): Ventas diarias.

    Returns:
        list: Lista de tuplas (día, venta)
    """
    dias_ventas = [(i + 1, venta) for i, venta in enumerate(ventas)]

    # Ordena por ventas de mayor a menor
    dias_ventas.sort(key=lambda x: x[1], reverse=True)

    return dias_ventas[:3]


def dias_sobre_promedio(ventas):
    """
    Obtiene los días con ventas sobre el promedio.

    Args:
        ventas (list): Ventas diarias.

    Returns:
        list: Lista de tuplas (día, venta)
    """
    promedio = sum(ventas) / len(ventas)

    return [(i + 1, venta) for i, venta in enumerate(ventas) if venta > promedio]


def racha_maxima_meta(ventas, meta):
    """
    Calcula la racha más larga de días cumpliendo la meta.

    Args:
        ventas (list): Ventas diarias.
        meta (int): Meta diaria.

    Returns:
        int: Máxima racha consecutiva.
    """
    racha_actual = 0
    racha_maxima = 0

    for venta in ventas:
        if venta >= meta:
            racha_actual += 1
            racha_maxima = max(racha_maxima, racha_actual)
        else:
            racha_actual = 0

    return racha_maxima


# ------------------ MAIN ------------------

def main():
    """
    Función principal del programa.

    Solicita datos al usuario, calcula métricas y muestra un informe
    completo de análisis de ventas.
    """
    global ventas

    # Entrada de datos
    cantidad_dias = pedir_entero("Ingrese la cantidad de días: ", minimo=5)
    meta_ventas = pedir_entero("Ingrese la meta de ventas diaria: ", minimo=1)

    for i in range(cantidad_dias):
        venta = pedir_entero(
            f"Ingrese ventas del día {i + 1}: ",
            minimo=1
        )
        ventas.append(venta)

    print("\n===== ANÁLISIS DE VENTAS =====")

    print(f"Días registrados     : {cantidad_dias}")
    print(f"Meta diaria          : ${meta_ventas:,}")

    # Total y promedio
    total, promedio = calcular_total_y_promedio(ventas)
    print(f"Total vendido        : ${total:,}")
    print(f"Promedio diario      : ${promedio:,.0f}")

    # Mayor y menor
    dia_mayor, mayor, dia_menor, menor = obtener_mayor_y_menor(ventas)
    print(f"Mayor venta          : Día {dia_mayor} -> ${mayor:,}")
    print(f"Menor venta          : Día {dia_menor} -> ${menor:,}")

    # Cumplimiento meta
    dias, porcentaje = calcular_cumplimiento_meta(ventas, meta_ventas)
    print(f"Días cumplidos       : {dias} ({porcentaje:.1f}%)")

    # Diferencia meta
    diferencia = calcular_diferencia_meta(ventas, meta_ventas)

    if diferencia > 0:
        print(f"Diferencia           : +${diferencia:,} (sobre meta)")
    elif diferencia < 0:
        print(f"Diferencia           : -${abs(diferencia):,} (bajo meta)")
    else:
        print(f"Diferencia           : $0 (en la meta)")

    # Racha
    racha = racha_maxima_meta(ventas, meta_ventas)
    print(f"Racha máxima         : {racha} día(s)")

    # Top 3
    print("\nTOP 3 DÍAS:")
    for i, (dia, venta) in enumerate(obtener_top_3(ventas), 1):
        print(f"{i}. Día {dia} -> ${venta:,}")

    # Sobre promedio
    print("\nDías sobre el promedio:")
    for dia, venta in dias_sobre_promedio(ventas):
        print(f"Día {dia}: ${venta:,}")

    # Gráfico simple
    print("\n===== GRÁFICO DE VENTAS =====")
    max_venta = max(ventas)
    escala = 50 / max_venta

    for i, venta in enumerate(ventas, 1):
        barras = int(venta * escala)
        print(f"Día {i:2} | ${venta:8,} | {'*' * barras}")


# ------------------ EJECUCIÓN ------------------

if __name__ == "__main__":
    ventas = []
    main()