from fastapi import APIRouter, HTTPException
from schemas import EmpleadoCreate
from repositories import EmpleadoRepository

router = APIRouter()
repo = EmpleadoRepository()

@router.get("/api/empleados")
def get_empleados():
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/empleados")
def create_empleado(empleado: EmpleadoCreate):
    try:
        if repo.get_by_cedula(empleado.cedula):
            raise HTTPException(status_code=400, detail="Ya existe un empleado con esta Cédula")
        new_id = repo.create(empleado)
        return {"message": "Empleado creado", "id": new_id}
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/empleados/{id_empleado}")
def update_empleado(id_empleado: int, empleado: EmpleadoCreate):
    try:
        existente = repo.get_by_cedula(empleado.cedula)
        if existente and existente['id'] != id_empleado:
            raise HTTPException(status_code=400, detail="Cédula duplicada")
        
        rows = repo.update(id_empleado, empleado)
        if rows == 0: raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"mensaje": "Empleado actualizado"}
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/empleados/{id_empleado}")
def delete_empleado(id_empleado: int):
    try:
        rows = repo.soft_delete(id_empleado)
        if rows == 0: raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"mensaje": "Empleado desactivado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))