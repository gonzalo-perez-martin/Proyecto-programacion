from numpy import array, dot, zeros 
from numpy.linalg import norm
from scipy.linalg import lu, lu_factor, lu_solve

#Gauss
def my_Gauss(A,b)
  n = len(b)   x = zeros(n)
  # Eliminación hacia adelante
  for k in range(n-1):
      for i in range(k+1, n):
          C = A[i,k] / A[k,k]
          A[i,k:] = A[i,k:] - C * A[k,k:]
          b[i] = b[i] - C * b[k]
  # Sustitución hacia atrás
  for i in range(n-1, -1, -1):
       x[i] = (b[i] - dot(A[i,i+1:], x[i+1:])) / A[i,i]
  return x

#Factorización LU
def LU(A,b):
    lu, piv = lu_factor(A)
    x = lu_solve((lu, piv), b)
    return x

#Jacobi
def my_Jacobi(A, b): 
    N = len(b)
    x, D, R = zeros(N), zeros(N), zeros((N,N))
    xn = 1 + x 
    tolerance = 1e-10
    k, max_iter = 0, 100
  #Iteración
    for i in range(N): 
        for j in range(N): 
            if i == j: 
                D[i] = A[i,j]
                R[i,j] = 0 
            else:
                R[i,j] = A[i,j]
   
    while norm(xn - x) > tolerance and k < max_iter: 
        x = xn
        xn = (b - dot(R, x)) / D
        k += 1                    

    return xn
# Jacobi no resuelve esta matriz porque no converge en este caso, ya que no es diagonalmente dominante. 
# Donde el valor absoluto de la diagonal principal es menor que la suma de los valores absolutos de los otros elementos en la fila.

def my_Gauss_Seidel(A, b):

    N = len(b)
    x1, x2, b1 = zeros(N), zeros(N), zeros(N)
    Error, tolerance = 1, 1e-10 
    k, max_iter = 0, 100
    #Iteracion
    while Error > tolerance  and  k < max_iter: 

        x1[:] = x2[:] 
        for i in range(N):
            b1[i] = b[i] - dot( A[i, i+1:], x1[i+1:] )

        for i in range(N):
            x2[i]  = ( b1[i] - dot( A[i, :i], x2[:i] ) )/ A[i, i] 
         
        Error = norm(x2-x1)
        k += 1
    return x2
#Gauss Seidel no funciona por el mismo motivo que el Jacobi, no tiene una diagonal principal dominante.
