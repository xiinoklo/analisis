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

import sys
from typing import List, Dict, Tuple

# Aumentar el límite de recursión es crítico para O(n^3) DP
# Un n=100 podría generar una profundidad de recursión cercana a 100.
# Para casos extremos y seguridad, lo elevamos significativamente.
sys.setrecursionlimit(20000)

def max_satisfaccion_array(st: List[int]) -> int:
    """
    Calcula la máxima satisfacción garantizada para el Profesor utilizando
    Programación Dinámica con Memoización basada en ARREGLOS.
    
    Complejidad Temporal: O(n^3)
    Complejidad Espacial: O(n^2)
    """
    n_slices = len(st)
    if n_slices == 0:
        return 0
    n = n_slices // 2
    
    # Duplicamos el arreglo para manejar la circularidad de manera lineal.
    # Esto permite acceder a rangos como [2n-1, 0, 1] simplemente usando índices.
    doubled_st = st + st
    
    # Precomputamos sumas de prefijos para consultas de rango O(1)
    prefix_sum = [0] * (len(doubled_st) + 1)
    for i in range(len(doubled_st)):
        prefix_sum[i+1] = prefix_sum[i] + doubled_st[i]

    def get_sum(start, length):
        """Retorna la suma del segmento [start, start+length-1] en O(1)"""
        return prefix_sum[start + length] - prefix_sum[start]

    # Tabla de Memoización: (2n+1) x (n+1)
    # Filas: índice de inicio (hasta 2n para cubrir toda la vuelta)
    # Columnas: longitud del segmento (hasta n)
    # Inicializamos con un valor centinela (-inf)
    memo = [[-float('inf')] * (n + 1) for _ in range(2 * n + 1)]

    def dp(start: int, length: int) -> int:
        """
        Retorna la ganancia MÁXIMA que el jugador actual puede obtener
        del segmento definido por 'start' y 'length'.
        """
        # Caso Base: Solo queda una porción, el jugador se la come.
        if length == 1:
            return doubled_st[start]
        
        # Verificar si ya está calculado
        if memo[start % n_slices][length]!= -float('inf'):
            return memo[start % n_slices][length]

        current_total_value = get_sum(start, length)
        
        # El jugador actual (maximizador) elige el corte 'k' que le da el mejor resultado.
        # Su resultado es `total - ganancia_oponente`. Para maximizarlo, debe minimizar
        # la ganancia del oponente. Para un 'k' dado, el oponente obtendrá
        # min(dp(start, k), dp(start + length - k, k)), ya que el jugador actual
        # elegirá si dejar el prefijo o el sufijo.
        # El jugador actual debe entonces elegir el 'k' que maximice su propio resultado.
        
        best_score_for_me = -float('inf')

        for k in range(1, length):
            # Oponente juega en prefijo de largo k -> Oponente gana dp(start, k)
            val_left = dp(start, k)
            
            # Oponente juega en sufijo de largo k -> Oponente gana dp(start + length - k, k)
            val_right = dp(start + length - k, k)
            
            # Yo elijo el corte que DEJA MENOS al oponente para este k.
            opponent_score = min(val_left, val_right)
            
            # Mi puntaje para este k es el total menos lo que se lleva el oponente.
            my_score = current_total_value - opponent_score
            
            # Quiero encontrar el k que maximice mi puntaje.
            if my_score > best_score_for_me:
                best_score_for_me = my_score
        
        # Mi mejor resultado es el máximo que encontré.
        res = best_score_for_me
        memo[start % n_slices][length] = res
        return res

    # Problema Original: El Profesor elige el primer corte de tamaño n.
    # Él maximiza: Total de la Torta - (Máxima ganancia de la Hermana en el resto)
    
    total_cake = get_sum(0, n_slices)
    max_prof = -float('inf')

    for i in range(n_slices):
        # Si el Profesor empieza en i, come [i, i+n-1].
        # Deja a la hermana el segmento que empieza en i+n con longitud n.
        sister_best = dp(i + n, n)
        prof_gain = total_cake - sister_best
        
        if prof_gain > max_prof:
            max_prof = prof_gain
            
    return max_prof


def max_satisfaccion_hash(st: List[int]) -> int:
    """
    Calcula la máxima satisfacción usando Memoización basada en TABLAS DE HASH (Diccionarios).
    Estructuralmente idéntica a la versión de array, pero cambia el almacenamiento.
    """
    n_slices = len(st)
    if n_slices == 0:
        return 0
    n = n_slices // 2
    doubled_st = st + st
    
    prefix_sum = [0] * (len(doubled_st) + 1)
    for i in range(len(doubled_st)):
        prefix_sum[i+1] = prefix_sum[i] + doubled_st[i]

    def get_sum(start, length):
        return prefix_sum[start + length] - prefix_sum[start]

    # Diccionario para memoización
    # Clave: Tupla (start, length) -> Valor: int
    memo: Dict[Tuple[int, int], int] = {}

    def dp(start: int, length: int) -> int:
        if length == 1:
            return doubled_st[start]
        
        state = (start % n_slices, length)
        if state in memo:
            return memo[state]

        current_total_value = get_sum(start, length)
        best_score_for_me = -float('inf')

        for k in range(1, length):
            # Oponente juega en prefijo de largo k -> Oponente gana dp(start, k)
            val_left = dp(start, k)
            
            # Oponente juega en sufijo de largo k -> Oponente gana dp(start + length - k, k)
            val_right = dp(start + length - k, k)
            
            # Yo elijo el corte que DEJA MENOS al oponente para este k.
            opponent_score = min(val_left, val_right)
            
            # Mi puntaje para este k es el total menos lo que se lleva el oponente.
            my_score = current_total_value - opponent_score
            
            # Quiero encontrar el k que maximice mi puntaje.
            if my_score > best_score_for_me:
                best_score_for_me = my_score

        res = best_score_for_me
        memo[state] = res
        return res

    total_cake = get_sum(0, n_slices)
    max_prof = -float('inf')

    for i in range(n_slices):
        sister_best = dp(i + n, n)
        prof_gain = total_cake - sister_best
        if prof_gain > max_prof:
            max_prof = prof_gain
            
    return max_prof

if __name__ == "__main__":
    print("Problema de la Torta - Maximización de Satisfacción")
    print("----------------------------------------------------")
    print("Ingrese los valores de satisfacción de las 2n porciones de torta, separados por espacios.")
    
    try:
        input_line = input("Valores: ")
        satisfacciones = [int(x) for x in input_line.split()]
        
        if not satisfacciones:
            print("Error: No se ingresaron valores.")
        elif len(satisfacciones) % 2 != 0:
            print("Error: El número de porciones debe ser par (2n).")
        else:
            # Usamos la versión con arrays por defecto
            resultado = max_satisfaccion_array(satisfacciones)
            print(f"\nMáxima satisfacción que el profesor puede garantizar: {resultado}")

    except ValueError:
        print("\nError: Ingrese solo números enteros separados por espacios.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
