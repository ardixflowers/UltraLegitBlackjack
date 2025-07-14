from capa_presentacion.interfaz import Interfaz

def main():
    app = Interfaz()
    app.iniciar_concurrencia() 
    app.ejecutar()

if __name__ == "__main__":
    main()