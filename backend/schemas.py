from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date
import re

# --- LOGIN / USUARIOS ---
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    rol: Optional[str] = Field(default='usuario')

# --- EMPLEADOS ---
class EmpleadoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    cedula: str = Field(..., min_length=5, max_length=15) # Adaptado para Cédula/NIT
    telefono: str = Field(..., min_length=7, max_length=15)
    email: Optional[str] = None
    porcentaje_comision: int = Field(..., ge=0, le=100)

    @validator('telefono')
    def validate_telefono_col(cls, v):
        # Validación flexible para Colombia (ej: 3001234567 o +57...)
        v_clean = v.replace('+', '').replace(' ', '').replace('-', '')
        if not v_clean.isdigit():
             raise ValueError('El teléfono solo debe contener números')
        return v

# --- SERVICIOS ---
class ServicioCreate(BaseModel):
    placa: str = Field(..., min_length=5, max_length=10)
    tipo_vehiculo: str
    tipo_servicio: str
    monto_total: float = Field(..., ge=0)
    id_empleado: int = Field(..., gt=0)
    
    # Campos opcionales para convenios
    id_convenio: Optional[int] = None
    descuento: Optional[float] = 0
    observaciones: Optional[str] = None

    @validator('placa')
    def uppercase_placa(cls, v):
        return v.upper().replace(' ', '').replace('-', '')

# CLASE QUE FALTABA (Corrige el ImportError)
class ServicioUpdate(BaseModel):
    placa: Optional[str] = None
    tipo_vehiculo: Optional[str] = None
    tipo_servicio: Optional[str] = None
    monto_total: Optional[float] = None
    id_empleado: Optional[int] = None
    observaciones: Optional[str] = None

# --- INVENTARIO ---
class InsumoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    categoria: str
    stock: float = Field(..., ge=0)
    stock_minimo: float = Field(..., ge=0)
    precio_unitario: float = Field(..., gt=0)
    unidad: str
    descripcion: Optional[str] = None

class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    stock: Optional[float] = None
    stock_minimo: Optional[float] = None
    precio_unitario: Optional[float] = None
    unidad: Optional[str] = None
    descripcion: Optional[str] = None

class MovimientoInventario(BaseModel):
    id_insumo: int
    tipo_movimiento: str # entrada, salida, ajuste
    cantidad: float
    motivo: Optional[str] = None
    usuario: str

# --- CONVENIOS ---
class ConvenioCreate(BaseModel):
    nombre_empresa: str
    nit_empresa: str = Field(..., min_length=6, max_length=15) # CORREGIDO: nit_empresa
    contacto: Optional[str] = None
    telefono: str
    email: EmailStr
    direccion: Optional[str] = None
    tipo_descuento: str # porcentaje, monto_fijo
    valor_descuento: float
    fecha_inicio: date
    fecha_termino: Optional[date] = None
    observaciones: Optional[str] = None

class ConvenioUpdate(BaseModel):
    nombre_empresa: Optional[str] = None
    nit_empresa: Optional[str] = None # CORREGIDO: nit_empresa
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    tipo_descuento: Optional[str] = None
    valor_descuento: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_termino: Optional[date] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class VehiculoConvenioCreate(BaseModel):
    # id_convenio no es necesario en el body si se pasa por URL
    placa: str
    tipo_vehiculo: str
    modelo: Optional[str] = None
    color: Optional[str] = None

# --- TARIFAS ---
class TarifaUpdate(BaseModel):
    precio: float = Field(..., gt=0)

# --- LIQUIDACIONES ---
class LiquidacionCreate(BaseModel):
    id_empleado: int
    periodo_inicio: date
    periodo_fin: date