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
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import List

# Importamos las funciones de solución desde el módulo torta_dp
# Asegurarse de que torta_dp.py esté en el mismo directorio
from torta_dp import max_satisfaccion_array, max_satisfaccion_hash

# ================================================
# EXPERIMENTO DE TIEMPOS - ESTILO R/GGPLOT2
# ================================================

# Configuración estética global para gráficos profesionales
plt.style.use("default")
mpl.rcParams["figure.figsize"] = (8, 6)
mpl.rcParams["axes.facecolor"] = "#EBEBEB"  # Fondo gris estilo ggplot
mpl.rcParams["axes.grid"] = True
mpl.rcParams["grid.color"] = "white"
mpl.rcParams["grid.linewidth"] = 1.0
mpl.rcParams["axes.edgecolor"] = "#333333"
mpl.rcParams["lines.linewidth"] = 2
mpl.rcParams["font.size"] = 10
mpl.rcParams["axes.labelsize"] = 11
mpl.rcParams["axes.titlesize"] = 13

def generar_instancia(n: int, low: int = -10, high: int = 10) -> List[int]:
    """
    Genera una instancia aleatoria de la torta.
    Retorna una lista de 2*n enteros.
    """
    return [random.randint(low, high) for _ in range(2 * n)]

def medir_tiempo(func, values: List[int], repeticiones: int = 3) -> float:
    """
    Ejecuta 'func(values)' un número de 'repeticiones' y retorna el promedio.
    Utiliza time.perf_counter() para medir tiempo de CPU/Wall-clock con alta precisión.
    """
    tiempos =
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        func(values)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return sum(tiempos) / len(tiempos)

def graficar_tiempos(n_values, tiempos_array, tiempos_hash):
    """Genera y guarda los 4 gráficos solicitados en el informe."""
    
    # 1. Gráfico Lineal: Comparación Directa
    fig, ax = plt.subplots()
    ax.plot(n_values, tiempos_array, 'o-', label='Memo Array', color='#E24A33')
    ax.plot(n_values, tiempos_hash, 's-', label='Memo Hash', color='#348ABD')
    ax.set_title("Comparación de Tiempos: Array vs Hash (Escala Lineal)")
    ax.set_xlabel("n (La torta tiene 2n porciones)")
    ax.set_ylabel("Tiempo promedio (segundos)")
    ax.legend(facecolor='white', framealpha=1)
    fig.tight_layout()
    fig.savefig("tiempos_lineal.png", dpi=200)
    plt.close(fig)

    # 2. Gráfico Log-Log: Análisis de Orden de Crecimiento
    fig, ax = plt.subplots()
    ax.loglog(n_values, tiempos_array, 'o-', label='Memo Array', color='#E24A33')
    ax.loglog(n_values, tiempos_hash, 's-', label='Memo Hash', color='#348ABD')
    ax.set_title("Comparación de Tiempos (Escala Log-Log)")
    ax.set_xlabel("n (Escala Log)")
    ax.set_ylabel("Tiempo (segundos, Escala Log)")
    ax.legend(facecolor='white', framealpha=1)
    fig.tight_layout()
    fig.savefig("tiempos_loglog.png", dpi=200)
    plt.close(fig)

    # 3. Ratio Hash/Array: Factor Constante de Overhead
    ratios =
    for t_h, t_a in zip(tiempos_hash, tiempos_array):
        if t_a > 1e-9: # Evitar división por cero
            ratios.append(t_h / t_a)
        else:
            ratios.append(1.0) 

    fig, ax = plt.subplots()
    ax.plot(n_values, ratios, 'o-', color='#8EBA42')
    ax.axhline(1.0, color='black', linestyle='--', alpha=0.5)
    ax.set_title("Ratio de Rendimiento: Tiempo Hash / Tiempo Array")
    ax.set_xlabel("n")
    ax.set_ylabel("Ratio (Hash / Array)")
    # Anotación del último valor para claridad
    if ratios:
        ax.text(n_values[-1], ratios[-1], f"{ratios[-1]:.2f}x", va='bottom', ha='right', fontweight='bold')
    fig.tight_layout()
    fig.savefig("ratio_hash_array.png", dpi=200)
    plt.close(fig)

    # 4. Normalización por n^3: Validación de Complejidad
    # Si T ~ k * n^3, entonces T / n^3 ~ k (constante)
    norm_array = [t / (n**3) for t, n in zip(tiempos_array, n_values)]
    norm_hash = [t / (n**3) for t, n in zip(tiempos_hash, n_values)]

    fig, ax = plt.subplots()
    ax.plot(n_values, norm_array, 'o-', label='Array / n³', color='#E24A33')
    ax.plot(n_values, norm_hash, 's-', label='Hash / n³', color='#348ABD')
    ax.set_title("Tiempos Normalizados por Complejidad Teórica O(n³)")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo / n³")
    ax.legend(facecolor='white', framealpha=1)
    fig.tight_layout()
    fig.savefig("tiempos_normalizados.png", dpi=200)
    plt.close(fig)

def experimento_tiempos():
    # Semilla fija para reproducibilidad científica
    random.seed(42)
    
    # Valores de n seleccionados para mostrar la curva de crecimiento.
    # Dado O(n^3), n=100 implica ~1 millón de operaciones base.
    # n=100 es razonable para una ejecución de segundos.
    n_values = 
    
    tiempos_array =
    tiempos_hash =

    print(f"{'n':<5} | {'2n':<5} | {'T_Array (s)':<12} | {'T_Hash (s)':<12}")
    print("-" * 45)

    for n in n_values:
        # Generar instancia única para ambos métodos para comparación justa
        instancia = generar_instancia(n)
        
        # Medición Array
        t_arr = medir_tiempo(max_satisfaccion_array, instancia, repeticiones=3)
        tiempos_array.append(t_arr)
        
        # Medición Hash
        t_hash = medir_tiempo(max_satisfaccion_hash, instancia, repeticiones=3)
        tiempos_hash.append(t_hash)
        
        print(f"{n:<5} | {2*n:<5} | {t_arr:<12.5f} | {t_hash:<12.5f}")

    print("\nGenerando visualizaciones...")
    graficar_tiempos(n_values, tiempos_array, tiempos_hash)
    print("Proceso completado. Se han generado 4 archivos.png con los resultados.")
    print("  - tiempos_lineal.png")
    print("  - tiempos_loglog.png")
    print("  - ratio_hash_array.png")
    print("  - tiempos_normalizados.png")

if __name__ == "__main__":
    experimento_tiempos()

if __name__ == "__main__":
    experimento_tiempos()
