import tkinter as tk
from capa_logica.juego import Juego
from capa_logica.juego import calcular_valor

class Interfaz:
    def __init__(self):
        self.juego = Juego()
        self.ventana = tk.Tk()
        self.ventana.title("Blackjack")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg="#1d1f21")

        tk.Label(self.ventana, text="🎴 Blackjack", font=("Arial", 20, "bold"), fg="white", bg="#1d1f21").pack(pady=10)

        self.lbl_estado = tk.Label(self.ventana, text="", font=("Arial", 12), fg="lightgreen", bg="#1d1f21")
        self.lbl_estado.pack(pady=5)

        frame_apuesta = tk.Frame(self.ventana, bg="#1d1f21")
        frame_apuesta.pack(pady=5)
        tk.Label(frame_apuesta, text="Apuesta:", font=("Arial", 12), fg="white", bg="#1d1f21").pack(side="left", padx=5)
        self.entry_apuesta = tk.Entry(frame_apuesta, width=10)
        self.entry_apuesta.pack(side="left")

        self.btn_repartir = tk.Button(self.ventana, text="Repartir", command=self.repartir, width=15, bg="#3e8e41", fg="white")
        self.btn_repartir.pack(pady=5)

        self.btn_pedir = tk.Button(self.ventana, text="Pedir Carta", command=self.pedir, state="disabled", width=15, bg="#007bff", fg="white")
        self.btn_pedir.pack(pady=5)

        self.btn_plantarse = tk.Button(self.ventana, text="Plantarse", command=self.plantarse, state="disabled", width=15, bg="#dc3545", fg="white")
        self.btn_plantarse.pack(pady=5)

        self.lbl_mano_jugador = tk.Label(self.ventana, text="Tu mano:", font=("Arial", 12), fg="white", bg="#1d1f21")
        self.lbl_mano_jugador.pack(pady=10)

        self.lbl_puntos_jugador = tk.Label(self.ventana, text="", font=("Arial", 12), fg="lightblue", bg="#1d1f21")
        self.lbl_puntos_jugador.pack(pady=2)

        self.lbl_mano_crupier = tk.Label(self.ventana, text="Crupier:", font=("Arial", 12), fg="white", bg="#1d1f21")
        self.lbl_mano_crupier.pack(pady=10)

    def repartir(self):
        try:
            apuesta = float(self.entry_apuesta.get())
        except ValueError:
            self.lbl_estado.config(text="Ingrese una apuesta válida.")
            return

        self.juego.nueva_ronda(apuesta)
        self.actualizar_manos()
        self.lbl_estado.config(text="Turno del jugador")
        self.btn_pedir.config(state="normal")
        self.btn_plantarse.config(state="normal")

    def pedir(self):
        self.juego.jugador_pide()
        self.actualizar_manos()
        if self.juego.jugador_se_paso():
            self.lbl_estado.config(text="Te pasaste. Perdiste.")
            self.juego.finalizar_partida("Perdiste")
            self.fin_turno()

    def plantarse(self):
        self.juego.turno_crupier()
        resultado = self.juego.resultado()
        self.actualizar_manos()
        self.lbl_estado.config(text=resultado)
        self.juego.finalizar_partida(resultado)
        self.fin_turno()

    def fin_turno(self):
        self.btn_pedir.config(state="disabled")
        self.btn_plantarse.config(state="disabled")

    def actualizar_manos(self):
        jugador_mano = self.juego.jugador.mostrar_mano()
        puntos = calcular_valor(self.juego.jugador.mano)
        self.lbl_mano_jugador.config(text=f"Tu mano: {', '.join(jugador_mano)}")
        self.lbl_puntos_jugador.config(text=f"Puntos: {puntos}")

        crupier_mano = self.juego.crupier.mostrar_mano()
        self.lbl_mano_crupier.config(text=f"Crupier: {', '.join(crupier_mano)}")

    def ejecutar(self):
        self.ventana.mainloop()
