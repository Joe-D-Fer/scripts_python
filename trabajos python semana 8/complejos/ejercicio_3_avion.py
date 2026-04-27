class Seat:
    # Estados posibles del asiento
    LIBRE = 'L'
    RESERVADO = 'R'
    OCUPADO = 'O'

    def __init__(self):
        self.estado = Seat.LIBRE  # estado inicial
        self.nombre = None        # pasajero asignado

    def reservar(self, nombre):
        if self.estado == Seat.LIBRE:
            self.estado = Seat.RESERVADO
            self.nombre = nombre
            return True
        return False

    def ocupar(self):
        if self.estado == Seat.RESERVADO:
            self.estado = Seat.OCUPADO
            return True
        return False

    def liberar(self):
        self.estado = Seat.LIBRE
        self.nombre = None  # se limpia el pasajero

    def __str__(self):
        return self.estado


class SeatingSystem:
    def __init__(self, filas=10, columnas=6):
        self.filas = filas
        self.columnas = columnas
        # matriz de asientos
        self.asientos = [
            [Seat() for _ in range(columnas)]
            for _ in range(filas)
        ]

    def reservar(self):
        try:
            nombre = input("Ingrese nombre: ")

            print("\nPreferencia de asiento:")
            print("1. Ventana")
            print("2. Pasillo")
            print("3. Medio")
            print("4. Cualquiera")

            opcion = int(input("Seleccione una opción: "))

            if opcion not in [1, 2, 3, 4]:
                print("Opción inválida")
                return

            # columnas según preferencia
            if opcion == 1:
                columnas_pref = [0, 5]  # ventana
            elif opcion == 2:
                columnas_pref = [2, 3]  # pasillo
            elif opcion == 3:
                columnas_pref = [1, 4]  # medio
            else:
                columnas_pref = list(range(self.columnas))  # cualquiera

            # búsqueda del primer asiento libre
            for i in range(self.filas):
                for j in columnas_pref:
                    if self.asientos[i][j].estado == Seat.LIBRE:
                        self.asientos[i][j].reservar(nombre)
                        print(f"Reserva realizada en Fila {i+1}, Columna {j+1}")
                        return

            print("No hay asientos disponibles con esa preferencia")

        except ValueError:
            print("Entrada inválida")

    def ocupar(self):
        try:
            pendientes = []

            print("\n=== RESERVAS PENDIENTES ===")

            # listar reservas pendientes
            contador = 1
            for i in range(self.filas):
                for j in range(self.columnas):
                    asiento = self.asientos[i][j]

                    if asiento.estado == Seat.RESERVADO:
                        print(f"{contador}. {asiento.nombre} - Fila {i+1}, Columna {j+1}")
                        pendientes.append((i, j))
                        contador += 1

            if not pendientes:
                print("No hay reservas pendientes")
                return

            opcion = int(input("Seleccione una reserva para confirmar: "))

            if not (1 <= opcion <= len(pendientes)):
                print("Opción inválida")
                return

            fila, columna = pendientes[opcion - 1]

            # confirmar reserva
            if self.asientos[fila][columna].ocupar():
                print(f"Asiento confirmado para {self.asientos[fila][columna].nombre}")
            else:
                print("Error al confirmar el asiento")

        except ValueError:
            print("Entrada inválida. Debe ingresar un número.")

    def liberar(self):
        try:
            opciones = []

            print("\n=== CANCELAR / LIBERAR ASIENTO ===")

            contador = 1
            for i in range(self.filas):
                for j in range(self.columnas):
                    asiento = self.asientos[i][j]

                    # solo reservados u ocupados
                    if asiento.estado in (Seat.RESERVADO, Seat.OCUPADO):
                        estado_txt = "Reservado" if asiento.estado == Seat.RESERVADO else "Ocupado"
                        print(f"{contador}. {asiento.nombre} - Fila {i+1}, Columna {j+1} ({estado_txt})")
                        opciones.append((i, j))
                        contador += 1

            if not opciones:
                print("No hay asientos ocupados o reservados")
                return

            opcion = int(input("Seleccione una opción para liberar: "))

            if not (1 <= opcion <= len(opciones)):
                print("Opción inválida")
                return

            fila, columna = opciones[opcion - 1]

            nombre = self.asientos[fila][columna].nombre
            self.asientos[fila][columna].liberar()

            print(f"Asiento liberado para {nombre}")

        except ValueError:
            print("Entrada inválida. Debe ingresar un número.")

    def mostrar(self):
        print("\n=== MAPA DE ASIENTOS ===\n")

        # encabezado con letras de columnas (A, B, C...)
        mid = self.columnas // 2

        izquierda = " ".join(f"{chr(65 + j):^2}" for j in range(mid))
        derecha = " ".join(f"{chr(65 + j):^2}" for j in range(mid, self.columnas))

        print("           " + izquierda + "  ||   " + derecha)
        print("        " + "-" * (self.columnas * 5))

        for i, fila in enumerate(self.asientos):
            izquierda = "  ".join(str(a) for a in fila[:self.columnas // 2])
            derecha = "  ".join(str(a) for a in fila[self.columnas // 2:])

            # espacio central simula el pasillo del avión
            print(f"Fila {i+1:<2} |  {izquierda}   ||   {derecha}  |")

    def listar_pasajeros(self):
        print("\n=== LISTADO DE PASAJEROS ===")

        hay_datos = False

        for i in range(self.filas):
            for j in range(self.columnas):
                asiento = self.asientos[i][j]

                # mostrar solo ocupados o reservados
                if asiento.estado in (Seat.RESERVADO, Seat.OCUPADO):
                    estado_txt = "Reservado" if asiento.estado == Seat.RESERVADO else "Ocupado"
                    print(f"Nombre: {asiento.nombre} | Fila: {i+1} | Columna: {j+1} | Estado: {estado_txt}")
                    hay_datos = True

        if not hay_datos:
            print("No hay pasajeros registrados")
    
    def estadisticas(self):
        total_asientos = self.filas * self.columnas

        ocupados = 0
        reservas_pendientes = 0

        # agrupación por tipo de asiento
        tipos = {
            "ventana": {"cols": [0, 5], "ocupados": 0, "total": 0},
            "medio": {"cols": [1, 4], "ocupados": 0, "total": 0},
            "pasillo": {"cols": [2, 3], "ocupados": 0, "total": 0},
        }

        for i in range(self.filas):
            for j in range(self.columnas):
                asiento = self.asientos[i][j]

                if asiento.estado == Seat.OCUPADO:
                    ocupados += 1
                elif asiento.estado == Seat.RESERVADO:
                    reservas_pendientes += 1

                # clasificar por tipo de asiento
                for tipo, data in tipos.items():
                    if j in data["cols"]:
                        data["total"] += 1
                        if asiento.estado == Seat.OCUPADO:
                            data["ocupados"] += 1

        porcentaje_total = (ocupados / total_asientos) * 100

        print("\n=== ESTADÍSTICAS ===")
        print(f"Ocupación total: {porcentaje_total:.2f}%")
        print(f"Reservas pendientes: {reservas_pendientes}")

        print("\nOcupación por tipo:")
        for tipo, data in tipos.items():
            if data["total"] > 0:
                porcentaje = (data["ocupados"] / data["total"]) * 100
                print(f"{tipo.capitalize()}: {porcentaje:.2f}%")

    def reservar_grupo(self):
        try:
            cantidad = int(input("Cantidad de asientos a reservar: "))

            if cantidad <= 0 or cantidad > self.columnas:
                print("Cantidad inválida")
                return

            # nombres del grupo
            nombres = []
            for i in range(cantidad):
                nombre = input(f"Ingrese nombre del pasajero {i+1}: ")
                nombres.append(nombre)

            # buscar asientos consecutivos
            for i in range(self.filas):
                consecutivos = 0
                inicio = 0

                for j in range(self.columnas):
                    if self.asientos[i][j].estado == Seat.LIBRE:
                        if consecutivos == 0:
                            inicio = j

                        consecutivos += 1

                        if consecutivos == cantidad:
                            # asignación en bloque
                            for k in range(cantidad):
                                self.asientos[i][inicio + k].reservar(nombres[k])

                            print(f"Grupo reservado en Fila {i+1}, Columnas {inicio+1} a {inicio+cantidad}")
                            return
                    else:
                        consecutivos = 0

            print("No hay suficientes asientos consecutivos disponibles")

        except ValueError:
            print("Entrada inválida")


def menu_principal(sistema):
    while True:
        print("\n=== SISTEMA DE RESERVAS ===")
        print("1. Reservar asiento")
        print("2. Confirmar reserva (ocupar)")
        print("3. Cancelar reserva (liberar)")
        print("4. Mostrar asientos")
        print("5. Reservar grupo")
        print("6. Listar pasajeros")
        print("7. Ver estadísticas")
        print("8. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
            print("\n")

            if opcion == 1:
                sistema.reservar()
            elif opcion == 2:
                sistema.ocupar()
            elif opcion == 3:
                sistema.liberar()
            elif opcion == 4:
                sistema.mostrar()
            elif opcion == 5:
                sistema.reservar_grupo()
            elif opcion == 6:
                sistema.listar_pasajeros()
            elif opcion == 7:
                sistema.estadisticas()
            elif opcion == 8:
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida")

        except ValueError:
            print("Entrada inválida. Ingrese un número.")


def main():
    sistema = SeatingSystem()
    menu_principal(sistema)


if __name__ == "__main__":
    main()