texto = "" #se crea una Variable

while texto.lower() != "salir":
    texto = input("Ingrese una palabra o frase (o 'salir' para terminar): ")

    #Gernero condicion de salida
    if texto.lower() != "salir":
        texto = texto.lower()

        a = e = i = o = u = 0  # contadores en 0

        #Sumar contador de letras
        for letra in texto:
            if letra == 'a':
                a += 1
            elif letra == 'e':
                e += 1
            elif letra == 'i':
                i += 1
            elif letra == 'o':
                o += 1
            elif letra == 'u':
                u += 1

        total = a + e + i + o + u # sumar cantidad de vocales

        #mostrar en pantalla total de vocales
        print("Total de vocales:", total)
        print("a:", a)
        print("e:", e)
        print("i:", i)
        print("o:", o)
        print("u:", u)

print("Programa terminado")