
# FUNCIONES HECHAS MANUALMENTE (my functions)

# Observaciones:
    # 1. Hay ciertas variables que se repiten en diferentes funciones, por lo que es importante copiar
    #    las funciones INDIVIDUALMENTE para evitar que se utilice la misma variable dos veces.
   
     
    # 2. En todas o casi todas las funciones he implementado sistemas de detección y aviso de errores 
    #    (raise ValueError). Sin embargo, al implementar el slider que nos pide el profe, es posible que 
    #    haya que especificar las condiciones de entrada (tamaños de matrices, filas o columnas no iguales
    #    a 0...), por lo que si esto ocurre, SE DEBERÁN ELIMINAR estos sistemas de errores, o al menos
    #    aquellos que respondan a errores ya resueltos con las especificaciones del slider, pues resultarían 
    #    redundantes y sumarían líneas de código adicionales.


    # 3. Además de los sistemas de detección y aviso de errores, también he implementado ciertos inputs. Al
    #    implementar el slider, estos inputs SE DEBERÁN ELIMINAR, pues el propio slider ya introuce los
    #    valores que se deseen.



# 1) BALANCE DE MASAS

    #I) my_linalg_solve

def my_linalg_solve(A, b):
    n = len(A)

    if n == 0 or len(b) != n:
        raise ValueError("Dimensiones incompatibles")

    # Construcción de la matriz aumentada [A | b], sin modificar las entradas.
    M = []
    for i in range(n):
        if len(A[i]) != n:
            raise ValueError("A debe ser cuadrada")

        row = []
        for j in range(n):
            row.append(float(A[i][j]))
        row.append(float(b[i]))
        M.append(row)

    # Eliminación de Gauss, con pivoteo parcial.
    for k in range(n):
        pivot = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[pivot][k]):
                pivot = i

        if M[pivot][k] == 0:
            raise ValueError("El sistema no tiene solución única")

        M[k], M[pivot] = M[pivot], M[k]

        for i in range(k + 1, n):
            factor = M[i][k] / M[k][k]
            M[i][k] = 0.0

            for j in range(k + 1, n + 1):
                M[i][j] -= factor * M[k][j]

    # Sustitución hacia atrás.
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum = M[i][n]
        for j in range(i + 1, n):
            sum -= M[i][j] * x[j]
        x[i] = sum / M[i][i]

    return x



# 2) CALIBRACIÓN DEL MOTOR

    # I) my_regression

def my_regression(A, b):
    rows = len(A)

    if rows == 0 or len(b) != rows:
        raise ValueError("Dimensiones incompatibles")

    columns = len(A[0])
    if columns == 0:
        raise ValueError("A debe tener al menos una columna")

    for row in A:
        if len(row) != columns:
            raise ValueError("Todas las filas de A deben tener la misma longitud")

    # Construición de la matriz aumentada de (A(traspuesta)A)x = A(traspuesta)b.
    M = [[0.0 for _ in range(columns + 1)] for _ in range(columns)]

    for i in range(columns):
        for j in range(columns):
            for k in range(rows):
                M[i][j] += A[k][i] * A[k][j]

        for k in range(rows):
            M[i][columns] += A[k][i] * b[k]

    # Eliminación de Gauss con pivoteo parcial.
    for k in range(columns):
        pivot = k
        for i in range(k + 1, columns):
            if abs(M[i][k]) > abs(M[pivot][k]):
                pivot = i

        if M[pivot][k] == 0:
            raise ValueError("No hay una solución única")

        M[k], M[pivot] = M[pivot], M[k]

        for i in range(k + 1, columns):
            factor = M[i][k] / M[k][k]
            for j in range(k, columns + 1):
                M[i][j] -= factor * M[k][j]

    # Sustitución hacia atrás.
    x = [0.0] * columns
    for i in range(columns - 1, -1, -1):
        sum = M[i][columns]
        for j in range(i + 1, columns):
            sum -= M[i][j] * x[j]
        x[i] = sum / M[i][i]

    return x


#3) PERFIL ATMOSFÉRICO

    # I) my_interpolation

from numpy import array, linspace

t_flight = linspace(0, 60, 1200)

def altitude(t):
    return 300 * t

def my_interpolation(h, heights, temperatures):
    if len(heights) != len(temperatures):
        raise ValueError("Debe haber una temperatura para cada altura")

    # Mantiene el comportamiento de numpy.interp fuera de la tabla:
    # usa la temperatura del extremo más cercano.

    # No sé si esta parte es necesaria: ¿fuera del rango de alturas se mantiene igual, o simplemente
    # introducimos un error que diga que h no puede salir del rango dado?
    if h <= heights[0]:
        return temperatures[0]
    if h >= heights[-1]:
        return temperatures[-1]

    for i in range(len(heights) - 1):
        h0 = heights[i]
        h1 = heights[i + 1]

        if h0 <= h <= h1:
            T0 = temperatures[i]
            T1 = temperatures[i + 1]
            return T0 + (T1 - T0) * (h - h0) / (h1 - h0)

    raise ValueError("No hay un intervalo para esa altura")


h_atm = array([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000])
T_atm = array([288.15, 275.15, 262.15, 249.15,
               236.15, 223.15, 216.65, 216.65])

h_flight = altitude(t_flight)
T_flight = [
    my_interpolation(h, h_atm, T_atm)
    for h in h_flight
]

t = float(input("Tiempo de vuelo en segundos: "))
T = my_interpolation(altitude(t), h_atm, T_atm)

print("Temperatura:", T, "K")