"""
Apartado 6: Integración numérica
  1. Implementación propia (my_trapecio, my_simpson)
  2. Versión con NumPy (vectorizada)

"""
# ============================================================
# 6.1  Implementación propia 
# ============================================================

def my_trapecio(f, a, b, n):
    
    """
    Calcula la integral definida de f(x) desde a hasta b usando la regla del trapecio (sumar área del rectángulo y el área del triángulo) 
    con n subintervalos (puede ser par o impar)

    Para aplicar la regla de integración del trapecio todos los nodos deben estar equiespaciados

    Parámetros: 
                f: función a integrar
                a: límite inferior de integración  
                b: límite superior de integración
                n: número de subintervalos (hay n+1 nodos: x0, x1, ..., xn)
    
    Variables internas:
                h: delta x (distancia entre los nodos consecutivos de evaluación)
    """
    h= (b-a)/n
    y= list(map(lambda i: f(a+i*h), range(n+1))) #Calculamos f(xi) para todos los nodos con la función lambda y luego lo guardamos en una lista para finalmente realizar un slicing.
    
    return (h/2)*(y[0] + 2*sum(y[1:-1]) + y[-1]) # NODOS EXTREMOS (y(0) y y(n)) multiplicados por 1,
                                                 # NODOS INTERIORES y(1) a y(n-1) multiplicados por 2 


def my_simpson(f, a, b, n):
    
    """
    Calcula la integral definida de f(x) desde a hasta b utilizando la regla de Simpson (con la aproximación de un polinomio de segundo grado)
    suma el área de la parábola que pasa por 3 nodos equiespaciados

    Utilizamos los mismos parámetros que en la función my_trapecio, con la restricción de que n debe ser necesariamente par
    y el número de nodos impar para asi poder aplicar la regla de Simpson.

    """
    
    if n % 2 != 0:
        raise ValueError("El número de subintervalos debe ser necesariamente par (número de nodos impar) para utilizar Simpson")
    
    h= (b-a)/n
    y = list(map(lambda i: f(a + i*h), range(n+1)))   #Calculamos f en cada nodo y lo guardamos en una lista para luego realizar un slicing
    
    return (h/3)*(y[0] + 4*sum(y[1:-1:2]) + 2*sum(y[2:-1:2]) + y[-1]) # NODOS EXTREMOS (y(0) y y(n)) multiplicados por 1,
                                                                      # NODOS INTERIORES IMPARES y(1) a y(n-1) multiplicados por 4,
                                                                      # NODOS INTERIORES PARES y(2) a y(n-2) multiplicados por 2

# ============================================================
# 6.2  Implementacion con numpy (vectorizada)
# ============================================================

import numpy as np
from scipy.integrate import simpson

def np_trapecio(f, a, b, n):

    """
    Calcula la integral definida de f(x) desde a hasta b usando la regla del trapecio
    con la función de NumPy (np.trapezoid), con n subintervalos (puede ser par o impar).

    Parámetros:
                f: función a integrar (debe aceptar arrays de NumPy, p. ej. np.sin, np.exp)
                a: límite inferior de integración
                b: límite superior de integración
                n: número de subintervalos (hay n+1 nodos: x0, x1, ..., xn)

    Variables internas:
                x: array con los n+1 nodos equiespaciados
    """
    x = np.linspace(a, b, n+1)          # Creamos los n+1 nodos equiespaciados
    return np.trapezoid(f(x), x)        # Evaluamos f en todos los nodos y aplicamos el trapecio de NumPy


def sp_simpson(f, a, b, n):

    """
    Calcula la integral definida de f(x) desde a hasta b usando la regla de Simpson
    con la función de SciPy (scipy.integrate.simpson).

    Utilizamos los mismos parámetros que en la función np_trapecio, con la restricción de que n debe ser
    necesariamente par (número de nodos impar) para poder aplicar la regla de Simpson.
    """
    if n % 2 != 0:
        raise ValueError("El número de subintervalos debe ser necesariamente par (número de nodos impar) para utilizar Simpson")

    x = np.linspace(a, b, n+1)          # Creamos los n+1 nodos equiespaciados
    return simpson(f(x), x=x)           # Evaluamos f en todos los nodos y aplicamos el Simpson de SciPy
