from tarea1.diccionario import Diccionario

class Array:
    def __init__(self, valor_inicial=None, tamaño = None):
        if not isinstance(tamaño, int) or tamaño < 0:
            raise ValueError("El tamaño debe ser un entero positivo.")
        if not isinstance(valor_inicial, list):
            self.__lista = [valor_inicial] * tamaño
            self.__tamaño = tamaño
        else:
            self.__lista = valor_inicial
            self.__tamaño = len(valor_inicial)        

    def __getitem__(self, índice):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites.")
        return self.__lista[índice]

    def __setitem__(self, índice, value):
        if not (0 <= índice < self.__tamaño):
            raise IndexError("Índice de arreglo fuera de los límites")
        self.__lista[índice] = value

    def __len__(self):
        return self.__tamaño

    def __repr__(self):
        return f"Array({self.__lista})"
    
    def __str__(self) -> str:
        return str(self.__lista)
    

class Nodo:
    
    # Constantes para el rango de caracteres
    RANGO_INICIO = ord('a')  # 97
    RANGO_FIN = ord('{')     # 123
    TAMAÑO_ARREGLO = RANGO_FIN - RANGO_INICIO + 1  # 27 posiciones
    
    def __init__(self):
        """
        Crea un nuevo nodo con un arreglo de 27 posiciones (a-z + {).
        Todas las posiciones se inicializan en None.        
        """
        # Arreglo de tamaño fijo: índice 0='a', 1='b', ..., 25='z', 26='{'
        self.hijos = Array(valor_inicial=None, tamaño=Nodo.TAMAÑO_ARREGLO)
    
    @staticmethod
    def char_a_indice(caracter):
        """
        Convierte un carácter ('a'-'z' o '{') a un índice del arreglo (0-26).
        
        Args:
            caracter (str): Carácter a convertir
            
        Returns:
            int: Índice correspondiente en el arreglo
        """
        return ord(caracter) - Nodo.RANGO_INICIO
    
    @staticmethod
    def indice_a_char(indice):
        """
        Convierte un índice del arreglo (0-26) a un carácter ('a'-'z' o '{').
        
        Args:
            indice (int): Índice del arreglo
            
        Returns:
            str: Carácter correspondiente
        """
        return chr(indice + Nodo.RANGO_INICIO)
    
    def tiene_hijos(self):
        """
        Verifica si el nodo tiene algún hijo (excluyendo el marcador de fin '{').
        
        Returns:
            bool: True si tiene al menos un hijo no-None
        """
        for i in range(26):  # Solo verificar 'a' a 'z', no el marcador '{'
            if self.hijos[i] is not None:
                return True
        return False


class TrieArreglos(Diccionario):
    """
    Implementación de un Trie (árbol de prefijos) usando arreglos de tamaño fijo.
    """
    
    def __init__(self):
        """
        Inicializa el Trie creando un nodo raíz vacío.
        """
        self.raiz = Nodo()
    
    def limpie(self):
        """
        Vacía el Trie reiniciándolo.
        """
        del self.raiz
        self.raiz = Nodo()
    
    def inserte(self, elemento):
        """
        Inserta una palabra en el Trie.
        """
        if not elemento:
            return
        
        nodo_actual = self.raiz
        
        # Recorrer cada carácter de la palabra
        for caracter in elemento.lower():
            # Solo procesar caracteres válidos (a-z)
            if 'a' <= caracter <= 'z':
                indice = Nodo.char_a_indice(caracter)

                # Si el hijo no existe (es None), crearlo
                if nodo_actual.hijos[indice] is None:
                    nodo_actual.hijos[indice] = Nodo()

                # Moverse al siguiente nodo
                nodo_actual = nodo_actual.hijos[indice]

        # Marcar el fin de palabra: t^['{']:= t
        # El nodo apunta a sí mismo en la posición '{'
        indice_fin = Nodo.char_a_indice('{')
        nodo_actual.hijos[indice_fin] = nodo_actual
    
    def borre(self, elemento):
        """
        Borra una palabra del Trie.
        
        Args:
            elemento (str): La palabra a borrar
        """
        if not elemento:
            return
        
        self._borre_en(self.raiz, elemento.lower(), 0)
    
    def _borre_en(self, nodo, palabra, i):
        """
        Función auxiliar recursiva para borrar una palabra.
        
        Args:
            nodo (Nodo): El nodo actual
            palabra (str): La palabra a borrar
            i (int): El índice actual en la palabra (empieza en 0)
            
        Returns:
            bool: True si el nodo actual debe ser eliminado
        """
        if i == len(palabra):
            # Llegamos al final de la palabra
            indice_fin = Nodo.char_a_indice('{')
            
            # Verificar si es realmente fin de palabra
            if nodo.hijos[indice_fin] != nodo:
                return False  # La palabra no existe
            
            # Desmarcar como fin de palabra:
            nodo.hijos[indice_fin] = None
            
            # Contar cuántos hijos tiene (sin contar '{')
            contador = 0
            for j in range(26):  # Solo 'a' a 'z'
                if nodo.hijos[j] is not None:
                    contador += 1
            
            # Si no tiene hijos, el nodo puede ser eliminado
            return contador == 0
        
        caracter = palabra[i]
        indice = Nodo.char_a_indice(caracter)
        
        # Si el hijo no existe, la palabra no está en el Trie
        if nodo.hijos[indice] is None:
            return False
        
        # Recursivamente borre en el siguiente nivel
        hijo = nodo.hijos[indice]
        debe_eliminar_hijo = self._borre_en(hijo, palabra, i + 1)
        
        # Si el hijo debe ser eliminado, eliminarlo
        if debe_eliminar_hijo:
            nodo.hijos[indice] = None
            
            # Contar hijos restantes (sin contar '{')
            contador = 0
            for j in range(26):
                if nodo.hijos[j] is not None:
                    contador += 1
            
            # Si este nodo no tiene hijos y no es fin de palabra, también puede eliminarse
            indice_fin = Nodo.char_a_indice('{')
            es_fin = nodo.hijos[indice_fin] == nodo
            
            return contador == 0 and not es_fin
        
        return False
    
    def miembro(self, elemento):
        """
        Verifica si una palabra existe en el Trie.
                
        Args:
            palabra (str): La palabra a buscar
            
        Returns:
            bool: True si la palabra existe, False en caso contrario
        """
        if not elemento:
            return False
        
        nodo_actual = self.raiz
        encontrado = True
        
        # Recorrer cada carácter de la palabra
        for caracter in elemento.lower():
            if 'a' <= caracter <= 'z':
                indice = Nodo.char_a_indice(caracter)
                
                # Si el hijo no existe (es None), la palabra no está
                if nodo_actual.hijos[indice] is None:
                    encontrado = False
                    break
                
                # Moverse al siguiente nodo
                nodo_actual = nodo_actual.hijos[indice]
        
        if not encontrado:
            return False
        
        # Verificar si es un fin de palabra:
        indice_fin = Nodo.char_a_indice('{')
        return nodo_actual.hijos[indice_fin] == nodo_actual
    
    def imprima(self):
        """
        Imprime todas las palabras almacenadas en el Trie en orden alfabético.
        
        """
        self._imprima_desde(self.raiz, "")
    
    def _imprima_desde(self, nodo, prefijo):
        """
        Función auxiliar recursiva para imprimir palabras.
        
        Args:
            nodo (Nodo): El nodo actual
            prefijo (str): El prefijo acumulado hasta este nodo
        """
        # Verificar si este nodo marca fin de palabra:
        indice_fin = Nodo.char_a_indice('{')
        if nodo.hijos[indice_fin] == nodo:
            print(prefijo)
        
        # Recorrer todos los caracteres de 'a' a 'z'
        for i in range(26):  # 0='a' hasta 25='z'
            if nodo.hijos[i] is not None:
                caracter = Nodo.indice_a_char(i)
                self._imprima_desde(nodo.hijos[i], prefijo + caracter)
    
    def obtener_palabras(self):
        """
        Retorna una lista con todas las palabras en el Trie.
        
        Returns:
            list: Lista de palabras en orden alfabético
        """
        palabras = []
        self._recolectar_palabras(self.raiz, "", palabras)
        return palabras
    
    def _recolectar_palabras(self, nodo, prefijo, palabras):
        """
        Función auxiliar recursiva para recolectar palabras.
        
        Args:
            nodo (Nodo): El nodo actual
            prefijo (str): El prefijo acumulado
            palabras (list): Lista donde se acumulan las palabras
        """
        indice_fin = Nodo.char_a_indice('{')
        if nodo.hijos[indice_fin] == nodo:
            palabras.append(prefijo)
        
        for i in range(26):
            if nodo.hijos[i] is not None:
                caracter = Nodo.indice_a_char(i)
                self._recolectar_palabras(nodo.hijos[i], prefijo + caracter, palabras)
    
    def buscar_con_prefijo(self, prefijo):
        """
        Encuentra todas las palabras que comienzan con un prefijo dado.
        Método adicional no presente en el código Pascal original.
        
        Args:
            prefijo (str): El prefijo a buscar
            
        Returns:
            list: Lista de palabras que comienzan con el prefijo
        """
        if not prefijo:
            return self.obtener_palabras()
        
        nodo_actual = self.raiz
        
        # Navegar hasta el nodo del prefijo
        for caracter in prefijo.lower():
            if 'a' <= caracter <= 'z':
                indice = Nodo.char_a_indice(caracter)
                if nodo_actual.hijos[indice] is None:
                    return []  # El prefijo no existe
                nodo_actual = nodo_actual.hijos[indice]
        
        # Recolectar todas las palabras desde este nodo
        palabras = []
        self._recolectar_palabras(nodo_actual, prefijo.lower(), palabras)
        return palabras
    
    def __contains__(self, palabra):
        """
        Permite usar el operador 'in' para verificar membresía.
        Ejemplo: if "casa" in trie: ...
        """
        return self.miembro(palabra)
    
    def __len__(self):
        """
        Retorna el número de palabras en el Trie.
        """
        return len(self.obtener_palabras())
    
    def __repr__(self):
        """
        Representación en cadena del Trie.
        """
        palabras = self.obtener_palabras()
        return f"TrieArreglos({len(palabras)} palabras: {palabras})"

    def __str__(self) -> str:
        return str(self.obtener_palabras)
