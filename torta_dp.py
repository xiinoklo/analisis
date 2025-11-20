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
    n = n_slices // 2
    
    # Duplicamos el arreglo para manejar la circularidad de manera lineal.
    # Esto permite acceder a rangos como [2n-1, 0, 1] simplemente usando índices.
    doubled_st = st + st
    
    # Precomputamos sumas de prefijos para consultas de rango O(1)
    prefix_sum =  * (len(doubled_st) + 1)
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
        if memo[start][length]!= -float('inf'):
            return memo[start][length]

        current_total_value = get_sum(start, length)
        
        # Lógica Minimax:
        # El jugador actual hace un corte y deja un segmento al oponente.
        # El oponente jugará óptimamente para maximizar SU ganancia en ese resto.
        # Por tanto, el jugador actual obtiene:
        # Total_Actual - (Lo máximo que el oponente puede sacar del resto)
        # Para maximizar mi ganancia, debo MINIMIZAR la ganancia máxima del oponente.
        
        min_opponent_score = float('inf')
        
        # Iteramos sobre todos los cortes posibles.
        # k representa el tamaño del segmento que se DEJA al oponente.
        # Geométricamente, al cortar, se generan dos arcos. Uno se come, otro se deja.
        # Podemos dejar el lado "izquierdo" (prefijo) o el "derecho" (sufijo).
        
        for k in range(1, length):
            # Opción 1: Dejar el prefijo de longitud k al oponente
            # El oponente jugará en dp(start, k)
            val_left = dp(start, k)
            
            # Opción 2: Dejar el sufijo de longitud k al oponente
            # El oponente jugará en dp(start + length - k, k)
            val_right = dp(start + length - k, k)
            
            # Buscamos el escenario donde el oponente gane lo MENOS posible
            move_min = min(val_left, val_right)
            
            if move_min < min_opponent_score:
                min_opponent_score = move_min
        
        # Mi mejor resultado es el total menos lo mejor que pude forzar al oponente a tener
        res = current_total_value - min_opponent_score
        memo[start][length] = res
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
    n = n_slices // 2
    doubled_st = st + st
    
    prefix_sum =  * (len(doubled_st) + 1)
    for i in range(len(doubled_st)):
        prefix_sum[i+1] = prefix_sum[i] + doubled_st[i]

    def get_sum(start, length):
        return prefix_sum[start + length] - prefix_sum[start]

    # Diccionario para memoización
    # Clave: Tupla (start, length) -> Valor: int
    memo: Dict, int] = {}

    def dp(start: int, length: int) -> int:
        if length == 1:
            return doubled_st[start]
        
        state = (start, length)
        if state in memo:
            return memo[state]

        current_total = get_sum(start, length)
        min_opp = float('inf')

        for k in range(1, length):
            val_left = dp(start, k)
            val_right = dp(start + length - k, k)
            min_opp = min(min_opp, val_left, val_right)
            
        res = current_total - min_opp
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
