"""
solucion_torta.py
===================

Este módulo contiene una solución completa al problema **Feliz
Cumpleaños :D** planteado en las tareas de la asignatura de
Análisis y Diseño de Algoritmos. Se implementan dos versiones
de programación dinámica para que el profesor maximice su
satisfacción al repartir una torta circular cortada en 2n
porciones.

### Descripción del problema

Se tiene una torta redonda dividida en 2n porciones iguales. El
profesor y su hermana se alternan turnos para elegir un ángulo
``αᵢ`` y comer todas las porciones que están en sentido contrario a
las agujas del reloj entre ``αᵢ`` y ``αᵢ + π``. Un ángulo es válido
siempre que queden porciones en ambos lados de la línea que pasa
por el centro. El profesor quiere garantizar que la suma de los
valores de las porciones que coma sea lo mayor posible, asumiendo
que su hermana juega de manera óptima para minimizar dicho total.

### Enfoque de programación dinámica

La estrategia de solución se basa en definir un subproblema
``F(start, length, turn)`` que representa la mejor suma de
satisfacción que el profesor puede asegurar en una partida donde
queda un segmento contiguo de ``length`` porciones de la torta,
comenzando en el índice ``start`` del arreglo extendido, y es el
turno del ``turn`` (0 para el profesor y 1 para la hermana).

Durante su turno el profesor puede comer un prefijo o un sufijo
de tamaño ``s`` (1 ≤ s < length). Al comer un prefijo recibe la suma
de esas porciones y el subproblema restante pasa a ser
``F(start+s, length-s, 1)``. Al comer un sufijo recibe la suma de las
porciones en el rango ``[start+length-s .. start+length-1]`` y el
subproblema pasa a ser ``F(start, length-s, 1)``. El profesor elige
la opción que maximice su total.

La hermana por su parte no obtiene valor de las porciones, pero
selecciona un prefijo o sufijo de tamaño ``s`` para minimizar
``F(start', length-s, 0)``. El caso base ocurre cuando
``length == 1``: si es el turno del profesor recibe el valor de la
única porción restante; si es el turno de la hermana, el profesor ya
no obtendrá más satisfacción.

Se usa un arreglo extendido duplicando las porciones para tratar
cómodamente la circularidad, y un arreglo de sumas prefijas para
obtener la suma de cualquier segmento en O(1). La primera jugada
del profesor consiste en escoger cualquier semicircunferencia de
``n`` porciones (hay 2n posibles posiciones), obtener su ganancia
inmediata, y resolver el subproblema en la mitad restante (``n``
porciones) con turno de la hermana.

Se implementan dos variantes de memoización: una usando listas
(arreglos) de tres dimensiones y otra usando un diccionario.

### Uso

Puede ejecutarse este módulo directamente para interactuar con el
usuario. También se pueden importar las funciones
``max_satisfaccion_array`` y ``max_satisfaccion_hash`` desde otras
partes del código o para pruebas unitarias.
"""

from typing import List, Dict, Tuple

# Valores extremos utilizados para inicializar las comparaciones
INF_POS = 10**18
INF_NEG = -10**18


def construir_arreglo_extendido(values: List[int]) -> List[int]:
    """Duplica la lista dada para manejar la torta de forma circular.

    Dado un arreglo de largo 2n, devuelve un arreglo de largo 4n
    que contiene dos copias consecutivas del mismo. Esto simplifica
    la obtención de subsecuencias que cruzan el final del círculo.

    Args:
        values: lista original de 2n enteros.

    Returns:
        Lista de 4n enteros con dos copias de ``values``.
    """
    return values * 2


def prefix_sums(arr: List[int]) -> List[int]:
    """Calcula las sumas prefijas de un arreglo.

    Se devuelve una lista ``pref`` tal que ``pref[i]`` es la suma de
    los primeros ``i`` elementos de ``arr``. De esta forma la suma
    de un segmento ``arr[a..b]`` puede obtenerse como ``pref[b+1] - pref[a]``.

    Args:
        arr: lista de enteros.

    Returns:
        Lista de enteros de largo ``len(arr) + 1`` con las sumas prefijas.
    """
    n = len(arr)
    pref = [0] * (n + 1)
    s = 0
    for i, val in enumerate(arr):
        s += val
        pref[i + 1] = s
    return pref


def rango_suma(pref: List[int], a: int, b: int) -> int:
    """Obtiene la suma de arr[a..b] usando las sumas prefijas.

    Args:
        pref: lista de sumas prefijas asociada al arreglo original.
        a: índice inicial (inclusive).
        b: índice final (inclusive).

    Returns:
        Suma de los elementos del arreglo original entre ``a`` y ``b``.
    """
    return pref[b + 1] - pref[a]


def max_satisfaccion_array(values: List[int]) -> int:
    """Versión con memoización en arreglos para el problema Feliz Cumpleaños.

    Implementa la función F(start, length, turn) con tres dimensiones
    de listas: una para el índice inicial del segmento, otra para la
    longitud y otra para el turno. El valor ``F(start, length, 0)``
    representa la máxima suma que el profesor puede asegurar a partir
    de un segmento de ``length`` porciones que comienza en ``start``
    cuando es su turno (turn=0). Para turn=1 representa la suma que el
    profesor obtendrá (posiblemente cero) cuando juega la hermana.

    Args:
        values: lista de 2n enteros que representan la satisfacción de
        cada porción de torta.

    Returns:
        Entero que indica la máxima suma de satisfacción que el
        profesor puede garantizar.
    """
    m = len(values)
    if m % 2 != 0:
        raise ValueError("La cantidad de porciones debe ser par (2n).")
    n = m // 2

    # Construir el arreglo extendido y las sumas prefijas
    w = construir_arreglo_extendido(values)
    pref = prefix_sums(w)

    # Estructuras de memoización en arreglos
    tam_i = len(w)
    # memo[start][length][turn] guardará el valor de F(start,length,turn)
    memo = [[[0] * 2 for _ in range(n + 1)] for _ in range(tam_i)]
    visitado = [[[False] * 2 for _ in range(n + 1)] for _ in range(tam_i)]

    def dp(start: int, length: int, turn: int) -> int:
        """Subrutina interna de la DP en arreglos."""
        if visitado[start][length][turn]:
            return memo[start][length][turn]
        # Marcar como visitado
        visitado[start][length][turn] = True
        # Caso base: una sola porción restante
        if length == 1:
            res = w[start] if turn == 0 else 0
            memo[start][length][turn] = res
            return res
        # Turno del profesor: busca maximizar
        if turn == 0:
            mejor = INF_NEG
            for s in range(1, length):
                # Comer prefijo de tamaño s
                ganancia_prefijo = rango_suma(pref, start, start + s - 1)
                valor_prefijo = ganancia_prefijo + dp(start + s, length - s, 1)
                if valor_prefijo > mejor:
                    mejor = valor_prefijo
                # Comer sufijo de tamaño s
                inicio_suf = start + length - s
                ganancia_sufijo = rango_suma(pref, inicio_suf, start + length - 1)
                valor_sufijo = ganancia_sufijo + dp(start, length - s, 1)
                if valor_sufijo > mejor:
                    mejor = valor_sufijo
            memo[start][length][turn] = mejor
            return mejor
        # Turno de la hermana: minimiza lo que obtendrá el profesor
        peor = INF_POS
        for s in range(1, length):
            valor_prefijo = dp(start + s, length - s, 0)
            if valor_prefijo < peor:
                peor = valor_prefijo
            valor_sufijo = dp(start, length - s, 0)
            if valor_sufijo < peor:
                peor = valor_sufijo
        memo[start][length][turn] = peor
        return peor

    mejor_global = INF_NEG
    # Probar cada ángulo válido para la primera jugada (2n opciones)
    for k in range(2 * n):
        # Ganancia inmediata al comer las n porciones comenzando en k
        ganancia_inicial = sum(values[(k + t) % (2 * n)] for t in range(n))
        inicio_restante = k + n
        valor_restante = dp(inicio_restante, n, 1)
        total = ganancia_inicial + valor_restante
        if total > mejor_global:
            mejor_global = total
    return mejor_global


def max_satisfaccion_hash(values: List[int]) -> int:
    """Versión con memoización en diccionarios para el problema Feliz Cumpleaños.

    La estructura de estados es idéntica a la de ``max_satisfaccion_array``.
    En lugar de usar listas tridimensionales, se usa un diccionario
    ``memo`` que almacena pares clave→valor donde la clave es la
    tupla ``(start, length, turn)`` y el valor es ``F(start,length,turn)``.

    Args:
        values: lista de 2n enteros que representan la satisfacción de
        cada porción de torta.

    Returns:
        Entero con la máxima suma de satisfacción que el profesor puede
        asegurar.
    """
    m = len(values)
    if m % 2 != 0:
        raise ValueError("La cantidad de porciones debe ser par (2n).")
    n = m // 2
    w = construir_arreglo_extendido(values)
    pref = prefix_sums(w)
    memo: Dict[Tuple[int, int, int], int] = {}

    def dp(start: int, length: int, turn: int) -> int:
        key = (start, length, turn)
        if key in memo:
            return memo[key]
        # Caso base
        if length == 1:
            res = w[start] if turn == 0 else 0
            memo[key] = res
            return res
        if turn == 0:
            mejor = INF_NEG
            for s in range(1, length):
                ganancia_prefijo = rango_suma(pref, start, start + s - 1)
                valor_prefijo = ganancia_prefijo + dp(start + s, length - s, 1)
                if valor_prefijo > mejor:
                    mejor = valor_prefijo
                inicio_suf = start + length - s
                ganancia_sufijo = rango_suma(pref, inicio_suf, start + length - 1)
                valor_sufijo = ganancia_sufijo + dp(start, length - s, 1)
                if valor_sufijo > mejor:
                    mejor = valor_sufijo
            memo[key] = mejor
            return mejor
        # Hermana minimiza
        peor = INF_POS
        for s in range(1, length):
            valor_prefijo = dp(start + s, length - s, 0)
            if valor_prefijo < peor:
                peor = valor_prefijo
            valor_sufijo = dp(start, length - s, 0)
            if valor_sufijo < peor:
                peor = valor_sufijo
        memo[key] = peor
        return peor

    mejor_global = INF_NEG
    for k in range(2 * n):
        ganancia_inicial = sum(values[(k + t) % (2 * n)] for t in range(n))
        inicio_restante = k + n
        valor_restante = dp(inicio_restante, n, 1)
        total = ganancia_inicial + valor_restante
        if total > mejor_global:
            mejor_global = total
    return mejor_global


def main() -> None:
    """Punto de entrada interactivo.

    Permite al usuario ingresar un valor ``n`` y los ``2n`` valores de
    satisfacción, y muestra el resultado obtenido por ambas versiones
    de la programación dinámica.
    """
    print("=== Problema Feliz Cumpleaños :D ===")
    n = int(input("Ingresa n (habrá 2n porciones): ").strip())
    valores_str = input(
        f"Ingresa los {2 * n} valores de satisfacción separados por espacio:\n"
    ).strip().split()
    if len(valores_str) != 2 * n:
        raise ValueError(
            f"Se esperaban {2 * n} valores, pero se recibieron {len(valores_str)}."
        )
    values = list(map(int, valores_str))
    print("\nCalculando...\n")
    res_arr = max_satisfaccion_array(values)
    res_hash = max_satisfaccion_hash(values)
    print("--- RESULTADOS ---")
    print("DP con arreglos:", res_arr)
    print("DP con hash:    ", res_hash)


if __name__ == "__main__":
    main()