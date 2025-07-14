import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from concurrente.hilos import reloj
from concurrente.procesos import iniciar_procesos
import time


from capa_logica.juego import Juego
from capa_logica.juego import calcular_valor
from capa_datos.db import agregar_usuario, obtener_usuario, actualizar_usuario


class Interfaz:
    def __init__(self):
        self.usuario_id = None
        self.usuario_nombre = None
        self.juego = Juego()
        self.saldo = 0

        # ----- Ventana ----------------------------------------------------
        self.ventana = tk.Tk()
        self.ventana.title("Blackjack")
        self.ventana.geometry("620x560")
        self.ventana.configure(bg="#1d1f21")
        self.ventana.attributes('-fullscreen', True)

        self.menu_usuario()

    def menu_usuario(self):
        self.menu_win = tk.Toplevel(self.ventana)
        self.menu_win.title("Crear o ingresar usuario")
        self.menu_win.geometry("350x250")
        self.menu_win.configure(bg="#23272e")
        self.menu_win.grab_set()
        tk.Label(
            self.menu_win,
            text="Bienvenido a Blackjack",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#23272e",
        ).pack(pady=10)
        tk.Label(
            self.menu_win,
            text="Nombre de usuario:",
            font=("Arial", 12),
            fg="white",
            bg="#23272e",
        ).pack(pady=5)
        self.entry_nombre = tk.Entry(self.menu_win, font=("Arial", 12))
        self.entry_nombre.pack(pady=5)
        tk.Label(
            self.menu_win,
            text="Contraseña:",
            font=("Arial", 12),
            fg="white",
            bg="#23272e",
        ).pack(pady=5)
        self.entry_contrasena = tk.Entry(self.menu_win, font=("Arial", 12), show="*")
        self.entry_contrasena.pack(pady=5)
        tk.Button(
            self.menu_win,
            text="Ingresar",
            font=("Arial", 12, "bold"),
            bg="#3e8e41",
            fg="white",
            command=self.ingresar_usuario,
        ).pack(pady=10)


    def ingresar_usuario(self):
        threading.Thread(target=self._login_usuario, daemon=True).start()

    def _login_usuario(self):
        nombre = self.entry_nombre.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        if not nombre or not contrasena:
            self.ventana.after(0, lambda: messagebox.showwarning("Datos requeridos", "Debe ingresar nombre de usuario y contraseña."))
            return

        from capa_datos.db import get_conn, agregar_usuario
        try:
            with get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(usuario)")
                columns = [col[1] for col in cursor.fetchall()]
                if not all(col in columns for col in ("nombre", "contrasena", "manos", "victorias", "derrotas", "saldo", "id_usuario")):
                    self.ventana.after(0, lambda: messagebox.showerror(
                        "Error de base de datos",
                        "La tabla 'usuario' no tiene las columnas requeridas.\n"
                        "Elimina el archivo blackjack.db y vuelve a crear la base de datos."
                    ))
                    self.ventana.after(0, self.ventana.destroy)
                    return

                cursor.execute("SELECT * FROM usuario WHERE nombre=?", (nombre,))
                usuario = cursor.fetchone()
                if usuario:
                    if usuario[2] == contrasena:
                        self.usuario_id = usuario[0]
                        self.usuario_nombre = usuario[1]
                        self.saldo = usuario[6]
                    else:
                        self.ventana.after(0, lambda: messagebox.showerror("Contraseña incorrecta", "La contraseña es incorrecta."))
                        return
                else:
                    self.usuario_id = nombre
                    self.usuario_nombre = nombre
                    self.saldo = 1000
                    agregar_usuario(nombre, nombre, contrasena, manos=0, victorias=0, derrotas=0, saldo=1000)
            # Abrir interfaz de juego desde el hilo principal
            self.ventana.after(0, lambda: [self.menu_win.destroy(), self.iniciar_interfaz_juego()])
        except Exception as e:
            self.ventana.after(0, lambda: messagebox.showerror("Error de base de datos", f"Ocurrió un error: {e}"))
            self.ventana.after(0, self.ventana.destroy)


    def iniciar_interfaz_juego(self):
        tk.Label(
            self.ventana,
            text=f"🎴 Blackjack - Usuario: {self.usuario_nombre}",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1d1f21",
        ).pack(pady=10)

        self.lbl_saldo = tk.Label(
            self.ventana,
            text=f"Saldo: ${self.saldo:.2f}",
            font=("Arial", 12),
            fg="gold",
            bg="#1d1f21",
        )
        self.lbl_saldo.pack()

        self.lbl_estado = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 12),
            fg="lightgreen",
            bg="#1d1f21",
        )
        self.lbl_estado.pack(pady=5)

        # ----------------------- Entrada apuesta -------------------------
        frame_apuesta = tk.Frame(self.ventana, bg="#1d1f21")
        frame_apuesta.pack(pady=5)
        tk.Label(
            frame_apuesta,
            text="Apuesta:",
            font=("Arial", 12),
            fg="white",
            bg="#1d1f21",
        ).pack(side="left", padx=5)
        self.entry_apuesta = tk.Entry(frame_apuesta, width=10)
        self.entry_apuesta.pack(side="left")

        # Etiqueta para mostrar la apuesta actual
        self.lbl_apuesta_actual = tk.Label(
            self.ventana,
            text="Apuesta actual: $0.00",
            font=("Arial", 12, "bold"),
            fg="#00ff99",
            bg="#1d1f21",
        )
        self.lbl_apuesta_actual.pack(pady=2)

        # ----------------------- Manos y puntos ---------------------------
        self.lbl_mano_jugador = tk.Label(
            self.ventana,
            text="Tu mano:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1d1f21",
        )
        self.lbl_mano_jugador.pack(pady=10)

        self.lbl_puntos_jugador = tk.Label(
            self.ventana,
            text="Tus puntos: 0",
            font=("Arial", 12, "bold"),
            fg="#00bfff",
            bg="#1d1f21",
        )
        self.lbl_puntos_jugador.pack(pady=2)

        self.lbl_mano_crupier = tk.Label(
            self.ventana,
            text="Crupier:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1d1f21",
        )
        self.lbl_mano_crupier.pack(pady=10)

        self.lbl_puntos_crupier = tk.Label(
            self.ventana,
            text="Puntos crupier: 0",
            font=("Arial", 12, "bold"),
            fg="#ffa500",
            bg="#1d1f21",
        )
        self.lbl_puntos_crupier.pack(pady=2)

        # ----------------------- Botonera inferior ------------------------
        self.frame_botones = tk.Frame(self.ventana, bg="#1d1f21")
        self.frame_botones.pack(side="bottom", pady=10)

        # Botones en horizontal y con padding
        self.btn_repartir = tk.Button(
            self.frame_botones,
            text="🃏 Repartir",
            command=self.repartir,
            width=13,
            font=("Arial", 11, "bold"),
            bg="#3e8e41",
            fg="white",
            activebackground="#2e7031",
            activeforeground="white",
            relief="raised",
            bd=3,
        )
        self.btn_repartir.grid(row=0, column=0, padx=6, pady=5)

        self.btn_pedir = tk.Button(
            self.frame_botones,
            text="➕ Pedir Carta",
            command=self.pedir,
            state="disabled",
            width=13,
            font=("Arial", 11, "bold"),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            relief="raised",
            bd=3,
        )
        self.btn_pedir.grid(row=0, column=1, padx=6, pady=5)

        self.btn_duplicar = tk.Button(
            self.frame_botones,
            text="✖️ Duplicar",
            command=self.duplicar_apuesta,
            state="disabled",
            width=13,
            font=("Arial", 11, "bold"),
            bg="#ffc107",
            fg="black",
            activebackground="#b28704",
            activeforeground="black",
            relief="raised",
            bd=3,
        )
        self.btn_duplicar.grid(row=0, column=2, padx=6, pady=5)

        self.btn_plantarse = tk.Button(
            self.frame_botones,
            text="⏹️ Plantarse",
            command=self.plantarse,
            state="disabled",
            width=13,
            font=("Arial", 11, "bold"),
            bg="#dc3545",
            fg="white",
            activebackground="#a71d2a",
            activeforeground="white",
            relief="raised",
            bd=3,
        )
        self.btn_plantarse.grid(row=0, column=3, padx=6, pady=5)

        self.btn_nueva_partida = tk.Button(
            self.frame_botones,
            text="🔄 Nueva Partida",
            command=self.nueva_partida,
            state="disabled",
            width=13,
            font=("Arial", 11, "bold"),
            bg="#6c757d",
            fg="white",
            activebackground="#343a40",
            activeforeground="white",
            relief="raised",
            bd=3,
        )
        self.btn_nueva_partida.grid(row=0, column=4, padx=6, pady=5)

        # Botón Salir
        self.btn_salir = tk.Button(
            self.frame_botones,
            text="Salir",
            command=self.ventana.quit,
            width=13,
            font=("Arial", 11, "bold"),
            bg="#222",
            fg="white",
            activebackground="#555",
            activeforeground="white",
            relief="raised",
            bd=3,
        )
        self.btn_salir.grid(row=0, column=5, padx=6, pady=5)

        self.iniciar_concurrencia()

    # ---------------------------------------------------------------------
    #   Utilidades
    # ---------------------------------------------------------------------
    def obtener_saldo_inicial(self):
        """Solicita un saldo positivo antes de comenzar."""
        while self.saldo <= 0:
            saldo_input = simpledialog.askfloat(
                "Saldo inicial", "Ingrese su saldo inicial:", minvalue=0.01
            )
            if saldo_input is None:
                self.ventana.destroy()
                return
            if saldo_input and saldo_input > 0:
                self.saldo = saldo_input

    def actualizar_manos(self, inicio=False):
        jugador_mano = self.juego.jugador.mostrar_mano()
        puntos_jugador = 0 if inicio else calcular_valor(self.juego.jugador.mano)
        self.lbl_mano_jugador.config(text=f"Tu mano: {', '.join(jugador_mano)}")
        self.lbl_puntos_jugador.config(text=f"Tus puntos: {puntos_jugador}")

        crupier_mano = self.juego.crupier.mostrar_mano()
        puntos_crupier = 0 if inicio else calcular_valor(self.juego.crupier.mano)
        self.lbl_mano_crupier.config(text=f"Crupier: {', '.join(crupier_mano)}")
        self.lbl_puntos_crupier.config(text=f"Puntos crupier: {puntos_crupier}")

    def fin_turno(self):
        self.btn_pedir.config(state="disabled")
        self.btn_duplicar.config(state="disabled")
        self.btn_plantarse.config(state="disabled")
        self.btn_repartir.config(state="disabled")
        self.btn_nueva_partida.config(state="normal")

    def check_saldo(self):
        if self.saldo <= 0:
            messagebox.showinfo("Sin saldo", "Te has quedado sin saldo.")
            self.obtener_saldo_inicial()
            self.lbl_saldo.config(text=f"Saldo: ${self.saldo:.2f}")

    def iniciar_concurrencia(self):
        # Inicia un hilo de reloj (daemon, no bloquea cierre)
        self.hilo_reloj = threading.Thread(target=reloj, daemon=True)
        self.hilo_reloj.start()
        # Inicia procesos reales para cada capa
        iniciar_procesos()

    # ------------------------------------------------------------------
    #   Flujo de juego
    # ------------------------------------------------------------------
    def repartir(self):
        """Inicia una nueva ronda y descuenta la apuesta del saldo."""
        try:
            apuesta = float(self.entry_apuesta.get())
            if apuesta <= 0 or apuesta > self.saldo:
                raise ValueError
        except (ValueError, TypeError):
            self.lbl_estado.config(text="Ingrese una apuesta válida y dentro de su saldo.")
            return

        # Descontar apuesta inmediatamente
        self.saldo -= apuesta
        self.lbl_saldo.config(text=f"Saldo: ${self.saldo:.2f}")

        self.juego.nueva_ronda(apuesta)
        # Mostrar los puntos reales al repartir (no 0)
        self.actualizar_manos(inicio=False)
        self.lbl_apuesta_actual.config(text=f"Apuesta actual: ${self.juego.apuesta:.2f}")

        self.lbl_estado.config(text="Turno del jugador")
        self.btn_pedir.config(state="normal")
        self.btn_duplicar.config(state="normal")  # Solo habilitado tras repartir
        self.btn_plantarse.config(state="normal")
        self.btn_repartir.config(state="disabled")
        self.btn_nueva_partida.config(state="disabled")

        self.duplicar_disponible = True  # Flag para controlar el uso de duplicar

    def pedir(self):
        """Jugador pide una carta."""
        self.juego.jugador_pide()
        self.actualizar_manos()
        # Deshabilitar duplicar después del primer turno
        self.btn_duplicar.config(state="disabled")
        self.duplicar_disponible = False
        if self.juego.jugador_se_paso():
            self.lbl_estado.config(text="Te pasaste. Perdiste.")
            self.finalizar_partida("Perdiste")
            self.fin_turno()

    def duplicar_apuesta(self):
        if not getattr(self, "duplicar_disponible", False):
            return  # No permitir duplicar si ya se pidió carta o se duplicó antes
        if self.saldo >= self.juego.apuesta:
            self.saldo -= self.juego.apuesta  # Resta exactamente lo apostado originalmente
            self.juego.apuesta *= 2
            self.lbl_saldo.config(text=f"Saldo: ${self.saldo:.2f}")
            self.lbl_apuesta_actual.config(text=f"Apuesta actual: ${self.juego.apuesta:.2f}")
            self.btn_duplicar.config(state="disabled")  # Deshabilitar tras usar
            self.duplicar_disponible = False
            self.pedir()
            self.plantarse()
        else:
            messagebox.showwarning("Sin saldo suficiente", "No tienes suficiente saldo para duplicar la apuesta.")



    def plantarse(self):
        self.lbl_estado.config(text="Turno del crupier...")
        self.juego.turno_crupier_async(callback=self._post_turno_crupier)
        print("Ejecutar turno crupier en hilo, y luego actualizar interfaz con after")
        thread_id = threading.current_thread().ident
        print(f"ID del hilo: {thread_id}")

    def _post_turno_crupier(self):
        self.ventana.after(0, self._actualizar_despues_crupier)
        print("Esta función corre en hilo distinto, usamos after para interactuar con Tkinter")
        thread_id = threading.current_thread().ident
        print(f"ID del hilo: {thread_id}")

    def _actualizar_despues_crupier(self):
        resultado = self.juego.resultado()
        self.actualizar_manos()
        self.lbl_estado.config(text=resultado)
        print("Guardar partida en hilo sin bloquear la UI")
        thread_id = threading.current_thread().ident
        print(f"ID del hilo: {thread_id}")
        self.finalizar_partida(resultado)  # <-- llamada directa aquí
        self.fin_turno()

    def _resolver_crupier(self):
        self.juego.turno_crupier()
        resultado = self.juego.resultado()
        time.sleep(1.2)  # Simula pensar
        self.ventana.after(0, lambda: self._mostrar_resultado(resultado))

    def _mostrar_resultado(self, resultado):
        self.actualizar_manos()
        self.lbl_estado.config(text=resultado)
        self.finalizar_partida(resultado)
        self.fin_turno()

    # ------------------------------------------------------------------
    #   Cierre de ronda y pago
    # ------------------------------------------------------------------
    def finalizar_partida(self, resultado):
        if resultado == "Ganaste":
            self.saldo += 2 * self.juego.apuesta
            print(f"[DEBUG] Ganaste. Nuevo saldo: {self.saldo:.2f}")
        elif resultado == "Empate":
            self.saldo += self.juego.apuesta
            print(f"[DEBUG] Empate. Nuevo saldo: {self.saldo:.2f}")
        else:
            print(f"[DEBUG] Perdiste. Saldo se mantiene en: {self.saldo:.2f}")

        # Actualizar saldo y estadísticas en BD
        if self.usuario_id:
            usuario = obtener_usuario(self.usuario_id)
            if usuario:
                manos = usuario[3] + 1
                victorias = usuario[4] + (1 if resultado == "Ganaste" else 0)
                derrotas = usuario[5] + (1 if resultado == "Perdiste" else 0)
                saldo_db = int(self.saldo)
                print(f"[DEBUG] Actualizando BD: manos={manos}, victorias={victorias}, derrotas={derrotas}, saldo={saldo_db}")
                actualizar_usuario(self.usuario_id, manos, victorias, derrotas, saldo_db)

        self.lbl_saldo.config(text=f"Saldo: ${self.saldo:.2f}")




    def nueva_partida(self):
        # Limpiar manos y puntajes
        self.lbl_mano_jugador.config(text="Tu mano:")
        self.lbl_puntos_jugador.config(text="Tus puntos: 0")
        self.lbl_mano_crupier.config(text="Crupier:")
        self.lbl_puntos_crupier.config(text="Puntos crupier: 0")
        self.lbl_estado.config(text="")
        self.lbl_apuesta_actual.config(text="Apuesta actual: $0.00")
        self.entry_apuesta.delete(0, tk.END)
        self.btn_repartir.config(state="normal")
        self.btn_nueva_partida.config(state="disabled")
        # se reinicia el objeto juego para barajar de nuevo
        self.juego = Juego()

    def ejecutar(self):
        self.ventana.mainloop()
        self.juego = Juego()
        self.btn_repartir.config(state="normal")
        self.btn_nueva_partida.config(state="disabled")
        # Opcional: reiniciar el objeto Juego si quieres barajar de nuevo
        self.juego = Juego()

    def ejecutar(self):
        self.ventana.mainloop()
        self.juego = Juego()