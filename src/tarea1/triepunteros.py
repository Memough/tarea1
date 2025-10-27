from diccionario import Diccionario

class Nodo:
    def __init__(self, elemento:str=''):
        self.elemento = elemento
        self.hijo: Nodo | None = None
        self.siguiente: Nodo |None = None


class TriePunteros(Diccionario):
    def __init__(self):
        self.__raiz = Nodo()
        self.__tamaño = 0

    def __len__(self)->int:
        return self.__tamaño
    
    #use later XDn't
    def __charExist__(self, char:str, actual:Nodo)->int:
        index = 0
        while actual is not None:
            if actual.elemento == str:
                return index
            else:
                actual = actual.siguiente
                index += 1
        return index

    #finnish later bruh
    def inserte(self, elemento:str):
        actual = self.__raiz
        if self.__tamaño == 0:
            for n in elemento:
                actual.hijo = Nodo(n)
                actual = actual.hijo
        else:
            actual = actual.hijo
            for n in elemento:
                if(self.__charExist__(n, actual)==self.__tamaño):
                    nuevo = Nodo(n)
                    
                    

    #do later
    def borre(self, elemento:str):
        pass

    def limpie(self):
        self.__raiz.hijo = None
        self.__tamaño = 0

    #do later as well
    def miembro(self, elemento:str)->bool:
        pass

    def imprima(self) -> None:
        print(self)

    #modify later
    def __str__(self)->str:
        elementos = []
        actual = self.__raiz.hijo
        while actual is not None:
            elementos.append(actual.elemento)
            actual = actual.hijo
        return "\n".join(elementos)

    def __del__(self):
        self.limpie()