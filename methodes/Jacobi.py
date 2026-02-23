import numpy as np

def jacobi(A, b, x0, tol=1e-6, max_iter=100):
    """
    Résout Ax = b par la méthode de Jacobi.
    
    A : matrice carrée (numpy array)
    b : vecteur second membre
    x0 : approximation initiale
    tol : tolérance d'arrêt
    max_iter : nombre maximal d'itérations
    """

    n = len(b)
    x = x0.copy()
    x_new = np.zeros_like(x)

    for k in range(max_iter):
        
        # Calcul de chaque composante
        for i in range(n):
            # Somme des termes hors diagonale
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            
            # Formule de Jacobi
            x_new[i] = (b[i] - s) / A[i][i]

        # Test de convergence (norme du résidu)
        if np.linalg.norm( np.dot(A, x_new) - b) < tol:
            print(f"Convergence atteinte en {k+1} itérations")
            return x_new

        x = x_new.copy()

    print("Nombre max d'itérations atteint")
    return x