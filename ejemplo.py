import tkinter as tk
import random

# --- Lógica del juego ---
VALORES = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
           'J': 10, 'Q': 10, 'K': 10}

def crear_mazo():
    return list(VALORES.keys()) * 4

def calcular_puntaje(mano):
    total = sum(VALORES[c] for c in mano)
    ases = mano.count('A')
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

# --- Estado inicial ---
saldo = 1000
apuesta = 0
mazo = []
mano_jugador = []
mano_banca = []
terminado = False

# --- Funciones principales ---
def nueva_ronda():
    global mazo, mano_jugador, mano_banca, terminado, apuesta
    try:
        apuesta = int(entry_apuesta.get())
        if apuesta <= 0 or apuesta > saldo:
            raise ValueError
    except:
        mostrar_mensaje("⚠ Ingrese una apuesta válida.")
        return

    # Reparto inicial
    mazo = crear_mazo()
    random.shuffle(mazo)
    mano_jugador = [mazo.pop(), mazo.pop()]
    mano_banca = [mazo.pop()]
    terminado = False

    entry_apuesta.config(state=tk.DISABLED)
    btn_apostar.config(state=tk.DISABLED)
    btn_pedir.config(state=tk.NORMAL)
    btn_plantarse.config(state=tk.NORMAL)

    mostrar_mensaje("Tu turno. ¿Pedir o Plantarse?")
    actualizar_pantalla()

def pedir():
    global terminado
    if terminado:
        return
    mano_jugador.append(mazo.pop())
    actualizar_pantalla()
    if calcular_puntaje(mano_jugador) > 21:
        finalizar_ronda("¡Te pasaste! Pierdes.", "perder")

def plantarse():
    global terminado
    if terminado:
        return
    # Turno banca
    while calcular_puntaje(mano_banca) < 17:
        mano_banca.append(mazo.pop())
    punt_j = calcular_puntaje(mano_jugador)
    punt_b = calcular_puntaje(mano_banca)
    if punt_b > 21 or punt_j > punt_b:
        finalizar_ronda("¡Ganaste!", "ganar")
    elif punt_j < punt_b:
        finalizar_ronda("Pierdes.", "perder")
    else:
        finalizar_ronda("Empate.", "empate")

def finalizar_ronda(mensaje, resultado):
    global saldo, terminado
    terminado = True
    if resultado == "ganar":
        saldo += apuesta
    elif resultado == "perder":
        saldo -= apuesta

    actualizar_pantalla()
    mostrar_mensaje(mensaje)
    entry_apuesta.config(state=tk.NORMAL)
    btn_apostar.config(state=tk.NORMAL)
    btn_pedir.config(state=tk.DISABLED)
    btn_plantarse.config(state=tk.DISABLED)

    if saldo <= 0:
        mostrar_mensaje("¡Sin saldo! Fin del juego.")
        btn_apostar.config(state=tk.DISABLED)

def actualizar_pantalla():
    label_jugador.config(text=f"Jugador: {' '.join(mano_jugador)}  ({calcular_puntaje(mano_jugador)})")
    banca_txt = ' '.join(mano_banca)
    if terminado:
        banca_txt += f" ({calcular_puntaje(mano_banca)})"
    else:
        banca_txt += " (?)"
    label_banca.config(text=f"Banca: {banca_txt}")
    label_saldo.config(text=f"💰 Saldo: ${saldo}")

def mostrar_mensaje(msg):
    label_estado.config(text=msg)

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Blackjack - UX Mejorada")

# Estilo general
ventana.configure(bg="#222")
fuente = ("Segoe UI", 14)
fuente_titulo = ("Segoe UI", 18, "bold")

# Encabezado
label_saldo = tk.Label(ventana, text="", font=fuente_titulo, fg="white", bg="#222")
label_saldo.pack(pady=10)

# Apuesta
frame_apuesta = tk.Frame(ventana, bg="#222")
frame_apuesta.pack()
tk.Label(frame_apuesta, text="Apuesta:", font=fuente, fg="white", bg="#222").pack(side=tk.LEFT)
entry_apuesta = tk.Entry(frame_apuesta, font=fuente, width=6)
entry_apuesta.insert(0, "100")
entry_apuesta.pack(side=tk.LEFT, padx=5)
btn_apostar = tk.Button(frame_apuesta, text="Apostar", font=fuente, bg="#4caf50", fg="white", command=nueva_ronda)
btn_apostar.pack(side=tk.LEFT, padx=10)

# Juego
label_jugador = tk.Label(ventana, text="Jugador:", font=fuente, fg="white", bg="#222")
label_jugador.pack(pady=10)
label_banca = tk.Label(ventana, text="Banca:", font=fuente, fg="white", bg="#222")
label_banca.pack(pady=10)

# Estado
label_estado = tk.Label(ventana, text="", font=fuente_titulo, fg="#ffd700", bg="#222")
label_estado.pack(pady=15)

# Botones de juego
frame_botones = tk.Frame(ventana, bg="#222")
frame_botones.pack()

btn_pedir = tk.Button(frame_botones, text="Pedir", font=fuente, width=10, command=pedir, state=tk.DISABLED)
btn_pedir.grid(row=0, column=0, padx=10)

btn_plantarse = tk.Button(frame_botones, text="Plantarse", font=fuente, width=10, command=plantarse, state=tk.DISABLED)
btn_plantarse.grid(row=0, column=1, padx=10)

# Inicializar
actualizar_pantalla()
mostrar_mensaje("Ingresa tu apuesta para comenzar.")

ventana.mainloop()
