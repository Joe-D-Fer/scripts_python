# Cajero automático simple

saldo = 100000
historial = []

def mostrar_menu():
    print("\n" + "*" * 30)
    print("      CAJERO AUTOMÁTICO")
    print("*" * 30)
    print("1. Consultar saldo")
    print("2. Depositar dinero")
    print("3. Retirar dinero")
    print("4. Salir")
    print("*" * 30)

while True:
    mostrar_menu()
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        print(f"Saldo actual: ${saldo}")
        historial.append(f"Consulta de saldo: ${saldo}")
    
    elif opcion == "2":
        try:
            monto = int(input("Ingrese monto a depositar: $"))
            if monto > 0:
                saldo += monto
                print(f"Depósito exitoso. Nuevo saldo: ${saldo}")
                historial.append(f"Depósito: +${monto}")
            else:
                print("El monto debe ser positivo.")
        except ValueError:
            print("Ingrese un número válido.")
    
    elif opcion == "3":
        try:
            monto = int(input("Ingrese monto a retirar: $"))
            if monto <= 0:
                print("El monto debe ser positivo.")
            elif monto > saldo:
                print("Fondos insuficientes.")
            else:
                saldo -= monto
                print(f"Retiro exitoso. Nuevo saldo: ${saldo}")
                historial.append(f"Retiro: -${monto}")
        except ValueError:
            print("Ingrese un número válido.")
    
    elif opcion == "4":
        print("\nHistorial de transacciones:")
        if len(historial) == 0:
            print("No se realizaron transacciones.")
        else:
            for i, transaccion in enumerate(historial, 1):
                print(f"{i}. {transaccion}")
        
        print("Gracias por usar el cajero automático.")
        break
    
    else:
        print("Opción no válida. Intente nuevamente.")