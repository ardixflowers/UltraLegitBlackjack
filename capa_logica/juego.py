from .mazo import Mazo
from .jugador import Jugador
from .crupier import Crupier
from capa_datos.db import guardar_partida
from datetime import datetime

def calcular_valor(mano):
    valor = 0
    ases = 0
    for carta in mano:
        if carta.valor in ['J', 'Q', 'K']:
            valor += 10
        elif carta.valor == 'A':
            valor += 11
            ases += 1
        else:
            valor += int(carta.valor)
    while valor > 21 and ases:
        valor -= 10
        ases -= 1
    return valor

class Juego:
    def __init__(self):
        self.mazo = Mazo()
        self.jugador = Jugador("Jugador")
        self.crupier = Crupier()
        self.apuesta = 0

    def nueva_ronda(self, apuesta):
        self.apuesta = apuesta
        self.mazo = Mazo()
        self.jugador.mano = []
        self.crupier.mano = []

        self.jugador.recibir_carta(self.mazo.sacar_carta())
        self.jugador.recibir_carta(self.mazo.sacar_carta())
        self.crupier.recibir_carta(self.mazo.sacar_carta())

    def jugador_pide(self):
        self.jugador.recibir_carta(self.mazo.sacar_carta())

    def jugador_se_paso(self):
        return calcular_valor(self.jugador.mano) > 21

    def turno_crupier(self):
        while calcular_valor(self.crupier.mano) < 17:
            self.crupier.recibir_carta(self.mazo.sacar_carta())

    def resultado(self):
        val_jugador = calcular_valor(self.jugador.mano)
        val_crupier = calcular_valor(self.crupier.mano)

        if val_jugador > 21:
            return "Perdiste"
        elif val_crupier > 21:
            return "Ganaste"
        elif val_jugador > val_crupier:
            return "Ganaste"
        elif val_jugador < val_crupier:
            return "Perdiste"
        else:
            return "Empate"

    def finalizar_partida(self, resultado):
        ganancia = 0
        if resultado == "Ganaste":
            ganancia = self.apuesta
        elif resultado == "Perdiste":
            ganancia = -self.apuesta
        guardar_partida(self.jugador.nombre, resultado, self.apuesta, ganancia, datetime.now())
