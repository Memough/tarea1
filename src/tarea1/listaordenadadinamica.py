from tarea1.diccionario import Diccionario

class Nodo:
    def __init__(self, elemento:str=''):
        self.elemento = elemento
        self.siguiente: Nodo | None = None

class ListaOrdenadaDinámica(Diccionario):
    def __init__(self):
        self.__cabeza = Nodo()
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño
    
    def __getitem__(self, indice: int) -> str:
        """Permite acceder como lista"""
        if not (0 <= indice < self.__tamaño):
            raise IndexError("Indice fuera de rango")
        ref = self.__cabeza.siguiente
        for _ in range(indice):
            ref = ref.siguiente
        return ref.elemento

    def inserte(self, elemento: str) -> None:
        """Inserta en orden"""
        anterior = self.__cabeza
        actual = anterior.siguiente
        while actual is not None and actual.elemento <= elemento:
            anterior, actual = actual, actual.siguiente
        nuevo = Nodo(elemento)
        nuevo.siguiente = actual
        anterior.siguiente = nuevo
        self.__tamaño += 1

    def borre(self, elemento: str) -> bool:
        """Borra ocurrencia si existe"""
        anterior = self.__cabeza
        actual = anterior.siguiente
        while actual is not None:
            if actual.elemento == elemento:
                anterior.siguiente = actual.siguiente
                self.__tamaño -= 1
                return True
            if actual.elemento > elemento:
                return False
            anterior, actual = actual, actual.siguiente
        return False

    def limpie(self) -> None:
        """Vacía la lista."""
        self.__cabeza.siguiente = None
        self.__tamaño = 0

    def miembro(self, elemento: str) -> bool:
        """Devuelve true si el elemento está en la lista"""
        actual = self.__cabeza.siguiente
        while actual is not None and actual.elemento <= elemento:
            if actual.elemento == elemento:
                return True
            actual = actual.siguiente
        return False

    def imprima(self) -> None:
        print(self)

    def __str__(self) -> str:
        elementos = []
        actual = self.__cabeza.siguiente
        while actual is not None:
            elementos.append(actual.elemento)
            actual = actual.siguiente
        return "\n".join(elementos)

    def __del__(self):
        self.limpie()