import matplotlib.pyplot as plt
from physics import apartado6
from gui import dibujar

datos = apartado6()                 # Calcula e imprime la frase en la terminal

fig, ax = plt.subplots(figsize=(10, 6))
dibujar(ax, datos)                  # Usa la misma función de dibujo que el dashboard
plt.show()
