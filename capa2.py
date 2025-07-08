import random, threading, multiprocessing, time


class Baraja:
    def __init__(self):
        self.cartas = self.crear_baraja()
        self.baraja = self.barajar()
        self.lock = threading.Lock()

    def crear_baraja(self):
        palos = ['♠', '♥', '♦', '♣']
        cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return [(carta, palo) for palo in palos for carta in cartas]

    def barajar(self):
        baraja = self.crear_baraja()
        random.shuffle(baraja)
        return baraja

    def sacar_carta(self):
        with self.lock:
            if self.baraja:
                return self.baraja.pop()
            return None

    @staticmethod
    def valor_carta(carta):
        if carta[0] in ['J', 'Q', 'K']:
            return 10
        elif carta[0] == 'A':
            return 11
        else:
            return int(carta[0])


class JugadorSimulado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.puntaje = 0
        self.en_juego = True

    def recibir_carta(self, carta):
        if carta:
            self.mano.append(carta)
            self.puntaje += Baraja.valor_carta(carta)

    def jugar_turno(self, baraja):
        print(f"[{self.nombre}] comienza su turno.")
        while self.puntaje < 17:
            carta = baraja.sacar_carta()
            self.recibir_carta(carta)
            print(f"[{self.nombre}] recibe {carta}, puntaje: {self.puntaje}")
            time.sleep(random.uniform(0.5, 1.0))
        print(f"[{self.nombre}] se planta con {self.puntaje}")


class JugadorHumano(JugadorSimulado):
    def __init__(self, nombre):
        super().__init__(nombre)

    def mostrar_mano(self):
        print(f"\nTu mano: {self.mano} (Puntaje: {self.puntaje})")

    def elegir_accion(self):
        acciones = ['1', '2', '3']
        print("\nElige una acción:")
        print("1. Pedir carta")
        print("2. Plantarse")
        print("3. Doblar apuesta (no implementado aún)")

        eleccion = input("Opción: ")
        while eleccion not in acciones:
            eleccion = input("Opción inválida. Intenta de nuevo: ")
        return eleccion

    def jugar_turno(self, baraja):
        print(f"\n== TURNO DE {self.nombre.upper()} ==")
        while self.puntaje < 21:
            self.mostrar_mano()
            accion = self.elegir_accion()

            if accion == '1':  # Pedir carta
                carta = baraja.sacar_carta()
                self.recibir_carta(carta)
                print(f"Recibiste: {carta}")
            elif accion == '2':  # Plantarse
                print(f"{self.nombre} se planta con {self.puntaje}.")
                break
            elif accion == '3':  # Doblar apuesta (placeholder)
                print("Funcionalidad de doblar aún no implementada.")
                break

        if self.puntaje > 21:
            self.mostrar_mano()
            print("¡Te pasaste de 21!")


class Dealer(JugadorSimulado):
    def __init__(self):
        super().__init__("Dealer")
        self.visible = []

    def revelar_carta(self, baraja):
        carta = baraja.sacar_carta()
        if carta:
            self.visible.append(carta)
            self.mano.append(self.visible.pop(0))


class Partida:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.jugador_humano = self.buscar_humano()
        self.dealer = Dealer()
        self.baraja = Baraja()
        self.resultados = {}

    def buscar_humano(self):
        for jugador in self.jugadores:
            if isinstance(jugador, JugadorHumano):
                return jugador
        return None

    def jugar_partida(self):
        print("\n== INICIA LA PARTIDA ==")

        # Repartir carta inicial
        for jugador in self.jugadores:
            jugador.recibir_carta(self.baraja.sacar_carta())

        # Turno del jugador humano (si existe)
        if self.jugador_humano:
            self.jugador_humano.recibir_carta(self.baraja.sacar_carta())
            self.jugador_humano.jugar_turno(self.baraja)

        # Turnos de los bots en hilos
        hilos = []
        for jugador in self.jugadores:
            if jugador != self.jugador_humano:
                jugador.recibir_carta(self.baraja.sacar_carta())
                hilo = threading.Thread(target=jugador.jugar_turno, args=(self.baraja,))
                hilos.append(hilo)
                hilo.start()

        for hilo in hilos:
            hilo.join()

        # Turno del dealer
        print("\n== TURNO DEL DEALER ==")
        self.dealer.jugar_turno(self.baraja)
        print(f"[Dealer] Puntaje final: {self.dealer.puntaje}")

        # Determinar resultados
        self.determinar_resultados()

        # Guardar resultados con procesos
        procesos = []
        for nombre, resultado in self.resultados.items():
            proceso = multiprocessing.Process(target=self.guardar_resultado, args=(nombre, resultado))
            procesos.append(proceso)
            proceso.start()

        for proceso in procesos:
            proceso.join()

    def determinar_resultados(self):
        for jugador in self.jugadores:
            if jugador.puntaje > 21:
                resultado = "Pierde"
            elif self.dealer.puntaje > 21 or jugador.puntaje > self.dealer.puntaje:
                resultado = "Gana"
            elif jugador.puntaje == self.dealer.puntaje:
                resultado = "Empate"
            else:
                resultado = "Pierde"

            self.resultados[jugador.nombre] = resultado
            print(f"[{jugador.nombre}] Resultado: {resultado}")

    @staticmethod
    def guardar_resultado(nombre, resultado):
        print(f"[Proceso] Guardando resultado de {nombre}: {resultado}")
        time.sleep(1)
        print(f"[Proceso] Resultado de {nombre} guardado.")


if __name__ == "__main__":
    humano = JugadorHumano("Sebastián")
    bots = [JugadorSimulado(f"Bot {i+1}") for i in range(3)]
    jugadores = [humano] + bots  # corregido: se agregan los bots correctamente

    partida = Partida(jugadores)
    partida.jugar_partida()
