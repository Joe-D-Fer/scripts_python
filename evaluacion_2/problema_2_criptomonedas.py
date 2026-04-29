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
    Menú multiselección para Windows.
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

        if key == b"\xe0": # Teclas especiales
            key = msvcrt.getch()
            if key == b"H": # Arriba
                cursor = (cursor - 1) % len(options)
            elif key == b"P": # Abajo
                cursor = (cursor + 1) % len(options)
        elif key == b" ": # Espacio
            selected[cursor] = not selected[cursor]
        elif key == b"\r": # Enter
            return [api_id for (_, api_id), is_selected in zip(options, selected) if is_selected]
        elif key == b"\x1b" or key == b'\x03':  # Esc o Ctrl+C
            return None

def fetch_coingecko(monedas, retries=3, delay=20):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(monedas), "vs_currencies": "usd"}

    for intento in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {moneda: data.get(moneda, {}).get("usd") for moneda in monedas}
        except requests.exceptions.HTTPError:
            if response.status_code == 429 and intento + 1 < retries:
                print(f"Límite de API. Reintentando en {delay}s...")
                time.sleep(delay)
            else:
                break
        except Exception as e:
            print(f"Error de conexión: {e}")
            break
    return None

def imprimir_resumen(historial, precio_inicial, alertas):
    clear_screen()
    print("=== RESUMEN FINAL ===\n")
    if not precio_inicial:
        print("No se recolectaron datos.")
        return

    for moneda, cola in historial.items():
        if not cola: continue
        inicial = precio_inicial[moneda]
        final = cola[-1]
        variacion = ((final - inicial) / inicial) * 100
        color = Fore.GREEN if variacion > 0 else Fore.RED if variacion < 0 else ""

        print(f"{moneda.upper()}")
        print(f"  Precio inicial : ${inicial:>15,.8f}")
        print(f"  Precio final   : ${final:>15,.8f}")
        print(f"  Variación total: {color}{variacion:>14.2f}%{Style.RESET_ALL}")
        print(f"  Alertas        : {alertas[moneda]:>15}")
        print("-" * 55)

def main():
    intervalo_request = 30
    init(autoreset=True)

    monedas_disponibles = [
        ("Bitcoin", "bitcoin"), ("Ethereum", "ethereum"), ("Solana", "solana"),
        ("Binance Coin", "binancecoin"), ("Avalanche", "avalanche-2"),
        ("Chainlink", "chainlink"), ("Arbitrum", "arbitrum"), ("Sui", "sui"),
        ("Render", "render-token"), ("Pepe", "pepe"),
    ]

    try:
        # 1. Selección de monedas
        titulo_menu = "Seleccione sus criptomonedas"
        while True:
            ids = multi_select_menu(monedas_disponibles, titulo_menu)
            if ids is None: return
            if not ids:
                titulo_menu = "DEBE SELECCIONAR AL MENOS UNA:"
            else: break

        clear_screen()
        umbral = float(input("Ingrese el umbral porcentual de alerta (ej. 0.2): "))

        # 2. Configuración de almacenamiento
        historial = {moneda: deque(maxlen=10) for moneda in ids}
        alertas = {moneda: 0 for moneda in ids}
        precio_inicial = {}

        # 3. Bucle principal de monitoreo
        while True:
            precios = fetch_coingecko(ids)
            
            if precios is None:
                print("Error obteniendo precios. Reintentando en 5s...")
                time.sleep(5)
                continue

            # Guardar precios iniciales solo en la primera respuesta exitosa
            if not precio_inicial:
                precio_inicial = precios.copy()

            clear_screen()
            now = time.strftime("%d/%m/%Y %H:%M:%S")
            print(f"=== Monitor de Criptomonedas - {now} ===\n")

            for moneda, precio_actual in precios.items():
                if precio_actual is None: continue
                
                cola = historial[moneda]
                cola.append(precio_actual)

                variacion_str = ""
                alerta_str = ""
                tiempo_str = ""

                # Cálculos solo si hay historia previa (más de 1 elemento)
                if len(cola) > 1:
                    precio_antiguo = cola[0]
                    variacion = ((precio_actual - precio_antiguo) / precio_antiguo) * 100
                    
                    # Formatear flecha de variación
                    if variacion > 0:
                        variacion_str = f"{Fore.GREEN}↑{variacion:+7.2f}%{Style.RESET_ALL}"
                    elif variacion < 0:
                        variacion_str = f"{Fore.RED}↓{variacion:+7.2f}%{Style.RESET_ALL}"
                    else:
                        variacion_str = f"→{variacion:+7.2f}%"

                    # Gestión de Alertas
                    if abs(variacion) >= umbral:
                        alertas[moneda] += 1
                        color_alert = Fore.GREEN if variacion > 0 else Fore.RED
                        icono = "▲" if variacion > 0 else "▼"
                        alerta_str = f"{color_alert}{icono} ALERTA: cambio > {umbral}%{Style.RESET_ALL}"

                    # Cálculo de tiempo relativo
                    segundos = (len(cola) - 1) * intervalo_request
                    if segundos >= 60:
                        tiempo_str = f"(vs hace {segundos // 60} min)"
                    else:
                        tiempo_str = f"(vs hace {segundos} seg)"

                # Impresión de fila
                print(
                    f"{moneda:<15}:"
                    f" USD {precio_actual:>15,.6f}   "
                    f"{variacion_str:>2} {tiempo_str:<18} "
                    f"{alerta_str}"
                )

            print(f"\nActualizando en {intervalo_request}s... (Ctrl+C para salir y ver resumen)")
            time.sleep(intervalo_request)

    except KeyboardInterrupt:
        imprimir_resumen(historial, precio_inicial, alertas)
    except ValueError:
        print("Error: El umbral debe ser un número.")
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()