
from methodes.Jacobi import jacobi
from methodes.Gauss_Seidel import gauss_seidel
from methodes.Relaxation import relaxation
import numpy as np

A = np.array([[4, 1],
              [1, 3]], dtype=float)

b = np.array([9, 6], dtype=float)

x0 = np.zeros(2)

print("Jacobi :", jacobi(A, b, x0))
print("Gauss-Seidel :", gauss_seidel(A, b, x0))
print("Relaxation :", relaxation(A, b, x0, omega=1.1))