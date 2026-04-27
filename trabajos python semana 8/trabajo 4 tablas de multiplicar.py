# genero variable del numero que ingresare
numero = ""
#genero un bucle 
while numero.lower() != "salir": 
    numero = input("Ingrese un número a multiplicar  (o 'salir' para terminar): ") #ingreso numero a multiplicar o salir para terminar

    if numero.lower() != "salir": #lower para que si se escribe en mayuscula lo tome como minuscula
        if not numero.isdigit():
            print("Error: debe ingresar un número entero positivo.")
        else:
            numero_int = int(numero)
            print(f"\nTabla del {numero_int}:")
            for i in range(1, 11):
                print(f"{numero_int} x {i} = {numero_int * i}") #genero tabla de multiplicar
            print("----------------------")

print("Programa finalizado")