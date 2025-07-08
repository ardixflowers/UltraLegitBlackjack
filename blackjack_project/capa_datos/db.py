import sqlite3

def crear_tabla():
    with sqlite3.connect("blackjack.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador TEXT,
                resultado TEXT,
                apuesta REAL,
                ganancia REAL,
                fecha TEXT
            )
        """)
        conn.commit()

def guardar_partida(jugador, resultado, apuesta, ganancia, fecha):
    with sqlite3.connect("blackjack.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO partidas (jugador, resultado, apuesta, ganancia, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (jugador, resultado, apuesta, ganancia, fecha.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
