import re # librería para expresiones regulares

def validar_contrasena(contrasena):
    errores = []

    if len(contrasena) < 8:
        errores.append("Debe tener al menos 8 caracteres")

    if not any(c.isupper() for c in contrasena):
        errores.append("Debe contener al menos una letra mayúscula")

    if not any(c.islower() for c in contrasena):
        errores.append("Debe contener al menos una letra minúscula")

    if not any(c.isdigit() for c in contrasena):
        errores.append("Debe contener al menos un número")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        errores.append("Debe contener al menos un carácter especial")

    if errores:
        # lanzamos un error con todos los mensajes
        raise ValueError("\n".join(errores))

    return True


def main():
    while True:
        try:
            contrasena = input("Ingrese la contraseña segura: ")
            validar_contrasena(contrasena)
            print("Su contraseña es segura")
            break

        except ValueError as e:
            print("Errores encontrados:")
            print(e)
            print("Intente nuevamente\n")


if __name__ == "__main__":
    main()