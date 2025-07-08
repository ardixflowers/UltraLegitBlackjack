from .jugador import Jugador

class Crupier(Jugador):
    def __init__(self):
        super().__init__("Crupier")

    def debe_pedir(self):
        return True
