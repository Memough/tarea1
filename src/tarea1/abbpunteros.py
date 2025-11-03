from diccionario import Diccionario


class _Nodo:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: str):
        self.key = key
        self.left = None
        self.right = None


class ABBPunteros(Diccionario):
    def __init__(self):
        self.raiz: _Nodo | None = None

    # internas
    def _norma(self, s: str) -> str:
        return s.strip() 

    def _inserte(self, nodo: _Nodo | None, key: str) -> _Nodo:
        if nodo is None:
            return _Nodo(key)
        if key < nodo.key:
            nodo.left = self._inserte(nodo.left, key)
        else:  # duplicados a la derecha
            nodo.right = self._inserte(nodo.right, key)
        return nodo

    def _miembro(self, nodo: _Nodo | None, key: str) -> bool:
        if nodo is None:
            return False
        if key == nodo.key:
            return True
        if key < nodo.key:
            return self._miembro(nodo.left, key)
        return self._miembro(nodo.right, key)

    def _min_nodo(self, nodo: _Nodo) -> _Nodo:
        # mínimo del subárbol
        actual = nodo
        while actual.left is not None:
            actual = actual.left
        return actual

    def _delete(self, nodo: _Nodo | None, key: str) -> tuple[_Nodo | None, bool]:
        """
        Elimina ocurrencia de key
        """
        if nodo is None:
            return None, False

        if key < nodo.key:
            nodo.left, borrado = self._delete(nodo.left, key)
            return nodo, borrado

        if key > nodo.key:
            nodo.right, borrado = self._delete(nodo.right, key)
            return nodo, borrado

        # key == nodo.key, borra este nodo
        # Caso 1: hoja
        if nodo.left is None and nodo.right is None:
            return None, True

        # Caso 2: un solo hijo
        if nodo.left is None:
            return nodo.right, True
        if nodo.right is None:
            return nodo.left, True

        # Caso 3: dos hijos, reemplaza por sucesor
        sucesor = self._min_nodo(nodo.right)
        nodo.key = sucesor.key
        # borrar sucesor del subárbol derecho
        nodo.right, _ = self._delete(nodo.right, sucesor.key)
        return nodo, True

    def _inorder(self, nodo: _Nodo | None, acc: list[str]):
        if nodo is None:
            return
        self._inorder(nodo.left, acc)
        acc.append(nodo.key)
        self._inorder(nodo.right, acc)

    def _as_lines(self) -> str:
        acc: list[str] = []
        self._inorder(self.raiz, acc)
        return "\n".join(acc)

    def inserte(self, elemento):
        elemento = self._norma(elemento)
        self.raiz = self._inserte(self.raiz, elemento)

    def borre(self, elemento) -> bool:
        elemento = self._norma(elemento)
        self.raiz, borrado = self._delete(self.raiz, elemento)
        return borrado  # True si se borró, false si no existía

    def limpie(self):
        self.raiz = None

    def miembro(self, elemento) -> bool:
        elemento = self._norma(elemento)
        return self._miembro(self.raiz, elemento)

    def imprima(self):
        """
        Devuelve el recorrido en orden y lo imprime
        """
        s = self._as_lines()
        print(s)
        return s

    def __str__(self) -> str:
        return self._as_lines()
