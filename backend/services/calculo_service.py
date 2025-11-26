from typing import Optional
from strategies import DescuentoContext

class CalculoService:
    """
    Servicio encargado de lógica matemática usando el Patrón Strategy.
    """

    @staticmethod
    def calcular_comision(monto_total: float, porcentaje_comision: int) -> int:
        if monto_total < 0 or porcentaje_comision < 0:
            return 0
        return int(monto_total * (porcentaje_comision / 100))

    @staticmethod
    def preparar_datos_convenio(id_convenio: int | None, descuento: float | None):
        """
        Determina las banderas y valores para un servicio de convenio.
        Acepta None para evitar errores de validación de tipos.
        """
        es_convenio = 1 if id_convenio else 0
        monto_descuento = descuento if descuento else 0.0
        return es_convenio, monto_descuento

    # --- NUEVO: Lógica de Strategy ---
    @staticmethod
    def calcular_descuento_final(precio_lista: float, tipo_descuento: str | None, valor_descuento: float | None) -> float:
        """
        Calcula el monto exacto del descuento usando la estrategia adecuada (Porcentaje o Fijo).
        """
        # 1. Obtener la estrategia correcta
        estrategia = DescuentoContext.obtener_estrategia(tipo_descuento)
        
        # 2. Ejecutar cálculo
        valor = valor_descuento if valor_descuento else 0
        return estrategia.calcular(precio_lista, valor)