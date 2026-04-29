import requests
import os
import subprocess
import msvcrt
import time
from collections import deque
from colorama import Fore, Style, init

def clear_screen():
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)

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

def fetch_coingecko(monedas, retries=3, delay=20):
    """
    Obtiene el precio en USD de una lista de criptomonedas usando CoinGecko.

    Args:
        monedas (list[str]): Lista de IDs de CoinGecko.
            Ejemplo: ["bitcoin", "ethereum", "solana"]
        retries (int): Número de intentos en caso de error.
        delay (int): Segundos entre intentos.

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

    for intento in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            return {
                moneda: data.get(moneda, {}).get("usd")
                for moneda in monedas
            }

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                if intento+1==retries:
                    print(f'Intento({intento+1}) >>> Error 429: "Too Many Requests for url".')
                else:
                    print(f'Intento({intento+1}) >>> Error 429: "Too Many Requests for url". Esperando {delay} segundos...')
                    time.sleep(delay)
            else:
                print(f"HTTP error: {e}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request fallida: {e}")
            break

    return None

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
    try:
        ids = multi_select_menu(monedas, "Seleccione sus monedas:")
        precios = fetch_coingecko(ids)
        if precios == None: raise Exception;
        
        # Umbral
        clear_screen()
        umbral = float(input("Ingrese el umbral porcentual: "))

        # Estructuras
        historial = {moneda: deque(maxlen=10) for moneda in precios}
        alertas = {moneda: 0 for moneda in precios}
        precio_inicial = {}

        # Inicializar historial
        for moneda, precio in precios.items():
            historial[moneda].append(precio)
            precio_inicial[moneda] = precio

    
        while True:
            clear_screen()
            precios = fetch_coingecko(ids)
            
            if precios == None: raise Exception;
            
            clear_screen()
            
            now = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print(f"=== Monitor de criptomonedas - {now} ===")

            for moneda, precio_str in precios.items():
                cola = historial[moneda]

                # Agregar nuevo precio (deque elimina automáticamente el más viejo)
                cola.append(precio_str)

                # Mostrar precio actual

                # Inicializar columnas
                variacion_str = ""
                alerta_str = ""

                if len(cola) > 1:
                    precio_antiguo = cola[0]
                    variacion = ((precio_str - precio_antiguo) / precio_antiguo) * 100

                    # Columna variación
                    if variacion >= 0.05:
                        variacion_str = Fore.GREEN + f"↑ {variacion:+6.2f}%" + Style.RESET_ALL
                    elif variacion <= -0.05:
                        variacion_str = Fore.RED + f"↓ {variacion:+6.2f}%" + Style.RESET_ALL
                    else:
                        variacion_str = f"→ {variacion:+6.2f}%"

                    # Columna alerta
                    if abs(variacion) >= umbral:
                        alertas[moneda] += 1

                        if variacion > 0:
                            alerta_str = Fore.GREEN + f"▲ ALERTA: subida superior al {umbral}%" + Style.RESET_ALL
                        elif variacion < 0:
                            alerta_str = Fore.RED + f"▼ ALERTA: bajada superior al {umbral}%" + Style.RESET_ALL

                # Imprimir fila alineada
                print(f"{moneda:<12} {':':>3} {precio_str:>10} {variacion_str:>15} {alerta_str:>33}")

            print("Actualizando en 30 segundos... (Ctrl+C para salir)")
            time.sleep(30)

    except KeyboardInterrupt:
        clear_screen()
        print("Resumen final:\n")

        for moneda, cola in historial.items():
            inicial = precio_inicial[moneda]
            final = cola[-1]
            variacion_total = ((final - inicial) / inicial) * 100

            print(f"{moneda}:")
            print(f"  Precio inicial: ${inicial:,}")
            print(f"  Precio final: ${final:,}")
            print(f"  Variación total: {variacion_total:.2f}%")
            print(f"  Alertas: {alertas[moneda]}")
            print("-" * 40)
    except:
        print("Ocurrió un error, cerrando Programa...")
            
if __name__ == "__main__":
    main()