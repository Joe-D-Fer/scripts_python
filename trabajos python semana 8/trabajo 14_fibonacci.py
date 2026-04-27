import math

def main():
    num = int(input("ingrese la cantidad de términos: "))
    while num < 2:
        print("número debe ser mayor a 2!")
        num = int(input("ingrese la cantidad de términos: "))

    fibo = [1, 2]
    for i in range(1, num-1):
        fibo.append(fibo[i]+fibo[i-1])

    print("secuencia completa:")
    print("[ " + ", ".join(str(i) for i in fibo) + " ]")
    
    
    count=0
    pares=0
    impares=0
    primos=0

    for i in fibo:
        count += i
        if i%2 == 0:
            pares += 1
        else:
            impares += 1
        if i < 2:
            continue
        primo = True
        for j in range(2, int(math.sqrt(i))):
            if i%j == 0:
                primo = False
                break
        if primo: primos += 1

    print("suma de todos los términos: ", count)
    print("cantidad de pares: ", pares)
    print("cantidad de impares: ", impares)
    print("cantidad de primos: ", primos)

if __name__ == "__main__":
    while True:
        main()
        if input("continuar? s/n: ").lower() == "n": break