from capa_datos.db import crear_tabla
from capa_presentacion.interfaz import Interfaz

def main():
    crear_tabla()
    app = Interfaz()
    app.iniciar_concurrencia() 
    app.ejecutar()

if __name__ == "__main__":
    main()
