usuarios = []

class usuario:
    def __init__(self, id, nombre):
        self.id = id,
        self.nombre = nombre
class libro:
    def __init__(self, cod, titulo, autor, publicacion, stock_disponible):
        self.cod = cod,
        self.titulo = titulo,
        self.autor = autor,
        self.publicacion = publicacion,
        self.stock_disponible = stock_disponible

    def prestar(self, usuario_id):
        self.stock_disponible -= 1


def main():
    return

if __name__ == "__main__":
    main()