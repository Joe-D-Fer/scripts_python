def decimal_a_binario(numero):
    pasos = []
    
    while numero > 0:
        cociente = numero // 2
        residuo = numero % 2
        pasos.append((numero, cociente, residuo))
        numero = cociente
    
    return pasos


def mostrar_proceso(pasos):
    print("\nProceso de conversión:")
    print("Número | Cociente | Residuo")
    print("----------------------------")
    
    for paso in pasos:
        print(f"{paso[0]:>6} | {paso[1]:>8} | {paso[2]:>7}")
    
    # El binario se forma leyendo los residuos al revés
    binario = ''.join(str(p[2]) for p in reversed(pasos))
    
    print("\nResultado en binario:", binario)


# Programa principal
try:
    numero = int(input("Ingrese un número entero positivo: "))
    
    if numero <= 0:
        print("Debe ingresar un número positivo mayor que 0.")
    else:
        pasos = decimal_a_binario(numero)
        mostrar_proceso(pasos)

except ValueError:
    print("Entrada inválida. Debe ingresar un número entero.")