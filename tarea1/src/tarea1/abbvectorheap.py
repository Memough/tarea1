from tarea1.diccionario import Diccionario

class ABBVectorHeap(Diccionario):
    def __init__(self):
        self.arbol = []

    # auxiliares
    def _norma(self, s: str) -> str:
        # Ajusta según tu contrato: solo a..z, longitud 20, etc.
        return s.strip()  # .lower() si tu diccionario trabaja en minúsculas
    
    def _inserte(self, index, key):
        # Asegura que exista el índice
        while index >= len(self.arbol):
            self.arbol.append(None)
        # inserta según el orden
        if self.arbol[index] is None:
            self.arbol[index] = key
        elif key < self.arbol[index]:
            self._inserte(2 * index + 1, key)
        else:
            self._inserte(2 * index + 2, key)

    def _miembro(self, index, key):
        if index >= len(self.arbol) or self.arbol[index] is None:
            return False
        if self.arbol[index] == key:
            return True
        if key < self.arbol[index]:
            return self._miembro(2 * index + 1, key)
        return self._miembro(2 * index + 2, key)

    def _inorder(self, index):
        if index >= len(self.arbol) or self.arbol[index] is None:
            return []
        return (
            self._inorder(2 * index + 1)
            + [self.arbol[index]]
            + self._inorder(2 * index + 2)
        )

    def _as_lines(self):
       return "\n".join(str(e) for e in self._inorder(0))
    
    def inserte(self, elemento):
        """Inserta un elemento"""
        if not self.arbol:
            self.arbol.append(elemento)
        else:
            self._inserte(0, elemento)

    def borre(self, elemento) -> bool:
        """Borra un elemento. Retorna True si se borró, False si no existía."""
        elemento = self._norma(elemento)
        if not self.arbol:
            return False

        elementos = self._inorder(0)
        try:
            elementos.remove(elemento)   # quita una sola vez
        except ValueError:
            return False                 # no estaba

        # reconstruir
        self.arbol = []
        for e in elementos:
            self.inserte(e)

        return True

    def limpie(self):
        """Vacía completamente el árbol"""
        self.arbol = []

    def miembro(self, elemento):
        """Retorna True si el elemento está en el árbol"""
        return self._miembro(0, elemento)

    def imprima(self):
        """Devuelve una cadena con los elementos en orden"""
        s = self._as_lines()
        print(s)
        return s

    def __str__(self) -> str:
        """Representación en texto"""
        return self._as_lines()