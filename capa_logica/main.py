from capa_datos.db import crear_tabla
from concurrente.hilos import iniciar_hilos
from concurrente.procesos import iniciar_procesos
from capa_presentacion.interfaz import Interfaz

def main():
    crear_tabla()
    iniciar_hilos()
    iniciar_procesos()

    app = Interfaz()
    app.ejecutar()

if __name__ == "__main__":
    main()
