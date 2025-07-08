import random
from .carta import Carta

class Mazo:
    def __init__(self):
        self.cartas = []
        self.generar_mazo()

    def generar_mazo(self):
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
        self.cartas = [Carta(valor, palo) for valor in valores for palo in palos]
        random.shuffle(self.cartas)

    def sacar_carta(self):
        return self.cartas.pop() if self.cartas else None
