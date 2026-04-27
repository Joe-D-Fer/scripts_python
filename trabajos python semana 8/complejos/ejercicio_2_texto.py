lineas = []
print("escriba el texto:")
while True:
    linea = input()
    if linea == "": # linea vacia termina el input
        break
    lineas.append(linea)

texto = "\n".join(lineas)

print("texto ingresado:")
print(texto)