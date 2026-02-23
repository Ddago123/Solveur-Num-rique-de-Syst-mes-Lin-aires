import numpy as np

def gauss_seidel(A, b, x0, tol=1e-6, max_iter=100):
    """
    Résout Ax = b par la méthode de Gauss-Seidel.
    """

    n = len(b)
    x = x0.copy()

    for k in range(max_iter):

        x_old = x.copy()

        for i in range(n):

            # Somme partie inférieure (nouvelles valeurs)
            s1 = sum(A[i][j] * x[j] for j in range(i))

            # Somme partie supérieure (anciennes valeurs)
            s2 = sum(A[i][j] * x_old[j] for j in range(i+1, n))

            # Formule Gauss-Seidel
            x[i] = (b[i] - s1 - s2) / A[i][i]

        # Test convergence
        if np.linalg.norm( np.dot(A, x) - b) < tol:
            print(f"Convergence atteinte en {k+1} itérations")
            return x

    print("Nombre max d'itérations atteint")
    return x