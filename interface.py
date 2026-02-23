import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from methodes.Jacobi import jacobi
from methodes.Gauss_Seidel import gauss_seidel
from methodes.Relaxation import relaxation 

# ================= UTILITAIRES =================

def parse_matrix(text):
    rows = text.strip().split("\n")
    matrix = [list(map(float, row.split())) for row in rows]
    return np.array(matrix)


def parse_vector(text):
    return np.array(list(map(float, text.strip().split())))


def solve():
    try:
        A = parse_matrix(matrix_text.get("1.0", tk.END))
        b = parse_vector(vector_entry.get())
        x0 = parse_vector(x0_entry.get())

        tol = float(tol_entry.get())
        max_iter = int(iter_entry.get())
        method = method_var.get()

        if method == "Jacobi":
            result = jacobi(A, b, x0, tol, max_iter)

        elif method == "Gauss-Seidel":
            result = gauss_seidel(A, b, x0, tol, max_iter)

        elif method == "Relaxation":
            omega = float(omega_entry.get())
            result = relaxation(A, b, x0, omega, tol, max_iter)

        result_var.set(f"Solution : {np.round(result, 6)}")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# ================= INTERFACE =================

root = tk.Tk()
root.title("Solveur Numérique - Jacobi | GS | Relaxation")
root.geometry("370x550")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

# ===== Titre =====
title = tk.Label(root,
                 text="Solveur de Systèmes Linéaires",
                 font=("Helvetica", 18, "bold"),
                 bg="#f4f6f9",
                 fg="#2c3e50")
title.pack(pady=15)

# ===== Frame principale =====
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# ===== Matrice A =====
ttk.Label(main_frame, text="Matrice A (ligne par ligne)").grid(row=0, column=0, sticky="w")
matrix_text = tk.Text(main_frame, height=5, width=40)
matrix_text.grid(row=1, column=0, columnspan=2, pady=5)

# ===== Vecteur b =====
ttk.Label(main_frame, text="Vecteur b").grid(row=2, column=0, sticky="w")
vector_entry = ttk.Entry(main_frame, width=40)
vector_entry.grid(row=3, column=0, columnspan=2, pady=5)

# ===== x0 =====
ttk.Label(main_frame, text="Vecteur initial x0").grid(row=4, column=0, sticky="w")
x0_entry = ttk.Entry(main_frame, width=40)
x0_entry.grid(row=5, column=0, columnspan=2, pady=5)

# ===== Paramètres =====
ttk.Label(main_frame, text="Tolérance").grid(row=6, column=0, sticky="w")
tol_entry = ttk.Entry(main_frame)
tol_entry.insert(0, "1e-6")
tol_entry.grid(row=7, column=0, pady=5)

ttk.Label(main_frame, text="Max itérations").grid(row=6, column=1, sticky="w")
iter_entry = ttk.Entry(main_frame)
iter_entry.insert(0, "100")
iter_entry.grid(row=7, column=1, pady=5)

# ===== Méthode =====
ttk.Label(main_frame, text="Méthode").grid(row=8, column=0, sticky="w")
method_var = tk.StringVar(value="Jacobi")
method_menu = ttk.Combobox(main_frame,
                           textvariable=method_var,
                           values=["Jacobi", "Gauss-Seidel", "Relaxation"],
                           state="readonly")
method_menu.grid(row=9, column=0, pady=5)

# ===== Omega =====
ttk.Label(main_frame, text="Omega (pour SOR)").grid(row=8, column=1, sticky="w")
omega_entry = ttk.Entry(main_frame)
omega_entry.insert(0, "1.1")
omega_entry.grid(row=9, column=1, pady=5)

# ===== Bouton =====
solve_button = ttk.Button(main_frame,
                          text="Résoudre",
                          command=solve)
solve_button.grid(row=10, column=0, columnspan=2, pady=20)

# ===== Résultat =====
result_var = tk.StringVar()
result_label = tk.Label(root,
                        textvariable=result_var,
                        font=("Helvetica", 12, "bold"),
                        bg="#f4f6f9",
                        fg="#27ae60")
result_label.pack(pady=10)

root.mainloop()