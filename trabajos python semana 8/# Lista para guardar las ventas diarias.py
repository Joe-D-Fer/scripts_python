# Lista para guardar las ventas diarias
ventas = []

# Ingreso de datos
for dia in range(1, 31):
    while True:
        try:
            monto = float(input(f"Ingrese la venta del día {dia}: "))
            if monto < 0:
                print("El monto no puede ser negativo.")
            else:
                ventas.append(monto)
                break
        except ValueError:
            print("Ingrese un número válido.")

# Cálculos
total_ventas = sum(ventas)
promedio = total_ventas / len(ventas)

mayor_venta = max(ventas)
menor_venta = min(ventas)

dia_mayor = ventas.index(mayor_venta) + 1
dia_menor = ventas.index(menor_venta) + 1

# Contar días sobre el promedio
dias_sobre_promedio = 0
for venta in ventas:
    if venta > promedio:
        dias_sobre_promedio += 1

# Resultados
print("\n--- RESULTADOS ---")
print(f"Total de ventas del mes: ${total_ventas:.2f}")
print(f"Promedio diario: ${promedio:.2f}")
print(f"Día con mayor venta: Día {dia_mayor} (${mayor_venta:.2f})")
print(f"Día con menor venta: Día {dia_menor} (${menor_venta:.2f})")
print(f"Días que superaron el promedio: {dias_sobre_promedio}")