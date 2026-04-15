import requests
from datetime import datetime, timezone

# Monedas disponibles
MONEDAS = ["ARS", "PEN", "BRL", "COP", "USD", "EUR", "GBP", "JPY"]

# Denominaciones CLP
EFECTIVO = [20000, 10000, 5000, 2000, 1000, 500, 100, 50, 10]

def fetch_rates(base="USD"):
    #se usará la base en Dólar Americano USD como intermediario
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    data = requests.get(url).json()

    cambios = {
        "base": base,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rates": data["rates"]
    }
    return cambios

def convert_to_clp(cambios, moneda, monto):
    rates = cambios["rates"]

    # Convertir moneda -> USD -> CLP
    if moneda == "USD":
        usd = monto
    else:
        usd = monto / rates[moneda]

    clp = usd * rates["CLP"]
    return int(clp)  # truncado

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
    print("=== Conversor a CLP ===\n")

    cambios = fetch_rates()

    print("Monedas disponibles:")
    for i, m in enumerate(MONEDAS, 1):
        print(f"{i}. {m}")

    # Selección
    opcion = int(input("\nSelecciona moneda (número): "))
    moneda = MONEDAS[opcion - 1]

    # Monto
    monto = float(input(f"Ingrese monto en {moneda}: "))

    # Conversión
    clp = convert_to_clp(cambios, moneda, monto)

    # Desglose efectivo
    desglose, sobrante = breakdown_clp(clp)

    # Resultados
    print("\n--- Resultado ---")
    print(f"CLP ajustado: {clp}")

    print("\nDesglose en efectivo:")
    for d, c in desglose.items():
        print(f"{d}: {c}")

    print(f"\nSobrante (no entregado): {sobrante} CLP")

if __name__ == "__main__":
    salida_flag = False
    while (not salida_flag) :
        main()
        if input("Desea realizar otro cambio? (s/n): ").lower() != "s":
            salida_flag = True