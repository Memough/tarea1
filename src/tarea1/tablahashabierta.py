from diccionario import Diccionario

def _poli_hash(s: str, mod: int) -> int:
    """Función hash polinómica base 27 sobre 'a'..'z'."""
    h = 0
    base = 27
    for ch in s:
        h = (h * base + (ord(ch) - 96)) % mod  # 'a'->1
    return h

class TablaHashAbierta(Diccionario):
    """Implementación de Tabla Hash Abierta, permite duplicados, usa rehash si factor de carga > 0.75"""

    def __init__(self, capacidad: int = 8, lf_max: float = 0.75):
        self._cap = max(8, capacidad)
        self._buckets: list[list[str]] = [[] for _ in range(self._cap)]
        self._n = 0
        self._lf_max = lf_max

    # utilidades internas
    def _idx(self, s: str, cap: int | None = None) -> int:
        m = self._cap if cap is None else cap
        return _poli_hash(s, m)

    def _rehash_si_necesario(self):
        if self._n / self._cap <= self._lf_max:
            return
        old_buckets = self._buckets
        self._cap *= 2
        self._buckets = [[] for _ in range(self._cap)]
        for bucket in old_buckets:
            for key in bucket:
                self._buckets[self._idx(key)].append(key)

    # operaciones del modelo 
    def inserte(self, elemento: str) -> None:
        self._buckets[self._idx(elemento)].append(elemento)
        self._n += 1
        self._rehash_si_necesario()

    def borre(self, elemento: str) -> bool:
        b = self._buckets[self._idx(elemento)]
        for i, v in enumerate(b):
            if v == elemento:
                b.pop(i)
                self._n -= 1
                return True
        return False

    def miembro(self, elemento: str) -> bool:
        b = self._buckets[self._idx(elemento)]
        return any(v == elemento for v in b)

    def limpie(self) -> None:
        self._buckets = [[] for _ in range(self._cap)]
        self._n = 0

    def imprima(self) -> None:
        print(self)

    def __str__(self) -> str:
        out = []
        for b in self._buckets:
            out.extend(b)
        return "\n".join(out)

    def __del__(self):
        self.limpie()
