from tarea1.diccionario import Diccionario

class Nodo:
    """los nodos usados para almacenar cada caracter"""
    def __init__(self, elemento:str=''):
        self.elemento = elemento
        self.cantidadHijos=0
        self.hijo: Nodo | None = None #puntero a la lista con los caracteres siguientes de la palabra
        self.siguiente: Nodo |None = None #puntero al caracter alternativo de la palabra
        self.padre : Nodo | None = None #puntero de regreso para simular recursvidad de manera iterativa


class TriePunteros(Diccionario):
    def __init__(self):
        self.__raiz = Nodo()
        self.__tamaño = 0

    def __len__(self)->int:
        """retorna el tamaño del trie"""
        return self.__tamaño
    
    def __charExist__(self, char:str, actual:Nodo)->int:
        """busca si el caracter existe dentro de esa sección de hijos"""
        index = 0
        while actual is not None:
            if actual.elemento == char:
                return index
            else:
                actual = actual.siguiente
                index += 1
        return index

    def inserte(self, elemento:str):
        """inserta un elemento al diccionario
        
        Args:
            elemento (str):la palabra a insertar
        """
        actual = self.__raiz
        if self.__tamaño == 0: #checkea de que no este vacio
            for n in elemento: 
                actual.hijo = Nodo(n)
                actual.hijo.padre = actual
                actual.cantidadHijos +=1
                actual = actual.hijo
        else:
            for n in elemento:
                index = self.__charExist__(n, actual.hijo) #revisa si existe un nodo con el mismo caracter
                if(index == actual.cantidadHijos): #en caso de que no crea uno al inicio
                    nuevo = Nodo(n)
                    nuevo.siguiente = actual.hijo
                    actual.cantidadHijos +=1
                    actual.hijo = nuevo
                    actual.hijo.padre = actual
                    actual = actual.hijo
                else: #en caso de que si se mueve hacia ese nodo
                    actual = actual.hijo
                    for i in range(index):
                        actual=actual.siguiente
        #crea un nodo notificando la terminacion de la palabra
        fin = Nodo('}')
        fin.siguiente = actual.hijo
        actual.hijo = fin
        actual.hijo.padre = actual
        actual.cantidadHijos +=1
        self.__tamaño +=1

    #do later
    def borre(self, elemento:str):
        """borra un elemento al diccionario
        
        Args:
            elemento (str):la palabra a borrar
        """
        borrarEntero = True
        actual = self.__raiz
        if(self.miembro(elemento) == False):
            return False #no existe dicha palabra en el trie
        for n in elemento:
            index = self.__charExist__(n,actual.hijo)
            actual = actual.hijo
            for i in range(index): # se posiciona en la letra conrrespondiente
                actual = actual.siguiente
        #una vez en la parte de abajo de la palabra ir borrando de arriba para abajo
        while(borrarEntero and actual != self.__raiz):
            if(actual.cantidadHijos<1): #en caso de que exista una palabra que extienda la palabra a eliminar
                borrarEntero = False
                index = self.__charExist__('}', actual.hijo)
                if(index == 0):#en caso de que la terminación de la palabra sea el inicio de los hijos
                    actual.hijo = actual.hijo.siguiente #reemplaza los punteros apuntando a el
                    actual.hijo.padre = actual
                    actual.cantidadHijos -=1
                else:#en caso contrario
                    son = actual.hijo
                    for i in range(index-1): #se desplaza hasta la terminacion de la palabra
                        son = son.siguiente
                    son.siguiente = son.siguiente.siguiente #reemplaza los punteros apuntando a esa terminacion para sacarlo de la lista
                    actual.cantidadHijos -=1
                borrarEntero = False
            else:
                actual.hijo = None
                actual.cantidadHijos -=1
            actual = actual.padre
        self.__tamaño -=1
        return True

    def limpie(self):
        """vacia el trie"""
        self.__raiz.hijo = None
        self.__tamaño = 0

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
            index = self.__charExist__(n,actual.hijo)
            if(index == actual.cantidadHijos): #si el index es igual a la cantidad de hijos entonces no encontro alguna coindencia en dichos hijos
                return False #no encontro la palabra
            actual = actual.hijo
            for i in range(index): #se posiciona en el hijo correspondiente
                actual=actual.siguiente
        if(self.__charExist__('}',actual.hijo) == actual.cantidadHijos):
            return False
        return True

    def imprima(self) -> None:
        """imprime el diccionario"""
        print(self)

    
    def __str__(self)->str:
        """convierte el trie en un string para imprimir"""
        
        elementos = []
        actual = self.__raiz
        contador = 0
        stackWord = [] #donde se guarden los caracteres antes de convertirse en un string
        regresar = [] #cuanto y a donde regresarse 2:para arriba, 1:para la izquierda
        atras = False #determina si se retorna para simular recursividad
        while (contador <self.__tamaño and actual != None):
            if(actual.elemento == '}'):
                contador +=1
                word =""
                for n in stackWord:
                    word += n
                elementos.append(word)
                if(actual.siguiente):
                    actual = actual.siguiente
                else:
                    actual = actual.padre
                    while(regresar.pop()!=2):
                        stackWord.pop()
                    stackWord.pop()
                    atras = True
                continue
            else:
                if(atras and actual.siguiente):
                    actual=actual.siguiente
                    atras = False
                    regresar.append(1)
                elif(atras and actual.siguiente == None):
                    actual = actual.padre
                    stackWord.pop()
                    regresar.pop()
                elif(atras==False):
                    stackWord.append(actual.elemento)
                    actual = actual.hijo
                    regresar.append(2)
                    
                    
        return "\n".join(elementos)
    
    def __del__(self):
        self.limpie()