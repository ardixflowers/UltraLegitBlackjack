from multiprocessing import Process
import os
import sys

def ejecutar_modulo(ruta_modulo):
    """Ejecuta un archivo Python como proceso independiente."""
    os.system(f"{sys.executable} {ruta_modulo}")

def iniciar_procesos():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rutas = [
        os.path.join(base, "capa_datos", "main.py"),
        os.path.join(base, "capa_logica", "main.py"),
        os.path.join(base, "capa_presentacion", "main.py"),
    ]
    procesos = []
    for ruta in rutas:
        if os.path.exists(ruta):
            p = Process(target=ejecutar_modulo, args=(ruta,))
            p.start()
            procesos.append(p)
    # Opcional: esperar a que terminen
    # for p in procesos:
    #     p.join()
