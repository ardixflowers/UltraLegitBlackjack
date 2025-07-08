from multiprocessing import Process
import time

def simulacion():
    print("🔁 Proceso de simulación iniciado")
    time.sleep(10)
    print("🔁 Proceso terminado")

def iniciar_procesos():
    for _ in range(3):
        proceso = Process(target=simulacion)
        proceso.start()
