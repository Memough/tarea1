from diccionario import Diccionario

class Nodo:
    def __init__(self, elemento:str=''):
        self.elemento = elemento
        self.siguiente : Nodo | None = None

class ListaOrdenadaPunteros(Diccionario):
    def __init__(self):
        self.cabeza = Nodo()
        self.tamaño = 0

    def __len__(self):
        return self.tamaño
    
    def __getitem__(self, indice):
        pass

    def inserte(self, elemento):
        if self.__cabeza.siguiente is None:
            self.__cabeza.siguiente = Nodo(elemento)
        else:
            referencia = self.__cabeza
            while referencia.siguiente.elemento < elemento and referencia.siguiente.siguiente is not None:
        