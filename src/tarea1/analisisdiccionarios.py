# -*- coding: utf-8 -*-
from __future__ import annotations
import random
import string
import time
import statistics
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
from listaordenadadinamica import ListaOrdenadaDinámica
from listaordenadaestatica import ListaOrdenadaEstática
from tablahashabierta import TablaHashAbierta
from abbpunteros import ABBPunteros
from abbvectorheap import ABBVectorHeap
from triepunteros import TriePunteros
from triearreglos import TrieArreglos

#Utilidades
ABC = string.ascii_lowercase  # a..z

def hilera_aleatoria() -> str:
    return ''.join(random.choice(ABC) for _ in range(20))

def generar_datos(tamaño: int, semilla: int) -> list[str]:
    """Genera una lista de hileras aleatorias de tamaño dado"""
    random.seed(semilla)
    return [hilera_aleatoria() for _ in range(tamaño)]

def construir_diccionario(nombre: str, n: int):
    """Devuelve una instancia de la estructura pedida por nombre"""
    if nombre == "ListaOrdenadaDinámica":
        return ListaOrdenadaDinámica()
    if nombre == "ListaOrdenadaEstática":
        return ListaOrdenadaEstática(n)  # arreglo de tamaño fijo n
    if nombre == "TablaHashAbierta":
        return TablaHashAbierta()
    if nombre == "ABBPunteros":
        return ABBPunteros()
    if nombre == "ABBVectorHeap":
        return ABBVectorHeap()
    if nombre == "TriePunteros":
        return TriePunteros()
    if nombre == "TrieArreglos":
        return TrieArreglos()
    raise ValueError("Estructura desconocida")

def medir_corrida(nombre: str, datos: list[str]) -> dict[str, float]:
    """
    Corre una corrida para una estructura que inserta todos los datos, verifica membresía de todos y borra todos.
    Además retorna tiempos promedio por operación.
    """
    n = len(datos)
    ed = construir_diccionario(nombre, n)

    # Inserción
    t0 = time.perf_counter()
    for s in datos:
        ed.inserte(s)
    t1 = time.perf_counter()
    t_ins_total = t1 - t0

    # Miembro (búsqueda)
    t0 = time.perf_counter()
    aciertos = 0
    for s in datos:
        if ed.miembro(s):
            aciertos += 1
    t1 = time.perf_counter()
    t_miem_total = t1 - t0

    # Borrado
    t0 = time.perf_counter()
    borrados = 0
    for s in datos:
        if ed.borre(s):
            borrados += 1
    t1 = time.perf_counter()
    t_bor_total = t1 - t0

    return {
        "ins_prom": t_ins_total / n if n else 0.0,
        "miem_prom": t_miem_total / n if n else 0.0,
        "bor_prom": t_bor_total / n if n else 0.0,
    }

def medir_memoria(nombre: str, datos: list[str]) -> int:
    """
    Inserta todos y devuelve la memoria actual, está es una aproximación del uso de memoria en bytes
    """
    ed = construir_diccionario(nombre, len(datos))
    tracemalloc.reset_peak()
    _ = tracemalloc.get_traced_memory()  # inicializa lectura
    for s in datos:
        ed.inserte(s)
    current, peak = tracemalloc.get_traced_memory()
    ed.limpie()
    return current # aproximación del uso de memoria en bytes

# Gráficos
def graficar_lineas_por_operacion(df_op: "pd.DataFrame", operacion: str) -> None:
    """
    Gráfico de líneas por operación.
    x = tamaño (N), y = tiempo promedio (s/op), una línea por estructura.
    df_op: filas = estructura, columnas = tamaño, valores = promedios.
    """
    plt.figure()
    for estructura in df_op.index:
        plt.plot(df_op.columns, df_op.loc[estructura].values, marker='o', label=estructura)
    plt.xlabel("Tamaño (N)")
    plt.ylabel(f"Tiempo promedio de {operacion} de segundos por operación")
    plt.title(f"Comparación por operación: {operacion}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

def graficar_barras_memoria(df_mem: "pd.DataFrame") -> None:
    """
    Barras agrupadas: x = tamaños (N) y una barra por estructura.
    """
    plt.figure()
    x = range(len(df_mem.columns))
    ancho = 0.1  # ancho de cada barra
    offset = - (len(df_mem.index) // 2) * ancho

    for i, estructura in enumerate(df_mem.index):
        posiciones = [xx + offset + i*ancho for xx in x]
        plt.bar(posiciones, df_mem.loc[estructura].values, width=ancho, label=estructura)
    plt.xticks(list(range(len(df_mem.columns))), [str(c) for c in df_mem.columns])
    plt.xlabel("Tamaño N")
    plt.ylabel("Memoria aproximada bytes")
    plt.title("Uso de memoria por estructura y tamaño N")
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()


# Programa principal
def main():
    estructuras = [
        "ListaOrdenadaDinámica",
        "ListaOrdenadaEstática",
        "TablaHashAbierta",
        "ABBPunteros",
        "ABBVectorHeap",
        "TriePunteros",
        "TrieArreglos",
    ]

    tamaños = [5, 10, 20]
    corridas = 10 

    print("\nPROGRAMA DE ANÁLISIS\n")
    print(f"Estructuras: {', '.join(estructuras)}")
    print(f"Tamaños N: {tamaños}")
    print(f"Corridas por caso: {corridas}\n")

    # Inicia la medición de la memoria global
    tracemalloc.start()

    # Resultados
    resultados: list[dict] = []

    # Tiempos
    print("Midiendo tiempos promedio por operación...\n")
    for n in tamaños:
        for nombre in estructuras:
            lista_ins, lista_miem, lista_bor = [], [], []
            for k in range(corridas):
                datos = generar_datos(n, semilla=1000 + k) 
                r = medir_corrida(nombre, datos)
                lista_ins.append(r["ins_prom"])
                lista_miem.append(r["miem_prom"])
                lista_bor.append(r["bor_prom"])

            fila = {
                "estructura": nombre,
                "tamaño": n,
                "ins_prom": statistics.fmean(lista_ins),
                "ins_sd": statistics.pstdev(lista_ins),
                "miem_prom": statistics.fmean(lista_miem),
                "miem_sd": statistics.pstdev(lista_miem),
                "bor_prom": statistics.fmean(lista_bor),
                "bor_sd": statistics.pstdev(lista_bor),
            }
            resultados.append(fila)
            print(f"{nombre:<24} N={n:<9}  ins={fila['ins_prom']:.6f}s/op  miem={fila['miem_prom']:.6f}s/op  bor={fila['bor_prom']:.6f}s/op")

    # Memoria
    print("\nMidiendo memoria aproximada posterior a inserciones...\n")
    filas_memoria: list[dict] = []
    for n in tamaños:
        datos = generar_datos(n, semilla=777)
        for nombre in estructuras:
            mem_b = medir_memoria(nombre, datos)
            filas_memoria.append({"estructura": nombre, "tamaño": n, "mem_bytes": mem_b})
            print(f"{nombre:<24} N={n:<9}  memoria≈ {mem_b} B")

    # Tablas y gráficos
    df_t = pd.DataFrame(resultados)
    df_m = pd.DataFrame(filas_memoria)

    # Pivotes para gráficos
    df_ins = df_t.pivot(index="estructura", columns="tamaño", values="ins_prom")
    df_miem = df_t.pivot(index="estructura", columns="tamaño", values="miem_prom")
    df_bor = df_t.pivot(index="estructura", columns="tamaño", values="bor_prom")
    df_memoria_bytes = df_m.pivot(index="estructura", columns="tamaño", values="mem_bytes")

    print("\n\nTABLAS\n")
    print("Inserción – tiempo promedio de segundos por operación:")
    print(df_ins.round(6).to_string())
    print("\nMiembro – tiempo promedio de segundos por operación:")
    print(df_miem.round(6).to_string())
    print("\nBorrado – tiempo promedio de segundos por operación:")
    print(df_bor.round(6).to_string())
    print("\nMemoria aproximada en bytes:")
    print(df_memoria_bytes.to_string())

    # Gráficos
    graficar_lineas_por_operacion(df_ins, "inserción")
    graficar_lineas_por_operacion(df_miem, "membresía")
    graficar_lineas_por_operacion(df_bor, "borrado")
    graficar_barras_memoria(df_memoria_bytes)
    plt.show()

    print("\nFin del análisis.\n")


if __name__ == "__main__":
    main()