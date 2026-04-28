import requests

def obtener_precios_coingecko(monedas):
    """
    Obtiene el precio en USD de una lista de criptomonedas usando CoinGecko.

    Args:
        monedas (list[str]): Lista de IDs de CoinGecko.
            Ejemplo: ["bitcoin", "ethereum", "solana"]

    Returns:
        dict: Diccionario con los precios.
            Ejemplo:
            {
                "bitcoin": 64000,
                "ethereum": 3200,
                "solana": 140
            }
    """
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(monedas),
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return {
        moneda: data.get(moneda, {}).get("usd")
        for moneda in monedas
    }
def main():
    monedas = ["bitcoin", "ethereum", "solana"]
    precios = obtener_precios_coingecko(monedas)

    for moneda, precio in precios.items():
        print(f"{moneda}: ${precio:,} USD")

while True:
    main()
    if input("continuar? (s/n)").lower()!="s":break;