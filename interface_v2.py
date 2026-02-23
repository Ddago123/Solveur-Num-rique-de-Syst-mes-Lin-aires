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


def validate_dimensions(A, b, x0):
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matrice A doit être carrée.")
    if len(b) != A.shape[0]:
        raise ValueError("Dimension incompatible entre A et b.")
    if len(x0) != A.shape[0]:
        raise ValueError("Dimension incompatible entre A et x0.")


def solve():
    try:
        A = parse_matrix(matrix_text.get("1.0", tk.END))
        b = parse_vector(vector_entry.get())
        x0 = parse_vector(x0_entry.get())

        validate_dimensions(A, b, x0)

        tol = float(tol_entry.get())
        max_iter = int(iter_entry.get())
        method = method_var.get()

        status_var.set("Calcul en cours...")

        if method == "Jacobi":
            result = jacobi(A, b, x0, tol, max_iter)

        elif method == "Gauss-Seidel":
            result = gauss_seidel(A, b, x0, tol, max_iter)

        elif method == "Relaxation":
            omega = float(omega_entry.get())
            result = relaxation(A, b, x0, omega, tol, max_iter)

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, f"Solution trouvée :\n\n{np.round(result, 6)}")

        status_var.set("Calcul terminé avec succès ✔")

    except Exception as e:
        status_var.set("Erreur ❌")
        messagebox.showerror("Erreur", str(e))


def reset_fields():
    matrix_text.delete("1.0", tk.END)
    vector_entry.delete(0, tk.END)
    x0_entry.delete(0, tk.END)
    result_box.delete("1.0", tk.END)
    status_var.set("Prêt")


def toggle_omega(event=None):
    if method_var.get() == "Relaxation":
        omega_entry.config(state="normal")
    else:
        omega_entry.config(state="disabled")


# ================= INTERFACE =================

root = tk.Tk()
root.title("Solveur Numérique Avancé")
root.geometry("500x700")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")

# Couleurs personnalisées
BG_COLOR = "#1e1e2f"
FRAME_COLOR = "#2c2f4a"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4CAF50"

# ===== Titre =====
title = tk.Label(root,
                 text="Solveur de Systèmes Linéaires",
                 font=("Segoe UI", 20, "bold"),
                 bg=BG_COLOR,
                 fg=TEXT_COLOR)
title.pack(pady=15)

# ===== Frame principale =====
main_frame = tk.Frame(root, bg=FRAME_COLOR, bd=2, relief="ridge")
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

# ===== Matrice A =====
tk.Label(main_frame, text="Matrice A", bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=(10, 0))
matrix_text = tk.Text(main_frame, height=5, width=45, bg="#3b3f5c", fg="white")
matrix_text.pack(pady=5)

# ===== Vecteur b =====
tk.Label(main_frame, text="Vecteur b", bg=FRAME_COLOR, fg=TEXT_COLOR).pack()
vector_entry = tk.Entry(main_frame, width=45, bg="#3b3f5c", fg="white")
vector_entry.pack(pady=5)

# ===== x0 =====
tk.Label(main_frame, text="Vecteur initial x0", bg=FRAME_COLOR, fg=TEXT_COLOR).pack()
x0_entry = tk.Entry(main_frame, width=45, bg="#3b3f5c", fg="white")
x0_entry.pack(pady=5)

# ===== Paramètres =====
param_frame = tk.Frame(main_frame, bg=FRAME_COLOR)
param_frame.pack(pady=10)

tk.Label(param_frame, text="Tolérance", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)
tol_entry = tk.Entry(param_frame, width=10)
tol_entry.insert(0, "1e-6")
tol_entry.grid(row=1, column=0, padx=5)

tk.Label(param_frame, text="Max itérations", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=1, padx=5)
iter_entry = tk.Entry(param_frame, width=10)
iter_entry.insert(0, "100")
iter_entry.grid(row=1, column=1, padx=5)

tk.Label(param_frame, text="Omega", bg=FRAME_COLOR, fg=TEXT_COLOR).grid(row=0, column=2, padx=5)
omega_entry = tk.Entry(param_frame, width=10)
omega_entry.insert(0, "1.1")
omega_entry.grid(row=1, column=2, padx=5)

# ===== Méthode =====
tk.Label(main_frame, text="Méthode", bg=FRAME_COLOR, fg=TEXT_COLOR).pack()
method_var = tk.StringVar(value="Jacobi")
method_menu = ttk.Combobox(main_frame,
                           textvariable=method_var,
                           values=["Jacobi", "Gauss-Seidel", "Relaxation"],
                           state="readonly")
method_menu.pack(pady=5)
method_menu.bind("<<ComboboxSelected>>", toggle_omega)

toggle_omega()

# ===== Boutons =====
button_frame = tk.Frame(main_frame, bg=FRAME_COLOR)
button_frame.pack(pady=15)

solve_btn = tk.Button(button_frame,
                      text="Résoudre",
                      bg=ACCENT_COLOR,
                      fg="white",
                      width=15,
                      command=solve)
solve_btn.grid(row=0, column=0, padx=10)

reset_btn = tk.Button(button_frame,
                      text="Réinitialiser",
                      bg="#e74c3c",
                      fg="white",
                      width=15,
                      command=reset_fields)
reset_btn.grid(row=0, column=1, padx=10)

# ===== Zone Résultat =====
tk.Label(main_frame, text="Résultat", bg=FRAME_COLOR, fg=TEXT_COLOR).pack()
result_box = tk.Text(main_frame, height=6, width=45, bg="#3b3f5c", fg="#00ffae")
result_box.pack(pady=5)

# ===== Barre de statut =====
status_var = tk.StringVar(value="Prêt")
status_bar = tk.Label(root,
                      textvariable=status_var,
                      bg="#151522",
                      fg="white",
                      anchor="w")
status_bar.pack(fill="x")

root.mainloop()