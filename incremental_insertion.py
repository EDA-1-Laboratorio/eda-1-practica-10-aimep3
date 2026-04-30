"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo : Estrategia incremental – Insertion sort instrumentado
"""

import time
import random

# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
    """
    Ordena 'arr' usando insertion sort e instrumenta la ejecución.

    Retorna:
        (arreglo_ordenado, comparaciones, movimientos, tiempo_seg)
    """
    arr = arr.copy()
    n = len(arr)
    comparaciones = 0
    movimientos = 0
    inicio = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1

        # Mientras j >= 0 y arr[j] > llave:
        while j >= 0:
            comparaciones += 1 # Contamos cada comparación
            if arr[j] > llave:
                arr[j + 1] = arr[j] # Desplaza
                movimientos += 1
                j -= 1
            else:
                break 

        # Coloca llave en su posición correcta
        arr[j + 1] = llave
        movimientos += 1 # La colocación de llave cuenta como movimiento

    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)

# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def generar_arreglo(n: int, escenario: str) -> list:
    """
    Genera un arreglo de tamaño n según el escenario indicado.

    Escenarios:
        'mejor' -> ya ordenado de menor a mayor (mejor caso: Θ(n))
        'peor' -> inversamente ordenado (peor caso: Θ(n²))
        'promedio' -> aleatorio (caso promedio: Θ(n²))
    """
    if escenario == 'mejor':
        return list(range(n))
    elif escenario == 'peor':
        return list(range(n, 0, -1))
    elif escenario == 'promedio':
        arr = list(range(n))
        random.shuffle(arr)
        return arr
    else:
        raise ValueError(f"Escenario inválido: {escenario}")

def medir_escenarios(tamanos: list) -> list:
    """
    Para cada tamaño en 'tamanos' evalúa los tres escenarios e imprime resultados.

    Retorna:
        Lista de dicts: {tamano, escenario, comparaciones, movimientos, tiempo}
    """
    resultados = []
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            arr = generar_arreglo(n, escenario)
            _, comparaciones, movimientos, tiempo = insertion_sort_metricas(arr)
            resultados.append({
                "tamano": n,
                "escenario": escenario,
                "comparaciones": comparaciones,
                "movimientos": movimientos,
                "tiempo": tiempo
            })
    return resultados

# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def _merge(izq: list, der: list) -> list:
    """Combina dos listas ordenadas en una sola."""
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    # Agrega los elementos restantes
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def _merge_sort_hibrido(arr: list, umbral: int) -> list:
    """
    Divide 'arr' recursivamente.
    Si el subarreglo tiene tamaño <= umbral, usa insertion_sort_metricas.
    Si no, divide a la mitad y fusiona con _merge.
    """
    if len(arr) <= umbral:
        return insertion_sort_metricas(arr)[0]

    mid = len(arr) // 2
    izq = _merge_sort_hibrido(arr[:mid], umbral)
    der = _merge_sort_hibrido(arr[mid:], umbral)
    return _merge(izq, der)

def insertion_sort_hibrido(arr: list, umbral: int = 32) -> list:
    """
    Punto de entrada del ordenamiento híbrido.
    Retorna el arreglo ordenado.
    """
    return _merge_sort_hibrido(arr, umbral)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000, 8000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamano']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")
