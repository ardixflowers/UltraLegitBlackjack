import sqlite3
import os

DB_PATH = "blackjack.db"

# Elimina el archivo si existe para asegurar estructura limpia
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE usuario (
            id_usuario TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            manos INTEGER NOT NULL,
            victorias INTEGER NOT NULL,
            derrotas INTEGER NOT NULL,
            saldo INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador TEXT NOT NULL,
            resultado TEXT NOT NULL,
            apuesta INTEGER NOT NULL,
            ganancia INTEGER NOT NULL,
            fecha TEXT NOT NULL
        )
    """)
    conn.commit()
