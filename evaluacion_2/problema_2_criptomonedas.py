import requests
import os
import msvcrt


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def multi_select_menu(options, title="Seleccione sus opciones"):
    """
    Menú multiselección.

    Args:
        options: Lista de tuplas de la forma:
                 (display_name, api_id)

    Returns:
        list[str]: API IDs Seleccionadas
    """
    selected = [False] * len(options)
    cursor = 0

    while True:
        clear_screen()
        print(title)
        print("-" * len(title))
        print("Usa ↑ ↓ para navegar, ESPACIO para seleccionar, ENTER para confirmar.\n")

        for i, (display_name, _) in enumerate(options):
            pointer = ">" if i == cursor else " "
            mark = "[x]" if selected[i] else "[ ]"
            print(f"{pointer} {mark} {display_name}")

        key = msvcrt.getch()

        if key == b"\xe0":
            key = msvcrt.getch()
            if key == b"H":      # Up
                cursor = (cursor - 1) % len(options)
            elif key == b"P":    # Down
                cursor = (cursor + 1) % len(options)

        elif key == b" ":
            selected[cursor] = not selected[cursor]

        elif key == b"\r":
            return [
                api_id
                for (_, api_id), is_selected in zip(options, selected)
                if is_selected
            ]


def fetch_coingecko(monedas):
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
    clear_screen()
    monedas = [
        ("Bitcoin", "bitcoin"),
        ("Ethereum", "ethereum"),
        ("Solana", "solana"),
        ("Cardano", "cardano"),
        ("Binance Coin", "binancecoin"),
        ("Avalanche", "avalanche-2")
    ]
    ids = multi_select_menu(monedas, "Seleccione sus monedas:")
    precios = fetch_coingecko(ids)
    
    clear_screen()
    input("Ingrese el umbral porcentual: ")
    print("+"*30)
    for moneda, precio in precios.items():
        print(f"{moneda}: ${precio:,} USD")

while True:
    main()
    if input("continuar? (s/n)").lower()!="s":break;