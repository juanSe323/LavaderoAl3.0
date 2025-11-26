from fastapi import APIRouter, HTTPException
from schemas import ConvenioCreate, ConvenioUpdate, VehiculoConvenioCreate
from repositories import ConvenioRepository

router = APIRouter()
repo = ConvenioRepository()

@router.get("/api/convenios")
def get_convenios():
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/convenios")
def create_convenio(convenio: ConvenioCreate):
    try:
        new_id = repo.create(convenio)
        return {"mensaje": "Convenio creado", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/convenios/{id_convenio}")
def update_convenio(id_convenio: int, convenio: ConvenioUpdate):
    try:
        campos, valores = [], []
        if convenio.nombre_empresa: campos.append("nombre_empresa=%s"); valores.append(convenio.nombre_empresa)
        if convenio.nit_empresa: campos.append("nit_empresa=%s"); valores.append(convenio.nit_empresa)
        if convenio.contacto: campos.append("contacto=%s"); valores.append(convenio.contacto)
        if convenio.telefono: campos.append("telefono=%s"); valores.append(convenio.telefono)
        if convenio.email: campos.append("email=%s"); valores.append(convenio.email)
        if convenio.tipo_descuento: campos.append("tipo_descuento=%s"); valores.append(convenio.tipo_descuento)
        if convenio.valor_descuento is not None: campos.append("valor_descuento=%s"); valores.append(convenio.valor_descuento)
        if convenio.fecha_inicio: campos.append("fecha_inicio=%s"); valores.append(convenio.fecha_inicio)
        if convenio.fecha_termino: campos.append("fecha_termino=%s"); valores.append(convenio.fecha_termino)
        if convenio.estado: campos.append("estado=%s"); valores.append(convenio.estado)
        
        if not campos: return {"mensaje": "Sin cambios"}
        
        repo.update_dynamic(id_convenio, campos, valores)
        return {"mensaje": "Convenio actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/convenios/{id_convenio}")
def delete_convenio(id_convenio: int):
    try:
        rows = repo.soft_delete(id_convenio)
        if rows == 0: raise HTTPException(status_code=404, detail="Convenio no encontrado")
        return {"mensaje": "Convenio desactivado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/convenios/{id_convenio}/vehiculos")
def add_vehiculo_convenio(id_convenio: int, vehiculo: VehiculoConvenioCreate):
    try:
        if repo.check_vehiculo_activo(vehiculo.placa):
            raise HTTPException(status_code=400, detail="Esta placa ya tiene un convenio activo")
        
        new_id = repo.add_vehiculo(id_convenio, vehiculo)
        return {"mensaje": "Vehículo agregado", "id": new_id}
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/convenios/{id_convenio}/vehiculos")
def get_vehiculos_convenio(id_convenio: int):
    try:
        return repo.get_vehiculos(id_convenio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/convenios/vehiculos/{id_vehiculo}")
def remove_vehiculo_convenio(id_vehiculo: int):
    try:
        repo.remove_vehiculo(id_vehiculo)
        return {"mensaje": "Vehículo eliminado del convenio"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/convenios/validar/{placa}")
def validar_convenio_placa(placa: str):
    """Valida si una placa pertenece a un convenio activo"""
    try:
        convenio = repo.validar_placa(placa)
        if convenio:
            return {"tiene_convenio": True, "convenio": convenio}
        return {"tiene_convenio": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))