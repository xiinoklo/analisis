# ================================================
# Trabajo: Análisis y Diseño de Algoritmos
# Problema "Feliz Cumpleaños :D"
#
# Solución por Programación Dinámica (minimax)
# - max_satisfaccion_array: memo en arreglos
# - max_satisfaccion_hash:  memo en tablas de hash
#
# Este archivo está listo para ejecución interactiva.
# ================================================

from typing import List, Dict, Tuple

INF_POS = 10**18
INF_NEG = -10**18


# ------------------------------------------------
# Utilidades comunes
# ------------------------------------------------

def construir_arreglo_extendido(values: List[int]) -> List[int]:
    """Dado v[0..2n-1], construye w[0..4n-1] repitiendo v dos veces."""
    return values * 2


def prefix_sums(arr: List[int]) -> List[int]:
    """Crea arreglo de sumas prefixadas: pref[i] = suma arr[0..i-1]."""
    n = len(arr)
    pref = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += arr[i]
        pref[i + 1] = s
    return pref


def rango_suma(pref: List[int], a: int, b: int) -> int:
    """Retorna sum(arr[a..b]) usando prefix sums."""
    return pref[b + 1] - pref[a]


# =====================================================
# 1) DP CON MEMOIZACIÓN EN ARREGLOS (LISTAS)
# =====================================================

def dp_array(
    w: List[int],
    pref: List[int],
    n: int,
    start: int,
    length: int,
    turn: int,
    memo: List[List[List[int]]],
    visitado: List[List[List[bool]]],
) -> int:
    """DP con memoización en arreglos: F(start, length, turn)."""

    if visitado[start][length][turn]:
        return memo[start][length][turn]

    visitado[start][length][turn] = True

    # Caso base
    if length == 1:
        if turn == 0:
            res = w[start]
        else:
            res = 0
        memo[start][length][turn] = res
        return res

    i = start
    L = length

    if turn == 0:
        # Turno profesor: maximiza
        mejor = INF_NEG

        # Jugadas válidas: comer prefijo o sufijo de tamaño s
        for s in range(1, L):
            # Profesor come prefijo [i .. i+s-1]
            gain_pref = rango_suma(pref, i, i + s - 1)
            val_pref = gain_pref + dp_array(
                w, pref, n,
                i + s,
                L - s,
                1,
                memo,
                visitado,
            )
            if val_pref > mejor:
                mejor = val_pref

            # Profesor come sufijo [i+L-s .. i+L-1]
            inicio_suf = i + L - s
            gain_suf = rango_suma(pref, inicio_suf, i + L - 1)
            val_suf = gain_suf + dp_array(
                w, pref, n,
                i,
                L - s,
                1,
                memo,
                visitado,
            )
            if val_suf > mejor:
                mejor = val_suf

        memo[start][length][turn] = mejor
        return mejor

    else:
        # Turno hermana: minimiza
        peor = INF_POS

        for s in range(1, L):
            # Hermana come prefijo
            val_pref = dp_array(
                w, pref, n,
                i + s,
                L - s,
                0,
                memo,
                visitado,
            )
            if val_pref < peor:
                peor = val_pref

            # Hermana come sufijo
            val_suf = dp_array(
                w, pref, n,
                i,
                L - s,
                0,
                memo,
                visitado,
            )
            if val_suf < peor:
                peor = val_suf

        memo[start][length][turn] = peor
        return peor


def max_satisfaccion_array(values: List[int]) -> int:
    """DP con memoización en arreglos."""
    m = len(values)
    assert m % 2 == 0, "La cantidad de porciones debe ser 2n."
    n = m // 2

    w = construir_arreglo_extendido(values)  # largo = 4n
    pref = prefix_sums(w)

    tamaño_i = len(w)
    memo = [[[0 for _ in range(2)] for _ in range(n + 1)] for _ in range(tamaño_i)]
    visitado = [[[False for _ in range(2)] for _ in range(n + 1)] for _ in range(tamaño_i)]

    mejor_global = INF_NEG

    # Primera jugada del profesor: elegir semicircunferencia
    for k in range(2 * n):
        # Ganancia inmediata
        gain0 = sum(values[(k + t) % (2 * n)] for t in range(n))

        # Intervalo restante
        inicio_restante = k + n
        valor_restante = dp_array(
            w, pref, n,
            inicio_restante,
            n,
            1,
            memo,
            visitado,
        )

        total_k = gain0 + valor_restante
        if total_k > mejor_global:
            mejor_global = total_k

    return mejor_global


# =====================================================
# 2) DP CON MEMOIZACIÓN EN TABLAS DE HASH (dict)
# =====================================================

def dp_hash(
    w: List[int],
    pref: List[int],
    n: int,
    start: int,
    length: int,
    turn: int,
    memo: Dict[Tuple[int, int, int], int],
) -> int:
    """DP con memoización en diccionario: F(start, length, turn)."""

    key = (start, length, turn)
    if key in memo:
        return memo[key]

    # Caso base
    if length == 1:
        res = w[start] if turn == 0 else 0
        memo[key] = res
        return res

    i = start
    L = length

    if turn == 0:
        mejor = INF_NEG
        for s in range(1, L):
            gain_pref = rango_suma(pref, i, i + s - 1)
            val_pref = gain_pref + dp_hash(
                w, pref, n,
                i + s,
                L - s,
                1,
                memo,
            )
            mejor = max(mejor, val_pref)

            inicio_suf = i + L - s
            gain_suf = rango_suma(pref, inicio_suf, i + L - 1)
            val_suf = gain_suf + dp_hash(
                w, pref, n,
                i,
                L - s,
                1,
                memo,
            )
            mejor = max(mejor, val_suf)

        memo[key] = mejor
        return mejor

    else:
        peor = INF_POS
        for s in range(1, L):
            val_pref = dp_hash(
                w, pref, n,
                i + s,
                L - s,
                0,
                memo,
            )
            peor = min(peor, val_pref)

            val_suf = dp_hash(
                w, pref, n,
                i,
                L - s,
                0,
                memo,
            )
            peor = min(peor, val_suf)

        memo[key] = peor
        return peor


def max_satisfaccion_hash(values: List[int]) -> int:
    """DP con memoización en diccionario (hash table)."""
    m = len(values)
    assert m % 2 == 0
    n = m // 2

    w = construir_arreglo_extendido(values)
    pref = prefix_sums(w)
    memo: Dict[Tuple[int, int, int], int] = {}

    mejor_global = INF_NEG

    for k in range(2 * n):
        gain0 = sum(values[(k + t) % (2 * n)] for t in range(n))

        inicio_restante = k + n
        valor_restante = dp_hash(
            w, pref, n,
            inicio_restante,
            n,
            1,
            memo,
        )

        mejor_global = max(mejor_global, gain0 + valor_restante)

    return mejor_global


# =====================================================
# 3) main() INTERACTIVO (corregido)
# =====================================================

def main() -> None:
    print("=== Problema Feliz Cumpleaños :D ===")

    n = int(input("Ingresa n (habrá 2n porciones): ").strip())

    vals_str = input(
        f"Ingresa los {2*n} valores de satisfacción separados por espacio:\n"
    ).strip().split()

    if len(vals_str) != 2 * n:
        raise ValueError(f"Se esperaban {2*n} valores, pero llegaron {len(vals_str)}.")

    vals = list(map(int, vals_str))

    print("\nCalculando...\n")

    res_array = max_satisfaccion_array(vals)
    res_hash = max_satisfaccion_hash(vals)

    print("--- RESULTADOS ---")
    print("DP con arreglos:", res_array)
    print("DP con hash:    ", res_hash)


if __name__ == "__main__":
    main()
