import random
from collections import deque
# Semilla para reproducibilidad
random.seed(42)

HORA_INICIO = 9 * 60
HORA_CIERRE = 13 * 60

clientes = []

# ====== INGRESO MANUAL DE PACIENTES ======
print("¿Deseas ingresar pacientes manualmente? (s/n)")
op = input().lower()

turno_manual = 1

if op == "s":
    while True:
        nombre = input("Nombre del paciente (o ENTER para terminar): ")
        if nombre == "":
            break

        llegada = int(input("Hora de llegada en minutos (ej 9:30 = 570): "))

        print("Clasificación: 1) Prioritario  2) Preferencial  3) Común")
        c = input("Seleccione opción: ")

        if c == "1":
            tipo = "Prioritario"
        elif c == "2":
            tipo = "Preferencial"
        else:
            tipo = "Común"

        duracion = int(input("Duración de atención (min): "))

        clientes.append({
            "turno": turno_manual,
            "nombre": nombre,
            "llegada": llegada,
            "tipo": tipo,
            "duracion": duracion
        })

        turno_manual += 1

# ====== GENERACIÓN AUTOMÁTICA ======
num_clientes = random.randint(40, 60)

for i in range(turno_manual, num_clientes + turno_manual):
    llegada = random.randint(HORA_INICIO, HORA_CIERRE)

    r = random.random()
    if r < 0.15:
        tipo = "Prioritario"
    elif r < 0.40:
        tipo = "Preferencial"
    else:
        tipo = "Común"

    duracion = random.randint(2, 12)

    clientes.append({
        "turno": i,
        "nombre": f"Cliente {i}",
        "llegada": llegada,
        "tipo": tipo,
        "duracion": duracion
    })

clientes.sort(key=lambda x: x["llegada"])

# Colas
cola_p = deque()
cola_pr = deque()
cola_c = deque()

tiempo = HORA_INICIO
indice = 0
cajero_libre = True
tiempo_restante = 0

# Estadísticas
esperas = {"Prioritario": [], "Preferencial": [], "Común": []}
atendidos = {"Prioritario": 0, "Preferencial": 0, "Común": 0}
max_espera = {"tiempo": -1, "turno": None, "tipo": None}
tiempo_ocioso = 0


def hora(minutos):
    return f"{minutos//60:02d}:{minutos%60:02d}"


# Simulación
while True:
    # Llegadas
    while indice < len(clientes) and clientes[indice]["llegada"] == tiempo:
        c = clientes[indice]
        if c["tipo"] == "Prioritario":
            cola_p.append(c)
        elif c["tipo"] == "Preferencial":
            cola_pr.append(c)
        else:
            cola_c.append(c)
        indice += 1

    # Avance atención
    if not cajero_libre:
        tiempo_restante -= 1
        if tiempo_restante == 0:
            cajero_libre = True

    # Tomar cliente
    if cajero_libre:
        if cola_p:
            actual = cola_p.popleft()
        elif cola_pr:
            actual = cola_pr.popleft()
        elif cola_c:
            actual = cola_c.popleft()
        else:
            actual = None

        if actual:
            espera = tiempo - actual["llegada"]
            tipo = actual["tipo"]

            esperas[tipo].append(espera)
            atendidos[tipo] += 1

            if espera > max_espera["tiempo"]:
                max_espera = {
                    "tiempo": espera,
                    "turno": actual["turno"],
                    "tipo": tipo
                }

            tiempo_restante = actual["duracion"]
            cajero_libre = False

            print(f"[{hora(tiempo)}] Atendiendo turno {actual['turno']} ({actual['tipo']}) — duración: {actual['duracion']} min")
        else:
            if tiempo <= HORA_CIERRE:
                tiempo_ocioso += 1

    # Fin
    if (tiempo > HORA_CIERRE and not cola_p and not cola_pr and not cola_c and cajero_libre):
        break

    tiempo += 1


# ====== INFORME FINAL ======
print("\n" + "="*50)
print("RESUMEN DEL DÍA")
print("="*50)

print(f"{'Tipo':<15}{'Atendidos':<12}{'Espera Prom (min)':<20}")
print("-"*50)

for tipo in ["Prioritario", "Preferencial", "Común"]:
    total = atendidos[tipo]
    promedio = sum(esperas[tipo]) / total if total > 0 else 0
    print(f"{tipo:<15}{total:<12}{promedio:<20.2f}")

print("-"*50)

print(f"\nCliente que más esperó:")
print(f"Turno {max_espera['turno']} ({max_espera['tipo']}) — {max_espera['tiempo']} min")

print(f"\nTiempo ocioso del cajero: {tiempo_ocioso} minutos")