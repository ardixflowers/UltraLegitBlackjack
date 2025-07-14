import mysql.connector
from contextlib import contextmanager

# Configura aquí los datos de tu servidor XAMPP/MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Cambia si tienes contraseña
    "database": "blackjack",
    "port": 3306     # Cambia si tu XAMPP usa otro puerto
}

@contextmanager
def get_conn():
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def crear_tabla():
    # No es necesario si la base ya existe y fue creada por el SQL, pero puedes dejarlo vacío o solo para pruebas
    pass

def guardar_partida(jugador, resultado, apuesta, ganancia, fecha):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO partidas (jugador, resultado, apuesta, ganancia, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, (jugador, resultado, apuesta, ganancia, fecha.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

# --- Casino ---
def obtener_estado_casino():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT saldo, dealers, jugadores_activos FROM casino LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {"saldo": row[0], "dealers": row[1], "jugadores_activos": row[2]}
        return None

def actualizar_estado_casino(saldo, dealers, jugadores_activos):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM casino")
        cursor.execute(
            "INSERT INTO casino (saldo, dealers, jugadores_activos) VALUES (%s, %s, %s)",
            (saldo, dealers, jugadores_activos)
        )
        conn.commit()

def modificar_saldo_casino(monto):
    estado = obtener_estado_casino()
    if estado:
        nuevo_saldo = estado["saldo"] + monto
        actualizar_estado_casino(nuevo_saldo, estado["dealers"], estado["jugadores_activos"])
        return nuevo_saldo
    return None

# --- Dealer ---
def agregar_dealer(id_dealer, nombre):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dealer (id_dealer, nombre, manos_jugadas, manos_ganadas, manos_perdidas)
            VALUES (%s, %s, 0, 0, 0)
        """, (id_dealer, nombre))
        conn.commit()

def obtener_dealer(id_dealer):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dealer WHERE id_dealer=%s", (id_dealer,))
        row = cursor.fetchone()
        if row:
            return {
                "id_dealer": row[0],
                "nombre": row[1],
                "manos_jugadas": row[2],
                "manos_ganadas": row[3],
                "manos_perdidas": row[4]
            }
        return None

def actualizar_dealer(id_dealer, manos_jugadas, manos_ganadas, manos_perdidas):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE dealer
            SET manos_jugadas=%s, manos_ganadas=%s, manos_perdidas=%s
            WHERE id_dealer=%s
        """, (manos_jugadas, manos_ganadas, manos_perdidas, id_dealer))
        conn.commit()

def dealer_paga_apuesta(id_dealer, monto):
    # El dealer descuenta el monto del saldo del casino
    estado = obtener_estado_casino()
    if estado and estado["saldo"] >= monto:
        modificar_saldo_casino(-monto)
        dealer = obtener_dealer(id_dealer)
        if dealer:
            actualizar_dealer(
                id_dealer,
                dealer["manos_jugadas"] + 1,
                dealer["manos_ganadas"],
                dealer["manos_perdidas"]
            )
        return True
    return False

def dealer_recibe_apuesta(id_dealer, monto):
    # El dealer suma el monto al saldo del casino
    estado = obtener_estado_casino()
    if estado:
        modificar_saldo_casino(monto)
        dealer = obtener_dealer(id_dealer)
        if dealer:
            actualizar_dealer(
                id_dealer,
                dealer["manos_jugadas"] + 1,
                dealer["manos_ganadas"],
                dealer["manos_perdidas"]
            )
        return True
    return False

# Funciones para la tabla usuario
def agregar_usuario(id_usuario, manos=0, victorias=0, derrotas=0, saldo=0):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario (id_usuario, manos, victorias, derrotas, saldo)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_usuario, manos, victorias, derrotas, saldo))
        conn.commit()

def actualizar_usuario(id_usuario, manos, victorias, derrotas, saldo):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuario
            SET manos=%s, victorias=%s, derrotas=%s, saldo=%s
            WHERE id_usuario=%s
        """, (manos, victorias, derrotas, saldo, id_usuario))
        conn.commit()

def obtener_usuario(id_usuario):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_usuario=%s", (id_usuario,))
        return cursor.fetchone()
        return cursor.fetchone()
