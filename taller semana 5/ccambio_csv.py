import csv
from datetime import datetime, timezone

# Monedas disponibles
MONEDAS = ["ARS", "PEN", "BRL", "COP", "USD", "EUR", "GBP", "JPY"]

# Denominaciones CLP
EFECTIVO = [20000, 10000, 5000, 2000, 1000, 500, 100, 50, 10]

# lee el archivo csv y devuelve un diccionario con dos claves: "tasas".
def fetch_tasas_from_csv(file_path="tasas.csv"):
    tasas = {}

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            tasas[row["currency"]] = float(row["clp_per_unit"])

    return {
        "tasas": tasas
    }

# dado que las tasas del archivo ya están en clp, sólo hay que multiplicar
def convert_to_clp(data_archivo, moneda, monto):
    tasas = data_archivo["tasas"]
    return int(monto * tasas[moneda])

# obtiene el desglose de efectivo
def breakdown_clp(monto):
    restante = monto
    desglose = {} #diccionario vacío para almacenar el desglose

    for d in EFECTIVO:
        cantidad = restante // d #division entera sin decimales
        if cantidad > 0:
            desglose[d] = int(cantidad) # se usa el billete/moneda como clave y se asigna con la cantidad
            restante -= d * cantidad
        if restante == 0: #evita iteraciones innecesarias
            break
    return desglose, restante

# proceso principal
def main():
    print("=== Conversor a CLP (CSV directo CLP tasas) ===\n")

    data_archivo = fetch_tasas_from_csv()

    print("Monedas disponibles:")
    for i, valor in enumerate(MONEDAS, 1): #recorre lista MONEDAS con índice i=1 y valor al mismo tiempo.
        print(f"{i}. {valor}")

    opcion = int(input("\nSelecciona moneda (número): "))
    moneda = MONEDAS[opcion - 1]

    monto = float(input(f"Ingrese monto en {moneda}: "))

    clp = convert_to_clp(data_archivo, moneda, monto)

    desglose, sobrante = breakdown_clp(clp)

    print("\n--- Resultado ---")
    print(f"CLP total: {clp}")

    print("\nDesglose en efectivo:")
    for d, c in desglose.items():
        print(f"{d}: {c}")

    print(f"\nSobrante (no entregado): {sobrante} CLP")

while True:
    main()
    if input("Desea realizar otro cambio? (S/N): ").lower() != "s":
        break