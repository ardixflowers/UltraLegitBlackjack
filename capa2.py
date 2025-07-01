import random

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre                  # Nombre del jugador
        self.mano = []                        # Lista de cartas (carta, palo) en mano
        self.puntaje = 0                      # Puntaje actual
        self.credito = 1000                   # Dinero disponible (apuesta)
        self.apuesta_actual = 0               # Apuesta en curso
        self.en_juego = True                  # Indica si sigue en la ronda

    def pedir_carta(self):
        print(f"Cartas en mesa: {len(self.mano)}")
        mazo = Baraja.barajar()
        carta = mazo[0]
        self.mano.add(carta)
        print(f"Te tocó: {carta}")
        print(f"Valor actual de la mano: {self.valor_mano()}")

    def valor_mano(self):
        for carta in self.mano:
            valor += Baraja.valor_carta(carta)
        return valor
    

    


class Dealer(Jugador):
    def __init__(self):
        super().__init__("Dealer")
        self.visible = []


class Baraja:
    def __init__(self):
        self.cartas = self.crear_baraja()    # Lista de cartas
        self.baraja = self.barajar()
    def crear_baraja(self):
        palos = ['♠', '♥', '♦', '♣']
        cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', 'J', 'Q', 'K']
        return [(valor, palo) for palo in palos for valor in valores]
    def barajar():
        baraja = [(cartas, palos) for palo in palos for carta in cartas]
        mazo = random.shuffle(baraja)
        return mazo
    def valor_carta(carta):
        if carta[0] in ['J', 'Q','K']:
            return 10
        elif carta[0] == 'A':
            return 11
        else:
            return int(carta[0])



class Partida:
    def __init__(self, jugadores):
        self.jugadores = jugadores            # Lista de Jugador
        self.dealer = Dealer()                # Instancia de Dealer
        self.baraja = Baraja()                # Mazo de cartas
        self.en_curso = True                  # Estado de la partida
        self.resultados = {}                  # Resultados al finalizar