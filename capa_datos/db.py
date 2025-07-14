import sqlite3
from contextlib import contextmanager

# Configura aquí la ruta de tu archivo SQLite
DB_PATH = "blackjack.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def guardar_partida(jugador, resultado, apuesta, ganancia, fecha):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO partidas (jugador, resultado, apuesta, ganancia, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (jugador, resultado, apuesta, ganancia, fecha.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

# --- Funciones para la tabla usuario ---
def agregar_usuario(id_usuario, nombre, contrasena, manos=0, victorias=0, derrotas=0, saldo=0):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (id_usuario, nombre, contrasena, manos, victorias, derrotas, saldo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_usuario, nombre, contrasena, manos, victorias, derrotas, saldo))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error: El usuario ya existe.", e)
            raise
        except sqlite3.OperationalError as e:
            print("Error al agregar usuario:", e)
            raise

def actualizar_usuario(id_usuario, manos, victorias, derrotas, saldo):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE usuario
                SET manos=?, victorias=?, derrotas=?, saldo=?
                WHERE id_usuario=?
            """, (manos, victorias, derrotas, saldo, id_usuario))
            conn.commit()
        except sqlite3.OperationalError as e:
            print("Error al actualizar usuario:", e)
            raise

def obtener_usuario(id_usuario):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuario WHERE id_usuario=?", (id_usuario,))
            return cursor.fetchone()
        except sqlite3.OperationalError as e:
            print("Error al obtener usuario:", e)
            return None