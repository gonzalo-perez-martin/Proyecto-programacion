"""
mathematics.py
Funciones matemáticas utilizadas en el proyecto AeroPy-I.

Contenido:
  Apartado 1: ...
  Apartado 2: ...
  Apartado 3: ...
  Apartado 4: ...
  Apartado 5: ...
  Apartado 6: Integración numérica
      6.1 Implementación propia (my_trapecio, my_simpson)
      6.2 Implementación con NumPy / SciPy (np_trapecio, sp_simpson)
"""


# ============================================================
# APARTADO 1: ...
# ============================================================

# --- 1.1 Implementación propia ---

def my_Gauss(A,b):
  n = len(b)   x = zeros(n)  # n es el número de incognitas y x donde guardaremos las soluciones
  # Eliminación hacia adelante
  for k in range(n-1):                             # Recorremos columnas donde se usa un pivote
      for i in range(k+1, n):                      # Recorremos las filas debajo del pivote
          C = A[i,k] / A[k,k]                      # Calculamos por cuánto hay que multiplicar el número de abajo del pìvote para eliminarlo
          A[i,k:] = A[i,k:] - C * A[k,k:]          # Se resta a la fila que se quiere eliminar la fila del pivote por el número anterior
          b[i] = b[i] - C * b[k]                   # Lo mismo pero en el vector de términos independientes
  # Sustitución hacia atrás
  for i in range(n-1, -1, -1):                               # Ahora que tenemos la matriz triangular superior, por lo que se recorren las filas de abajo a arriba
       x[i] = (b[i] - dot(A[i,i+1:], x[i+1:])) / A[i,i]      # Se calcula el producto escalar de los coeficientes de las incógnitas, 
  return x                                                   # se pasan esos términos al otro lado y se divide por el coeficiente de la incógnita que se quiere obtener (basicamente un despeje)


def my_Jacobi(A, b): 
    N = len(b)                                      # N es el número de incógnitas
    x, D, R = zeros(N), zeros(N), zeros((N,N))      # x es el vector inicial de incógnitas, D almacenará la diagonal principal y R los elementos fuera de la diagonal principal
    xn = 1 + x                                      # Se crea una aproximacion diferente de x para que entre en bucle
    tolerance = 1e-10                               # Se establece el error maximo permitido
    k, max_iter = 0, 100                            # k es el contador de iteraciones y 100 el maximo
  #Iteración
    for i in range(N): 
        for j in range(N): 
            if i == j:                               # Se toma lña diagonal principal i==j
                D[i] = A[i,j]                        # Se guardan los elementos en la diagonal
                R[i,j] = 0                           # Se pone un 0 en esa posición de R (se quita la diagonal principal en R)
            else:
                R[i,j] = A[i,j]                      #Se guarda el elemento en R
   
    while norm(xn - x) > tolerance and k < max_iter:    # Se calcula la direfencia entre las aproximaciones y tolerance comprueba si todavia se está lejos de la aproximación y se ve si se superaron las iteraciones
        x = xn                                          # Se guarda la aproximación anterior
        xn = (b - dot(R, x)) / D                        # Calculamos una nueva aproximación, todo esto se basa en la formula matemática de Jacobi
        k += 1                                          # Se suma una iteración evitando que siga hasta el infinito

    return xn


def my_Gauss_Seidel(A, b):

    N = len(b)                                                       # N es el número de incognitas
    x1, x2, b1 = zeros(N), zeros(N), zeros(N)                        # x1 aproximación anterior, x2 aproximación nueva y b1 almacena los términos independientes modificados
    Error, tolerance = 1, 1e-10                                      # Error es el error inicial para entrar en bucle y tolerance el error maximo permitido
    k, max_iter = 0, 100                                             # K iteraciones iniciales con un máximo de 100
    #Iteracion
    while Error > tolerance  and  k < max_iter:                      # Mientras que el error sea mayor que la tolerancia y k no haya alcanzado el máximo seguimos calculando

        x1[:] = x2[:]                                                # Calculamos los valores actuales de x1 y x2
        for i in range(N):                                            
            b1[i] = b[i] - dot( A[i, i+1:], x1[i+1:] )               # Calculamos los términos independientes restando las incógnitas a la derecha de la diagonal

        for i in range(N):                                           # Selecciona los elementos a la izquierda de la diagonal A[i,:i], se selecciona las soluciones que hemos calculado x2[:i] y se multiplican ambos vectores
            x2[i]  = ( b1[i] - dot( A[i, :i], x2[:i] ) )/ A[i, i]    # Una vez multiplicados se dividen por la diagonal  
         
        Error = norm(x2-x1)                                          # Calculamos la diferencia entre las aproximaciones
        k += 1                                                       # Sumamos una iteración
      

# --- 1.2 Implementación con NumPy ---

def LU(A,b):
    lu, piv = lu_factor(A)                         # lu_factor hace la factorización LU, lu almacena las matrices L y U y piv los intercambios de filas realizados
    x = lu_solve((lu, piv), b)                     # Se resuelven los sistemas triangulares utilizando LU
    return x


# ============================================================
# APARTADO 2: ...
# ============================================================

# --- 2.1 Implementación propia ---


# --- 2.2 Implementación con NumPy ---



# ============================================================
# APARTADO 3: ...
# ============================================================

# --- 3.1 Implementación propia ---


# --- 3.2 Implementación con NumPy ---



# ============================================================
# APARTADO 4: ...
# ============================================================

# --- 4.1 Implementación propia ---


# --- 4.2 Implementación con NumPy ---



# ============================================================
# APARTADO 5: ...
# ============================================================

# --- 5.1 Implementación propia ---


# --- 5.2 Implementación con NumPy ---



# ============================================================
# APARTADO 6: Integración numérica
# ============================================================

# --- 6.1 Implementación propia ---

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
    y el número de nodos impar para así poder aplicar la regla de Simpson.

    """

    if n % 2 != 0:
        raise ValueError("El número de subintervalos debe ser necesariamente par (número de nodos impar) para utilizar Simpson")

    h= (b-a)/n
    y = list(map(lambda i: f(a + i*h), range(n+1)))   #Calculamos f en cada nodo y lo guardamos en una lista para luego realizar un slicing

    return (h/3)*(y[0] + 4*sum(y[1:-1:2]) + 2*sum(y[2:-1:2]) + y[-1]) # NODOS EXTREMOS (y(0) y y(n)) multiplicados por 1,
                                                                      # NODOS INTERIORES IMPARES y(1) a y(n-1) multiplicados por 4,
                                                                      # NODOS INTERIORES PARES y(2) a y(n-2) multiplicados por 2


# --- 6.2 Implementación con NumPy / SciPy ---

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
