class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def recibir_carta(self, carta):
        self.mano.append(carta)

    def mostrar_mano(self):
        return [str(carta) for carta in self.mano]
