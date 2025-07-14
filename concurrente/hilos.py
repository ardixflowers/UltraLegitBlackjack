import threading
import time

# Evento global para controlar el hilo del reloj
stop_event = threading.Event()

def reloj():
    while not stop_event.is_set():
        print("⏰ Reloj en marcha")
        time.sleep(5)

def detener_reloj():
    stop_event.set()

def iniciar_hilos():
    for _ in range(5):
        hilo = threading.Thread(target=reloj, daemon=True)
        hilo.start()
