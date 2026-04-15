import csv
from datetime import datetime, timezone

# Monedas disponibles
MONEDAS = ["ARS", "PEN", "BRL", "COP", "USD", "EUR", "GBP", "JPY"]

# Denominaciones CLP
EFECTIVO = [20000, 10000, 5000, 2000, 1000, 500, 100, 50, 10]


def fetch_rates_from_csv(file_path="rates.csv"):
    rates = {}

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rates[row["currency"]] = float(row["clp_per_unit"])

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rates": rates
    }


def convert_to_clp(cambios, moneda, monto):
    rates = cambios["rates"]
    return int(monto * rates[moneda])


def breakdown_clp(monto):
    restante = monto
    desglose = {}

    for d in EFECTIVO:
        cantidad = restante // d
        if cantidad > 0:
            desglose[d] = int(cantidad)
            restante -= d * cantidad

    return desglose, restante


def main():
    print("=== Conversor a CLP (CSV directo CLP rates) ===\n")

    cambios = fetch_rates_from_csv()

    print("Monedas disponibles:")
    for i, m in enumerate(MONEDAS, 1):
        print(f"{i}. {m}")

    opcion = int(input("\nSelecciona moneda (número): "))
    moneda = MONEDAS[opcion - 1]

    monto = float(input(f"Ingrese monto en {moneda}: "))

    clp = convert_to_clp(cambios, moneda, monto)

    desglose, sobrante = breakdown_clp(clp)

    print("\n--- Resultado ---")
    print(f"CLP total: {clp}")

    print("\nDesglose en efectivo:")
    for d, c in desglose.items():
        print(f"{d}: {c}")

    print(f"\nSobrante (no entregado): {sobrante} CLP")


if __name__ == "__main__":
    while True:
        main()
        if input("Desea realizar otro cambio? (s/n): ").lower() != "s":
            break