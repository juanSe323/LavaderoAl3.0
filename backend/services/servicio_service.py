from fastapi import HTTPException
# Importamos el repositorio de convenios
from repositories import ServicioRepository, EmpleadoRepository, ConvenioRepository
from services.calculo_service import CalculoService
from schemas import ServicioCreate, ServicioUpdate

class ServicioService:
    def __init__(self):
        # Instanciamos todos los repositorios necesarios
        self.servicio_repo = ServicioRepository()
        self.empleado_repo = EmpleadoRepository()
        self.convenio_repo = ConvenioRepository()
        self.calculo_service = CalculoService()

    def listar_servicios(self):
        return self.servicio_repo.get_all()

    def registrar_servicio(self, data: ServicioCreate):
        # 1. Validar Empleado
        empleado = self.empleado_repo.get_by_id(data.id_empleado)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # 2. Lógica de Convenios (PATRÓN STRATEGY APLICADO)
        monto_descuento_final = 0.0
        
        if data.id_convenio:
            # Buscamos los detalles del convenio en la BD
            convenio = self.convenio_repo.get_by_id(data.id_convenio)
            
            if convenio and convenio['estado'] == 'activo':
                # El servicio de cálculo usa la estrategia internamente
                monto_descuento_final = self.calculo_service.calcular_descuento_final(
                    precio_lista=data.monto_total,
                    tipo_descuento=convenio['tipo_descuento'],
                    valor_descuento=convenio['valor_descuento']
                )
        
        # Decisión de negocio: Si viene un descuento manual, ¿usamos ese o el del convenio?
        # Aquí damos prioridad al del convenio si existe, sino usamos el manual.
        descuento_real = monto_descuento_final if data.id_convenio else (data.descuento or 0.0)

        # 3. Calcular Comisión (Sobre el precio final con descuento aplicado)
        precio_final = data.monto_total - descuento_real
        monto_comision = self.calculo_service.calcular_comision(
            precio_final, 
            empleado['porcentaje_comision']
        )
        
        # 4. Guardar
        try:
            new_id = self.servicio_repo.create(
                data, 
                monto_comision, 
                1 if data.id_convenio else 0, 
                descuento_real
            )
            return new_id
        except Exception as e:
            print(f"Error DB: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    def actualizar_servicio(self, id_servicio: int, data: ServicioUpdate):
        # 1. Verificar existencia
        actual = self.servicio_repo.get_by_id(id_servicio)
        if not actual:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # 2. Construir query dinámica
        campos = []
        vals = []

        if data.placa: 
            campos.append("placa=%s")
            vals.append(data.placa.upper())
        if data.tipo_vehiculo: 
            campos.append("tipo_vehiculo=%s")
            vals.append(data.tipo_vehiculo)
        if data.tipo_servicio: 
            campos.append("tipo_servicio=%s")
            vals.append(data.tipo_servicio)
        if data.monto_total is not None: 
            campos.append("monto_total=%s")
            vals.append(data.monto_total)
        if data.id_empleado is not None: 
            campos.append("id_empleado=%s")
            vals.append(data.id_empleado)
        if data.observaciones is not None: 
            campos.append("observaciones=%s")
            vals.append(data.observaciones)

        # 3. Recalcular comisión si cambia monto o empleado
        if data.monto_total is not None or data.id_empleado is not None:
            nuevo_monto = data.monto_total if data.monto_total is not None else actual['monto_total']
            nuevo_emp_id = data.id_empleado if data.id_empleado is not None else actual['id_empleado']
            
            empleado = self.empleado_repo.get_by_id(nuevo_emp_id)
            if empleado:
                # Nota: En edición simple no estamos recalculando estrategia de convenio 
                # para no complicar, asumimos el descuento que ya tenía o 0 si no se envía.
                nueva_comision = self.calculo_service.calcular_comision(
                    float(nuevo_monto), # Calcula sobre el monto bruto (o ajusta según tu regla)
                    empleado['porcentaje_comision']
                )
                campos.append("monto_comision=%s")
                vals.append(nueva_comision)

        if not campos:
            return False

        # 4. Persistencia
        try:
            self.servicio_repo.update_dynamic(id_servicio, campos, vals)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def cancelar_servicio(self, id_servicio: int):
        try:
            rows = self.servicio_repo.cancel(id_servicio)
            if rows == 0:
                raise HTTPException(status_code=404, detail="Servicio no encontrado")
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))