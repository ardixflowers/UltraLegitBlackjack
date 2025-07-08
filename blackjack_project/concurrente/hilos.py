import threading
import time

def reloj():
    while True:
        print("⏰ Reloj en marcha")
        time.sleep(5)

def iniciar_hilos():
    for _ in range(5):
        hilo = threading.Thread(target=reloj, daemon=True)
        hilo.start()
