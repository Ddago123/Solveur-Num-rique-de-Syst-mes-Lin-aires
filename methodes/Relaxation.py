import numpy as np

def relaxation(A, b, x0, omega, tol=1e-6, max_iter=100):
    """
    Résout Ax = b par la méthode SOR.
    
    omega : paramètre de relaxation
    """

    n = len(b)
    x = x0.copy()

    for k in range(max_iter):

        x_old = x.copy()

        for i in range(n):

            # Partie inférieure (valeurs nouvelles)
            s1 = sum(A[i][j] * x[j] for j in range(i))

            # Partie supérieure (anciennes valeurs)
            s2 = sum(A[i][j] * x_old[j] for j in range(i+1, n))

            # Valeur Gauss-Seidel temporaire
            gs_value = (b[i] - s1 - s2) / A[i][i]

            # Relaxation
            x[i] = (1 - omega) * x_old[i] + omega * gs_value

        # Test convergence
        if np.linalg.norm( np.dot(A, x) - b) < tol:
            print(f"Convergence atteinte en {k+1} itérations")
            return x

    print("Nombre max d'itérations atteint")
    return x