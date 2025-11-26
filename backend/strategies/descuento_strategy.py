from abc import ABC, abstractmethod

# 1. La Interfaz (Estrategia Abstracta)
class DescuentoStrategy(ABC):
    @abstractmethod
    def calcular(self, precio_lista: float, valor_descuento: float) -> float:
        """Devuelve el monto monetario a descontar"""
        pass

# 2. Estrategias Concretas

class DescuentoPorcentaje(DescuentoStrategy):
    def calcular(self, precio_lista: float, valor_descuento: float) -> float:
        # Ejemplo: 10000 * 10% = 1000
        return int(precio_lista * (valor_descuento / 100))

class DescuentoFijo(DescuentoStrategy):
    def calcular(self, precio_lista: float, valor_descuento: float) -> float:
        # Ejemplo: Descuento de $2000 fijos. No puede ser mayor al precio.
        descuento = int(valor_descuento)
        return min(descuento, int(precio_lista))

class SinDescuento(DescuentoStrategy):
    def calcular(self, precio_lista: float, valor_descuento: float) -> float:
        return 0

# 3. El Contexto (Factory) para elegir la estrategia
class DescuentoContext:
    _strategies = {
        'porcentaje': DescuentoPorcentaje(),
        'monto_fijo': DescuentoFijo()
    }
    _default = SinDescuento()

    @classmethod
    def obtener_estrategia(cls, tipo_descuento: str | None) -> DescuentoStrategy:
        if not tipo_descuento:
            return cls._default
        return cls._strategies.get(str(tipo_descuento).lower(), cls._default)