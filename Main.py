"""
main.py
Punto de entrada del dashboard de telemetría AeroPy-I.
Ejecuta los 6 apartados (resultados por terminal) y lanza la interfaz gráfica.
"""
from physics import (apartado1, apartado2, apartado3,
                     apartado4, apartado5, apartado6)
from gui import lanzar_dashboard


def main():
    print("=" * 60)
    print("  DASHBOARD DE TELEMETRÍA - COHETE SONDA AeroPy-I")
    print("=" * 60)

    # 1. Resolver los 6 apartados (cada uno imprime su interpretación)
    resultados = {
        1: apartado1(),     # Reacciones en los apoyos
        2: apartado2(),     # Recta de calibración (m, c)
        3: apartado3(),     # Temperatura T(t)
        4: apartado4(),     # Instante crítico tc
        5: apartado5(),     # Aceleración a(t)
        6: apartado6(),     # Altitud total
    }

    # 2. Lanzar la ventana interactiva con los resultados
    lanzar_dashboard(resultados)


if __name__ == "__main__":
    main()
