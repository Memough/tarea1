from diccionario import Diccionario

class Array:
    def __init__(self, valor_inicial=None, tamaño = None):
        if not isinstance(tamaño, int) or tamaño < 0:
            raise ValueError("El tamaño debe ser un entero positivo.")
        if not isinstance(valor_inicial, list):
            self.__lista = [valor_inicial] * tamaño
            self.__tamaño = tamaño
        else:
            self.__lista = valor_inicial[:]
            self.__tamaño = len(valor_inicial)        

    def __getitem__(self, índice: int):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites.")
        return self.__lista[índice]

    def __setitem__(self, índice: int, value):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites")
        self.__lista[índice] = value

    def __len__(self) -> int:
        return self.__tamaño

    def __repr__(self) -> str:
        return f"Array({self.__lista!r})"

    def as_list(self):
        return self.__lista

class ListaOrdenadaEstática(Diccionario):
    """Lista ordenada sobre un areglo fijo, permite duplicados"""

    def __init__(self, tamaño: int):
        if tamaño <= 0:
            raise ValueError("El tamaño debe ser mayor que 0.")
        self.__arreglo: Array = Array(valor_inicial="", tamaño=tamaño)
        self.__último: int = -1

    def __len__(self) -> int:
        return self.__último + 1

    def __getitem__(self, índice: int) -> str:
        if not (0 <= índice <= self.__último):
            raise IndexError("Índice fuera de los elementos cargados.")
        return self.__arreglo[índice]

    def _buscar_pos(self, elemento: str) -> tuple[bool, int]:
        """Devuelve. Si no se encuentra, pos es la posición de inserción"""
        
        lo, hi = 0, self.__último
        while lo <= hi:
            mid = (lo + hi) // 2
            v = self.__arreglo[mid]
            if v == elemento:
                return True, mid
            if v < elemento:
                lo = mid + 1
            else:
                hi = mid - 1
        return False, lo  # lo es la posición de inserción

    def inserte(self, elemento: str) -> None:
        # capacidad llena
        if self.__último + 1 >= len(self.__arreglo):
            raise OverflowError("La lista está llena.")

        _, pos = self._buscar_pos(elemento)

        # corrimiento hacia la derecha
        i = self.__último
        while i >= pos:
            self.__arreglo[i + 1] = self.__arreglo[i]
            i -= 1

        self.__arreglo[pos] = elemento
        self.__último += 1

    def borre(self, elemento: str) -> bool:
        encontrado, pos = self._buscar_pos(elemento)
        if not encontrado:
            return False

        # corrimiento hacia la izquierda
        for i in range(pos, self.__último):
            self.__arreglo[i] = self.__arreglo[i + 1]
        # limpiar la última celda visible
        self.__arreglo[self.__último] = ""
        self.__último -= 1
        return True

    def limpie(self) -> None:
        # borra lógicamente todos los elementos
        for i in range(self.__último + 1):
            self.__arreglo[i] = ""
        self.__último = -1

    def miembro(self, elemento: str) -> bool:
        encontrado, _ = self._buscar_pos(elemento)
        return encontrado

    def imprima(self) -> None:
        print(self)

    def __str__(self) -> str:
        if self.__último < 0:
            return ""
        # Solo imprime la parte "activa" del arreglo, en orden
        return "\n".join(self.__arreglo[i] for i in range(self.__último + 1))

    def __del__(self):
        self.limpie()