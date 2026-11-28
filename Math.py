from numpy import array, dot, zeros 
from numpy.linalg import norm
from scipy.linalg import lu, lu_factor, lu_solve

#Gauss
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

#Factorización LU
def LU(A,b):
    lu, piv = lu_factor(A)                         # lu_factor hace la factorización LU, lu almacena las matrices L y U y piv los intercambios de filas realizados
    x = lu_solve((lu, piv), b)                     # Se resuelven los sistemas triangulares utilizando LU
    return x

#Jacobi
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
# Jacobi no resuelve esta matriz porque no converge en este caso, ya que no es diagonalmente dominante. 
# Donde el valor absoluto de la diagonal principal es menor que la suma de los valores absolutos de los otros elementos en la fila.

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
    return x2
#Gauss Seidel no funciona por el mismo motivo que el Jacobi, no tiene una diagonal principal dominante.
