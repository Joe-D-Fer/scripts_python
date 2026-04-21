import csv
import os

# ---------- Clase Cliente ----------
class Cliente:
    def __init__(self, rut, nombre, cuenta, clave, saldo):
        self.rut = rut
        self.nombre = nombre
        self.cuenta = cuenta
        self.clave = clave
        self.saldo = saldo

    @staticmethod
    def generar_numero_cuenta(clientes):
        if not clientes:
            return 1000
        return max(c.cuenta for c in clientes) + 10

    @staticmethod
    def generar_clave(nombre, saldo):
        return int((saldo / len(nombre)) * 150)

    def depositar(self, monto):
        self.saldo += monto

    def girar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto
            return True
        return False

    def cambiar_clave(self, clave_actual, nueva_clave):
        if clave_actual == self.clave:
            self.clave = nueva_clave
            return True
        return False

# ---------- Funciones de gestión ----------
def cargar_clientes(archivo):
    clientes = []
    if os.path.exists(archivo):
        with open(archivo, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rut, nombre, cuenta, clave, saldo = row
                clientes.append(Cliente(rut, nombre, int(cuenta), int(clave), float(saldo)))
    return clientes

def guardar_clientes(archivo, clientes):
    with open(archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for c in clientes:
            writer.writerow([c.rut, c.nombre, c.cuenta, c.clave, c.saldo])

def buscar_cliente_por_rut(clientes, rut):
    for c in clientes:
        if c.rut == rut:
            return c
    return None

# ---------- Funciones del menú ----------
def crear_cliente(clientes):
    rut = input("Ingrese RUT: ")
    nombre = input("Ingrese nombre: ")
    saldo = float(input("Ingrese monto inicial: "))
    cuenta = Cliente.generar_numero_cuenta(clientes)
    clave = Cliente.generar_clave(nombre, saldo)
    nuevo_cliente = Cliente(rut, nombre, cuenta, clave, saldo)
    clientes.append(nuevo_cliente)
    print(f"Cliente creado. Número de cuenta: {cuenta}, Clave secreta: {clave}")

def actualizar_cliente(clientes):
    while True:
        print("\n--- Actualización de clientes ---")
        print("1. Cambio de clave")
        print("2. Depósito")
        print("3. Giro")
        print("4. Cancelación de cuenta")
        print("5. Fin de actualizaciones")
        opcion = input("Seleccione opción: ")

        if opcion == '1':
            rut = input("Ingrese RUT: ")
            cliente = buscar_cliente_por_rut(clientes, rut)
            if cliente:
                clave_actual = int(input("Ingrese clave actual: "))
                nueva_clave = int(input("Ingrese nueva clave: "))
                if cliente.cambiar_clave(clave_actual, nueva_clave):
                    print("Clave actualizada correctamente.")
                else:
                    print("Clave incorrecta. No se puede actualizar.")
            else:
                print("Cliente no encontrado.")

        elif opcion == '2':
            rut = input("Ingrese RUT: ")
            cliente = buscar_cliente_por_rut(clientes, rut)
            if cliente:
                deposito = float(input("Ingrese monto a depositar: "))
                cliente.depositar(deposito)
                print("Depósito realizado correctamente.")
            else:
                print("Cliente no encontrado.")

        elif opcion == '3':
            rut = input("Ingrese RUT: ")
            cliente = buscar_cliente_por_rut(clientes, rut)
            if cliente:
                giro = float(input("Ingrese monto a girar: "))
                if cliente.girar(giro):
                    print("Giro realizado correctamente.")
                else:
                    print("Fondos insuficientes.")
            else:
                print("Cliente no encontrado.")

        elif opcion == '4':
            rut = input("Ingrese RUT: ")
            cliente = buscar_cliente_por_rut(clientes, rut)
            if cliente:
                clientes.remove(cliente)
                print("Cuenta cancelada.")
            else:
                print("Cliente no encontrado.")

        elif opcion == '5':
            break
        else:
            print("Opción inválida.")

def consultas(clientes):
    while True:
        print("\n--- Consultas ---")
        print("1. Buscar cliente por RUT")
        print("2. Listado de todos los clientes")
        print("3. Cliente con menor saldo")
        print("4. Cliente con mayor saldo")
        print("5. Cantidad de clientes")
        print("6. Fin de consultas")
        opcion = input("Seleccione opción: ")

        if opcion == '1':
            rut = input("Ingrese RUT: ")
            cliente = buscar_cliente_por_rut(clientes, rut)
            if cliente:
                print(f"Nombre: {cliente.nombre}, Cuenta: {cliente.cuenta}, Saldo: {cliente.saldo}")
            else:
                print("Cliente no encontrado.")

        elif opcion == '2':
            for c in sorted(clientes, key=lambda x: x.rut):
                print(f"RUT: {c.rut}, Nombre: {c.nombre}, Saldo: {c.saldo}")

        elif opcion == '3':
            if clientes:
                c = min(clientes, key=lambda x: x.saldo)
                print(f"Cliente con menor saldo: {c.nombre}, Saldo: {c.saldo}")
            else:
                print("No hay clientes.")

        elif opcion == '4':
            if clientes:
                c = max(clientes, key=lambda x: x.saldo)
                print(f"Cliente con mayor saldo: {c.nombre}, Saldo: {c.saldo}")
            else:
                print("No hay clientes.")

        elif opcion == '5':
            print(f"Cantidad de clientes: {len(clientes)}")

        elif opcion == '6':
            break

        else:
            print("Opción inválida.")

# ---------- Programa principal ----------
def main():
    archivo = "clientes.csv"
    clientes = cargar_clientes(archivo)

    while True:
        print("\n--- Menú Principal ---")
        print("1. Crear clientes nuevos")
        print("2. Actualizar clientes antiguos")
        print("3. Realizar consultas")
        print("4. Salir")
        opcion = input("Seleccione opción: ")

        if opcion == '1':
            crear_cliente(clientes)
        elif opcion == '2':
            actualizar_cliente(clientes)
        elif opcion == '3':
            consultas(clientes)
        elif opcion == '4':
            guardar_clientes(archivo, clientes)
            print("Información guardada. Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()