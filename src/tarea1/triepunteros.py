from diccionario import Diccionario

class Nodo:
    """Nodo de la lista de hijos con puntero a primer hijo y a siguiente hermano."""
    def __init__(self, elemento: str = ''):
        self.elemento = elemento
        self.cantidadHijos = 0
        self.hijo: 'Nodo | None' = None       # primer hijo 
        self.siguiente: 'Nodo | None' = None  # siguiente hermano en la lista
        self.padre: 'Nodo | None' = None      # puntero al padre 


class TriePunteros(Diccionario):
    """
    Implementación de Trie por punteros con lista ligada de hijos
    """
    FIN = '}'  # marca de fin de palabra

    def __init__(self):
        self.__raiz = Nodo()
        self.__tamaño = 0

    def __len__(self) -> int:
        return self.__tamaño

    # internas
    def __validar(self, elemento: str) -> str:
        if not isinstance(elemento, str):
            raise TypeError("La clave debe ser str")
        s = elemento.strip().lower()
        if not s:
            raise ValueError("La clave no puede ser vacía")
        return s

    def __buscar_en_hijos(self, primero: Nodo | None, ch: str):
        """
        Busca el caracter en la lista ligada primero.
        Retorna el encontrado, el anterior y el indice.
        Si no lo encuentra retorna none como encontrado.
        """
        idx = 0
        ant = None
        act = primero
        while act is not None:
            if act.elemento == ch:
                return act, ant, idx
            ant = act
            act = act.siguiente
            idx += 1
        return None, ant, idx  # no encontrado
    
    def __buscar_o_previo_ordenado(self, primero: Nodo | None, ch: str):
        """
        Recorre hermanos manteniendo orden alfabético.
        Si existe 'ch', retorna nodo, anterior.
        Si no existe, retorna None, anterior, debe insertarse después de anterior
        si anterior es None, se inserta al inicio.
        """
        ant = None
        act = primero
        # saltar el FIN al comienzo si está
        if act is not None and act.elemento == self.FIN:
            ant = act
            act = act.siguiente
        while act is not None and act.elemento < ch:
            ant = act
            act = act.siguiente
        if act is not None and act.elemento == ch:
            return act, ant
        return None, ant

    def __tiene_fin(self, nodo: Nodo) -> bool:
        """True si entre los hijos de nodo existe la marca de fin de palabra."""
        encontrado, _, _ = self.__buscar_en_hijos(nodo.hijo, self.FIN)
        return encontrado is not None

    def inserte(self, elemento: str):
        palabra = self.__validar(elemento)
        actual = self.__raiz

        # Recorre/crea el camino
        for ch in palabra:
            encontrado, anterior = self.__buscar_o_previo_ordenado(actual.hijo, ch)
            if encontrado is None:
                nuevo = Nodo(ch)
                nuevo.padre = actual
                # insertar después de anterior o al inicio si es none
                if anterior is None:
                    # si hay FIN debe quedarse primero
                    nuevo.siguiente = actual.hijo
                    actual.hijo = nuevo
                else:
                    nuevo.siguiente = anterior.siguiente
                    anterior.siguiente = nuevo
                actual.cantidadHijos += 1
                encontrado = nuevo
            actual = encontrado

        # insertar FIN al INICIO
        if not self.__tiene_fin(actual):
            fin = Nodo(self.FIN)
            fin.padre = actual
            fin.siguiente = actual.hijo
            actual.hijo = fin
            actual.cantidadHijos += 1
            self.__tamaño += 1

    def miembro(self, elemento: str) -> bool:
        if self.__tamaño == 0:
            return False
        try:
            palabra = self.__validar(elemento)
        except Exception:
            return False

        actual = self.__raiz
        for ch in palabra:
            # como los hijos están ordenados, buscamos por recorrido lineal
            encontrado, anterior = self.__buscar_o_previo_ordenado(actual.hijo, ch)
            if encontrado is None:
                return False
            actual = encontrado
        return self.__tiene_fin(actual)

    def borre(self, elemento: str) -> bool:
        if self.__tamaño == 0:
            return False
        try:
            palabra = self.__validar(elemento)
        except Exception:
            return False

        camino = []
        actual = self.__raiz
        for ch in palabra:
            encontrado, _, _ = self.__buscar_en_hijos(actual.hijo, ch)
            if encontrado is None:
                return False
            camino.append(encontrado)
            actual = encontrado

        fin, fin_ant, _ = self.__buscar_en_hijos(actual.hijo, self.FIN)
        if fin is None:
            return False

        # quitar FIN
        if fin_ant is None:
            actual.hijo = fin.siguiente
        else:
            fin_ant.siguiente = fin.siguiente
        actual.cantidadHijos -= 1
        self.__tamaño -= 1

        # podar hacia arriba
        for nodo in reversed(camino):
            if nodo.cantidadHijos > 0:
                break
            padre = nodo.padre
            if padre is None:
                break
            target, ant, _ = self.__buscar_en_hijos(padre.hijo, nodo.elemento)
            if target is None:
                break
            if ant is None:
                padre.hijo = target.siguiente
            else:
                ant.siguiente = target.siguiente
            padre.cantidadHijos -= 1

        return True

    def limpie(self):
        """Vacía por completo el trie."""
        self.__raiz.hijo = None
        self.__tamaño = 0

<<<<<<< HEAD
    def miembro(self, elemento:str)->bool:
        """revisa si un elemento esta en el diccionario
        
        Args:
            elemento (str):la palabra a buscar
        """
        #checkea de que no este vacio
        if(self.__tamaño == 0):
            return False
        actual = self.__raiz
        for n in elemento:
            if actual.hijo is None:
                return False
            index = self.__charExist__(n,actual.hijo)
            if(index == actual.cantidadHijos): #si el index es igual a la cantidad de hijos entonces no encontro alguna coindencia en dichos hijos
                return False #no encontro la palabra
            actual = actual.hijo
            for i in range(index): #se posiciona en el hijo correspondiente
                actual=actual.siguiente
        if actual.hijo is None:
            return False
        if(self.__charExist__('}',actual.hijo) == actual.cantidadHijos):
            return False
        return True

=======
>>>>>>> 7783545bed113d2f4f5d12d620353bfcccd52c4d
    def imprima(self) -> None:
        """Imprime todas las palabras en orden de exploración por hermanos."""
        print(self)

    def __str__(self) -> str:
        """
        Recorre en profundidad cada nivel itera la lista de hermanos,
        """
        palabras: list[str] = []
        buffer: list[str] = []

        def dfs_lista(primero: Nodo | None):
            cur = primero
            while cur is not None:
                if cur.elemento == self.FIN:
                    palabras.append(''.join(buffer))
                else:
                    buffer.append(cur.elemento)
                    dfs_lista(cur.hijo)
                    buffer.pop()
                cur = cur.siguiente

        dfs_lista(self.__raiz.hijo)
        return "\n".join(palabras)

    def __del__(self):
        self.limpie()
    
    def __del__(self):
        self.limpie()
