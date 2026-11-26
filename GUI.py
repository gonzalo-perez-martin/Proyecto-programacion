"""
gui.py
Interfaz gráfica del dashboard AeroPy-I.

Requisitos de la guía:
  - UNA sola ventana interactiva con matplotlib.widgets
  - Panel izquierdo con RadioButtons para elegir el apartado (1 a 6)
  - Un Slider que controla un parámetro físico (Mach crítico del apartado 4, entre 0.8 y 2.5)
  - El resultado numérico de cada apartado se muestra sobre la figura (ax.text) y se actualiza

Cada apartado de physics.py devuelve un diccionario con lo necesario para dibujarlo:
    {
        "titulo":  str,
        "xlabel":  str,
        "ylabel":  str,
        "curvas":  [ (x, y, estilo, etiqueta), ... ],   # estilo: "-", "o", "--", etc.
        "barras":  (etiquetas, valores)  o  None,        # opcional, p. ej. apartado 1
        "texto":   str                                   # resultado numérico a mostrar
    }
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider


def dibujar(ax, datos):
    """Dibuja en el eje principal el apartado descrito por el diccionario 'datos'."""
    ax.clear()

    if datos.get("barras") is not None:                       # Gráfico de barras
        etiquetas, valores = datos["barras"]
        ax.bar(etiquetas, valores, color="tab:blue")
    for x, y, estilo, etiqueta in datos.get("curvas", []):    # Curvas / puntos
        ax.plot(x, y, estilo, label=etiqueta)

    ax.set_title(datos["titulo"])
    ax.set_xlabel(datos["xlabel"])
    ax.set_ylabel(datos["ylabel"])
    ax.grid(True, alpha=0.3)
    if datos.get("curvas"):
        ax.legend(loc="upper right")

    # Reporte numérico superpuesto en la figura
    ax.text(0.02, 0.95, datos["texto"], transform=ax.transAxes, va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))


def lanzar_dashboard(resultados, recalcular_apartado4):
    """
    Crea la ventana única del dashboard.

    Parámetros:
                resultados: diccionario {1: datos_ap1, ..., 6: datos_ap6} devuelto por physics.py
                recalcular_apartado4: función que recibe el Mach crítico y devuelve los datos del apartado 4
                                      (se llama cada vez que se mueve el Slider)
    """
    fig = plt.figure(figsize=(12, 7))
    fig.canvas.manager.set_window_title("Dashboard AeroPy-I")

    # --- Zonas de la ventana: [izquierda, abajo, ancho, alto] en fracciones de la figura ---
    ax_principal = fig.add_axes([0.30, 0.20, 0.65, 0.70])     # Gráfica principal
    ax_radio     = fig.add_axes([0.03, 0.40, 0.20, 0.40])     # Panel izquierdo: RadioButtons
    ax_slider    = fig.add_axes([0.30, 0.06, 0.55, 0.03])     # Slider abajo

    # --- RadioButtons: selección de apartado ---
    nombres = ["1. Balance de masas", "2. Calibración motor", "3. Perfil atmosférico",
               "4. Régimen transónico", "5. Acelerómetro", "6. Altitud apogeo"]
    ax_radio.set_title("Apartado")
    radio = RadioButtons(ax_radio, nombres)

    # --- Slider: Mach crítico (solo afecta al apartado 4) ---
    slider = Slider(ax_slider, "Mach crítico", 0.8, 2.5, valinit=1.2)

    estado = {"apartado": 1}                                  # Apartado que se está mostrando

    def al_elegir_apartado(etiqueta):
        estado["apartado"] = nombres.index(etiqueta) + 1      # "4. Régimen..." -> 4
        dibujar(ax_principal, resultados[estado["apartado"]])
        fig.canvas.draw_idle()

    def al_mover_slider(valor):
        resultados[4] = recalcular_apartado4(valor)           # Recalcula tc con el nuevo Mach
        if estado["apartado"] == 4:                           # Solo redibuja si se está viendo el 4
            dibujar(ax_principal, resultados[4])
            fig.canvas.draw_idle()

    radio.on_clicked(al_elegir_apartado)
    slider.on_changed(al_mover_slider)

    dibujar(ax_principal, resultados[1])                      # Vista inicial: apartado 1
    plt.show()
