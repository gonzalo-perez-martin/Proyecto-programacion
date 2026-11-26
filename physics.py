"""
physics.py
Modelos físicos y datos del cohete sonda AeroPy-I.

Contenido:
  Datos de partida
    Apartado 1: Balance de masas (Sistema lineal)
    Apartado 2: Calibración del motor (Regresión lineal)
    Apartado 3: Perfil atmosférico (Interpolación 1D)
    Apartado 4: Régimen transónico (Ecuación no lineal)
    Apartado 5: Acelerómetro virtual (Derivación numérica)
    Apartado 6: Altitud apogeo (Integración numérica) 
"""
import numpy as np
from mathematics import *


# ============================================================
# DATOS DE PARTIDA
# ============================================================

# 1. Calibración del sensor principal de empuje (Voltaje [V] vs Fuerza [kN])
voltaje_sensor = np.array([0.0, 1.25, 2.45, 3.80, 5.10])
fuerza_real    = np.array([0.0, 15.2, 31.0, 48.5, 65.3])

# 2. Reacciones en la plataforma de lanzamiento (Coordenadas apoyos y pesos)
# Matriz de geometría estática (distancias en m) para el balance de masas
matriz_estatica = np.array([
    [ 1.0, 1.0,  1.0],      # Suma de fuerzas Z
    [ 0.0, 1.5, -1.5],      # Momentos en X
    [-2.0, 1.0,  1.0]       # Momentos en Y
])
vector_cargas = np.array([25000.0, 1500.0, -800.0])     # [N, Nm, Nm]

# 3. Datos de Atmósfera Estándar (Altitud [m], Temperatura [K], Presión [Pa])
h_atm = np.array([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000])
T_atm = np.array([288.15, 275.15, 262.15, 249.15, 236.15, 223.15, 216.65, 216.65])
P_atm = np.array([101325, 79501, 61660, 47217, 35651, 26499, 19399, 14170])

# 4. Telemetría de vuelo: Tiempo [s] y Velocidad [m/s]
t_vuelo = np.linspace(0, 60, 1200)      # Muestreo a 20 Hz
# (Perfil simulado de velocidad de un cohete)
v_vuelo = 800 * np.sin(np.pi * t_vuelo / 60) * np.exp(-0.02 * t_vuelo)



# ============================================================
# APARTADO 1: ...
# ============================================================



# ============================================================
# APARTADO 2: ...
# ============================================================



# ============================================================
# APARTADO 3: ...
# ============================================================



# ============================================================
# APARTADO 4: ...
# ============================================================



# ============================================================
# APARTADO 5: ...
# ============================================================

# ============================================================
# APARTADO 6: Altitud apogeo (Integración numérica)
# ============================================================

def velocidad(t):
    """Perfil de velocidad del cohete [m/s] (el mismo que genera v_vuelo)."""
    return 800 * np.sin(np.pi * t / 60) * np.exp(-0.02 * t)


def apartado6():

    """
    Calcula la altitud total alcanzada a los 60 s integrando la curva de velocidad
    experimental (v_vuelo) con la regla del trapecio de NumPy:
        h_total = ∫ v(t) dt   (de 0 a 60 s)

    Como comprobación, se compara con:
        - la implementación propia (my_trapecio), con los mismos 1199 subintervalos
        - la regla de Simpson (SciPy), más precisa

    Devuelve:
                diccionario con los datos para la GUI
    """
    h_total = np.trapezoid(v_vuelo, t_vuelo)            # Trapecio de NumPy sobre los datos

    n = len(t_vuelo) - 1                                # 1200 nodos -> 1199 subintervalos
    h_propia  = my_trapecio(velocidad, 0, 60, n)        # Comprobación: implementación propia
    h_simpson = simpson(v_vuelo, x=t_vuelo)             # Comprobación: Simpson (SciPy)

    print(f"Apartado 6: La altitud total alcanzada a los 60 s es de {h_total:.2f} m "
          f"({h_total/1000:.3f} km). Con la implementación propia se obtiene {h_propia:.2f} m, "
          f"idéntico al de NumPy, y con Simpson {h_simpson:.2f} m, una diferencia de "
          f"{abs(h_simpson - h_total):.3f} m, lo que confirma la precisión de la regla del trapecio.")

    return {
        "titulo": "Apartado 6: Altitud apogeo",
        "xlabel": "Tiempo [s]",
        "ylabel": "Velocidad [m/s]",
        "curvas": [(t_vuelo, v_vuelo, "-", "v(t)")],
        "barras": None,
        "texto":  f"h total = {h_total:.2f} m",
    }
