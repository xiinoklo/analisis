# ================================================
# Experimento de tiempos - estilo inspirado en R/ggplot2
# Problema "Feliz Cumpleaños :D"
#
# Genera 4 gráficos:
#   1) tiempos_lineal.png
#   2) tiempos_loglog.png
#   3) ratio_hash_array.png
#   4) tiempos_normalizados.png
# ================================================

import random
import time
from typing import List

import matplotlib.pyplot as plt
import matplotlib as mpl

from torta_dp import max_satisfaccion_array, max_satisfaccion_hash

# --------- Estilo tipo ggplot2 ---------
# Fondo gris suave, grilla blanca, texto claro
plt.style.use("default")

mpl.rcParams["figure.figsize"] = (7, 5)
mpl.rcParams["axes.titlesize"] = 14
mpl.rcParams["axes.labelsize"] = 12
mpl.rcParams["legend.fontsize"] = 11
mpl.rcParams["xtick.labelsize"] = 10
mpl.rcParams["ytick.labelsize"] = 10
mpl.rcParams["axes.facecolor"] = "#E5E5E5"     # gris claro (panel)
mpl.rcParams["figure.facecolor"] = "white"     # fondo blanco
mpl.rcParams["grid.color"] = "white"          # grilla blanca
mpl.rcParams["grid.linestyle"] = "-"          # líneas sólidas
mpl.rcParams["grid.linewidth"] = 0.8
mpl.rcParams["axes.edgecolor"] = "#888888"    # borde gris
mpl.rcParams["axes.grid"] = True              # activar grilla


# ----------------- Utilidades -------------------

def generar_instancia(n: int, low: int = -10, high: int = 10) -> List[int]:
    """Genera una instancia aleatoria de 2n porciones."""
    return [random.randint(low, high) for _ in range(2 * n)]


def medir_tiempo(func, values: List[int], repeticiones: int = 1) -> float:
    """Tiempo promedio (segundos) de ejecutar func(values)."""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        func(values)
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones


# ----------------- Gráficos ---------------------

def graficar_tiempos(n_values, tiempos_array, tiempos_hash) -> None:
    # 1) Escala lineal
    fig, ax = plt.subplots()
    ax.plot(n_values, tiempos_array,
            marker="o", linestyle="-", linewidth=2,
            label="Memo en arreglos")
    ax.plot(n_values, tiempos_hash,
            marker="s", linestyle="-", linewidth=2,
            label="Memo en hash")
    ax.set_xlabel("n (la torta tiene 2n porciones)")
    ax.set_ylabel("Tiempo promedio (segundos)")
    ax.set_title("Comparación de tiempos (escala lineal)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig("tiempos_lineal.png", dpi=200)

    # 2) Escala log–log
    fig, ax = plt.subplots()
    ax.loglog(n_values, tiempos_array,
              marker="o", linestyle="-", linewidth=2,
              label="Memo en arreglos")
    ax.loglog(n_values, tiempos_hash,
              marker="s", linestyle="-", linewidth=2,
              label="Memo en hash")
    ax.set_xlabel("n (escala log)")
    ax.set_ylabel("Tiempo (segundos, escala log)")
    ax.set_title("Tiempos en escala log–log")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig("tiempos_loglog.png", dpi=200)

    # 3) Ratio hash / array
    ratios = []
    for t_arr, t_hash in zip(tiempos_array, tiempos_hash):
        ratios.append(t_hash / t_arr if t_arr > 0 else float("nan"))

    fig, ax = plt.subplots()
    ax.plot(n_values, ratios,
            marker="o", linestyle="-", linewidth=2)
    ax.axhline(1.0, linestyle="--", linewidth=1.5, color="#444444")
    ax.set_xlabel("n (la torta tiene 2n porciones)")
    ax.set_ylabel("ratio tiempo_hash / tiempo_array")
    ax.set_title("Relación de tiempos: hash vs arreglos")
    fig.tight_layout()
    fig.savefig("ratio_hash_array.png", dpi=200)

    # 4) Tiempos normalizados por n^3
    norm_array = [t_arr / (n ** 3) for n, t_arr in zip(n_values, tiempos_array)]
    norm_hash = [t_hash / (n ** 3) for n, t_hash in zip(n_values, tiempos_hash)]

    fig, ax = plt.subplots()
    ax.plot(n_values, norm_array,
            marker="o", linestyle="-", linewidth=2,
            label="Arreglos / n³")
    ax.plot(n_values, norm_hash,
            marker="s", linestyle="-", linewidth=2,
            label="Hash / n³")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo / n³")
    ax.set_title("Tiempos normalizados por n³")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig("tiempos_normalizados.png", dpi=200)


# --------------- Experimento principal ----------

def experimento_tiempos() -> None:
    random.seed(0)

    # Ajusta n según lo que aguante tu PC
    n_values = [4, 6, 8, 10, 12, 14]
    repeticiones = 3

    tiempos_array = []
    tiempos_hash = []

    for n in n_values:
        print(f"n = {n} (2n = {2*n} porciones)")
        vals = generar_instancia(n)

        t_arr = medir_tiempo(max_satisfaccion_array, vals, repeticiones)
        t_hash = medir_tiempo(max_satisfaccion_hash, vals, repeticiones)

        tiempos_array.append(t_arr)
        tiempos_hash.append(t_hash)

        print(f"  arreglo: {t_arr:.6f} s")
        print(f"  hash   : {t_hash:.6f} s")

    graficar_tiempos(n_values, tiempos_array, tiempos_hash)
    print("Gráficos generados:")
    print("  tiempos_lineal.png")
    print("  tiempos_loglog.png")
    print("  ratio_hash_array.png")
    print("  tiempos_normalizados.png")


if __name__ == "__main__":
    experimento_tiempos()
