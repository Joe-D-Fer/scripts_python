import requests
import os
import subprocess
import msvcrt
import time
from collections import deque
from colorama import Fore, Style, init

def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


def multi_select_menu(options, title="Seleccione sus opciones"):
    """
    Menú multiselección.

    Controles:
        ↑ ↓ : navegar
        ESPACIO : seleccionar
        ENTER : confirmar
        ESC : salir
    """
    selected = [False] * len(options)
    cursor = 0

    while True:
        clear_screen()
        print(title)
        print("-" * len(title))
        print("↑ ↓ Navegar | ESPACIO Seleccionar | ENTER Confirmar | ESC Salir\n")

        for i, (display_name, _) in enumerate(options):
            pointer = ">" if i == cursor else " "
            mark = "[x]" if selected[i] else "[ ]"
            print(f"{pointer} {mark} {display_name}")

        key = msvcrt.getch()

        if key == b"\xe0": # Prefijo de teclas especiales (flechas, Insert, Delete, etc.)
            key = msvcrt.getch()

            if key == b"H": # Flecha Arriba
                cursor = (cursor - 1) % len(options)

            elif key == b"P": # Flecha Abajo
                cursor = (cursor + 1) % len(options)

        elif key == b" ": # Barra espaciadora
            selected[cursor] = not selected[cursor]

        elif key == b"\r": # Enter
            return [
                api_id
                for (_, api_id), is_selected in zip(options, selected)
                if is_selected
            ]

        elif key == b"\x1b":  # Esc
            return None
        elif key == b'\x03':  # Ctrl+C
            return None


def fetch_coingecko(monedas, retries=3, delay=20):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(monedas),
        "vs_currencies": "usd"
    }

    for intento in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                moneda: data.get(moneda, {}).get("usd")
                for moneda in monedas
            }

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                if intento + 1 < retries:
                    print(
                        f'Intento {intento + 1}: demasiadas solicitudes. '
                        f'Reintentando en {delay} segundos...'
                    )
                    time.sleep(delay)
                else:
                    print("Error: límite de solicitudes alcanzado.")
            else:
                print(f"HTTP Error: {e}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            break

    return None


def imprimir_resumen(historial, precio_inicial, alertas):
    clear_screen()
    print("=== RESUMEN FINAL ===\n")

    for moneda, cola in historial.items():
        inicial = precio_inicial[moneda]
        final = cola[-1]
        variacion = ((final - inicial) / inicial) * 100

        color = (
            Fore.GREEN if variacion > 0
            else Fore.RED if variacion < 0
            else ""
        )

        print(f"{moneda.upper()}")
        print(f"  Precio inicial : ${inicial:>15,.8f}")
        print(f"  Precio final   : ${final:>15,.8f}")
        print(f"  Variación total: {color}{variacion:>14.2f}%{Style.RESET_ALL}")
        print(f"  Alertas        : {alertas[moneda]:>15}")
        print("-" * 55)


def main():
    # Tiempo entre consultas
    intervalo_request = 30
    # Inicializar Colorama
    init(autoreset=True)

    monedas = [
        ("Bitcoin", "bitcoin"),
        ("Ethereum", "ethereum"),
        ("Solana", "solana"),
        ("Binance Coin", "binancecoin"),
        ("Avalanche", "avalanche-2"),
        ("Chainlink", "chainlink"),
        ("Arbitrum", "arbitrum"),
        ("Sui", "sui"),
        ("Render", "render-token"),
        ("Pepe", "pepe"),
    ]

    try:
        titulo = "Seleccione sus criptomonedas"
        while True:
            ids = multi_select_menu(monedas, titulo)

            if ids is None:
                print("\nPrograma cancelado por el usuario.")
                return

            if not ids:
                titulo="Debe seleccionar al menos una criptomoneda."
            else:
                break

        precios = fetch_coingecko(ids)

        if precios is None:
            print("No fue posible obtener los precios iniciales.")
            return

        clear_screen()
        umbral = float(input("Ingrese el umbral porcentual de alerta: "))

        historial = {moneda: deque(maxlen=10) for moneda in ids}
        alertas = {moneda: 0 for moneda in ids}
        precio_inicial = {}

        for moneda, precio in precios.items():
            historial[moneda].append(precio)
            precio_inicial[moneda] = precio

        while True:
            precios = fetch_coingecko(ids)

            if precios is None:
                print("No se pudieron actualizar los precios.")
                time.sleep(5)
                continue

            clear_screen()

            now = time.strftime("%d/%m/%Y %H:%M:%S")
            print(f"=== Monitor de Criptomonedas - {now} ===\n")

            for moneda, precio_actual in precios.items():
                cola = historial[moneda]
                cola.append(precio_actual)

                variacion_str = ""
                alerta_str = ""

                if len(cola) > 1:
                    precio_antiguo = cola[0]
                    variacion = ((precio_actual - precio_antiguo) / precio_antiguo) * 100
                    if variacion > 0:
                        variacion_str = (
                            f"{Fore.GREEN}"
                            f"↑{variacion:+7.2f}%"
                            f"{Style.RESET_ALL}"
                        )

                    elif variacion < 0:
                        variacion_str = (
                            f"{Fore.RED}"
                            f"↓{variacion:+7.2f}%"
                            f"{Style.RESET_ALL}"
                        )

                    else:
                        variacion_str = (
                            f"→{variacion:+7.2f}%"
                        )

                    if abs(variacion) >= umbral:
                        alertas[moneda] += 1

                        if variacion > 0:
                            alerta_str = (
                                f"{Fore.GREEN}"
                                f"▲ ALERTA: subida superior al {umbral}%"
                                f"{Style.RESET_ALL}"
                            )
                        else:
                            alerta_str = (
                                f"{Fore.RED}"
                                f"▼ ALERTA: bajada superior al {umbral}%"
                                f"{Style.RESET_ALL}"
                            )
                    # Cada consulta ocurre cada 30 segundos
                    tiempo_str = ""

                    if len(cola) > 1:
                        # Número de intervalos entre el primer y último precio
                        segundos = (len(cola) - 1) * intervalo_request

                        if segundos >= 60:
                            minutos = segundos // 60
                            tiempo_str = f"(vs hace {minutos} min)"
                        else:
                            tiempo_str = f"(vs hace {segundos} seg)"
                print(
                    f"{moneda:<15}"
                    f"{":":>2}"
                    f" USD {precio_actual:>15,.6f}   "
                    f"{variacion_str:>2} {tiempo_str}"
                    f" {alerta_str}"
                )

            print(f"\nActualizando en {intervalo_request} segundos... (Ctrl+C para salir)")
            time.sleep(intervalo_request)

    except KeyboardInterrupt:
        imprimir_resumen(historial, precio_inicial, alertas)

    except ValueError:
        print("Debe ingresar un número válido para el umbral.")

    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()