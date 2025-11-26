from fastapi import APIRouter, HTTPException
from schemas import ServicioCreate, ServicioUpdate
from repositories import ServicioRepository, EmpleadoRepository
from services.servicio_service import ServicioService

router = APIRouter()
service = ServicioService()

@router.get("/api/servicios")
def get_servicios():
    return service.listar_servicios()

@router.post("/api/servicios")
def create_servicio(data: ServicioCreate):
    new_id = service.registrar_servicio(data)
    return {"mensaje": "Servicio registrado", "id": new_id}

@router.put("/api/servicios/{id_servicio}")
def update_servicio(id_servicio: int, data: ServicioUpdate):
    resultado = service.actualizar_servicio(id_servicio, data)
    if not resultado:
        return {"mensaje": "No hubo cambios"}
    return {"mensaje": "Servicio actualizado correctamente"}

@router.delete("/api/servicios/{id_servicio}")
def cancelar_servicio(id_servicio: int):
    service.cancelar_servicio(id_servicio)
    return {"mensaje": "Servicio cancelado"}