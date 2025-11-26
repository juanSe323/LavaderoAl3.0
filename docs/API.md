# 📡 Documentación de API - Lavadero AL

## Tabla de Contenidos

- [Información General](#información-general)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
  - [Autenticación](#endpoints-autenticación)
  - [Empleados](#endpoints-empleados)
  - [Servicios](#endpoints-servicios)
  - [Inventario](#endpoints-inventario)
  - [Convenios](#endpoints-convenios)
  - [Tarifas](#endpoints-tarifas)
  - [Liquidaciones](#endpoints-liquidaciones)
  - [Reportes](#endpoints-reportes)
  - [Dashboard](#endpoints-dashboard)
- [Códigos de Estado](#códigos-de-estado)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Información General

### URL Base

```
http://localhost:8000
```

### Formato de Datos

- **Request:** JSON (`application/json`)
- **Response:** JSON (`application/json`)

### Versión de la API

**v1.0.0**

### Documentación Interactiva

FastAPI proporciona documentación interactiva automática:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Autenticación

La API utiliza **Bearer Token Authentication** mediante JWT (JSON Web Tokens).

### Cómo obtener un token

1. Realiza una petición POST a `/api/login` con credenciales válidas
2. El servidor retorna un token JWT
3. Incluye el token en el header `Authorization` de las peticiones subsiguientes

### Formato del Header

```http
Authorization: Bearer <tu-token-jwt>
```

### Ejemplo

```javascript
// Obtener token
const response = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const { token } = await response.json();

// Usar token en peticiones
const empleados = await fetch('http://localhost:8000/api/empleados', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

---

## Endpoints

## Endpoints: Autenticación

### POST `/api/login`

Autenticar usuario y obtener token JWT.

**Autenticación requerida:** No

**Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "admin",
    "rol": "admin"
  }
}
```

**Errores:**
- `401` - Credenciales incorrectas
- `500` - Error del servidor

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

---

### POST `/api/register`

Registrar un nuevo usuario.

**Autenticación requerida:** Sí (Solo admin)

**Body:**
```json
{
  "username": "string",
  "password": "string",
  "rol": "usuario"  // opcional, por defecto "usuario"
}
```

**Validaciones:**
- `username`: mínimo 3 caracteres, máximo 50
- `password`: mínimo 8 caracteres
- `rol`: "admin" o "usuario"

**Respuesta exitosa (200):**
```json
{
  "message": "Usuario creado exitosamente",
  "id": 5
}
```

**Errores:**
- `400` - El usuario ya existe
- `401` - No autorizado
- `422` - Datos de validación incorrectos

---

## Endpoints: Empleados

### GET `/api/empleados`

Obtener lista de todos los empleados.

**Autenticación requerida:** Sí

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "cedula": "1234567890",
    "telefono": "3001234567",
    "email": "juan@email.com",
    "porcentaje_comision": 15,
    "activo": true,
    "fecha_registro": "2024-01-15"
  }
]
```

**Ejemplo cURL:**
```bash
curl http://localhost:8000/api/empleados \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### POST `/api/empleados`

Crear un nuevo empleado.

**Autenticación requerida:** Sí

**Body:**
```json
{
  "nombre": "María García",
  "cedula": "9876543210",
  "telefono": "3109876543",
  "email": "maria@email.com",
  "porcentaje_comision": 20
}
```

**Validaciones:**
- `nombre`: mínimo 3 caracteres, máximo 100
- `cedula`: mínimo 5 caracteres, máximo 15, única
- `telefono`: solo números (puede incluir +, -, espacios)
- `porcentaje_comision`: entre 0 y 100

**Respuesta exitosa (200):**
```json
{
  "message": "Empleado creado",
  "id": 5
}
```

**Errores:**
- `400` - Ya existe un empleado con esta Cédula
- `422` - Datos de validación incorrectos

---

### PUT `/api/empleados/{id_empleado}`

Actualizar información de un empleado.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_empleado` (integer): ID del empleado

**Body:** Misma estructura que POST

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Empleado actualizado"
}
```

**Errores:**
- `404` - Empleado no encontrado
- `400` - Cédula duplicada

---

### PUT `/api/empleados/{id_empleado}/reactivar`

Reactivar un empleado desactivado.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_empleado` (integer): ID del empleado

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Empleado reactivado exitosamente"
}
```

---

### DELETE `/api/empleados/{id_empleado}`

Desactivar un empleado (soft delete).

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_empleado` (integer): ID del empleado

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Empleado desactivado"
}
```

**Nota:** Esta operación no elimina el empleado, solo lo marca como inactivo.

---

## Endpoints: Servicios

### GET `/api/servicios`

Obtener lista de servicios realizados.

**Autenticación requerida:** Sí

**Query Parameters:**
- `limite` (opcional): Número máximo de resultados (default: 50)
- `fecha_inicio` (opcional): Filtrar desde fecha (formato: YYYY-MM-DD)
- `fecha_fin` (opcional): Filtrar hasta fecha (formato: YYYY-MM-DD)

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "placa": "ABC123",
    "tipo_vehiculo": "Auto",
    "tipo_servicio": "Lavado completo",
    "monto_total": 25000,
    "id_empleado": 1,
    "nombre_empleado": "Juan Pérez",
    "fecha": "2024-01-15 10:30:00",
    "id_convenio": null,
    "descuento": 0,
    "observaciones": null
  }
]
```

**Ejemplo:**
```bash
curl "http://localhost:8000/api/servicios?limite=10&fecha_inicio=2024-01-01" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### POST `/api/servicios`

Registrar un nuevo servicio.

**Autenticación requerida:** Sí

**Body:**
```json
{
  "placa": "ABC123",
  "tipo_vehiculo": "Auto",
  "tipo_servicio": "Lavado completo",
  "monto_total": 25000,
  "id_empleado": 1,
  "id_convenio": null,
  "descuento": 0,
  "observaciones": "Cliente frecuente"
}
```

**Validaciones:**
- `placa`: 5-10 caracteres, se convierte a mayúsculas
- `tipo_vehiculo`: Auto, SUV, Camioneta, Camión
- `monto_total`: mayor a 0
- `id_empleado`: debe existir en base de datos
- `descuento`: mayor o igual a 0

**Respuesta exitosa (200):**
```json
{
  "message": "Servicio registrado",
  "id": 15
}
```

---

## Endpoints: Inventario

### GET `/api/inventario`

Obtener lista de insumos en inventario.

**Autenticación requerida:** Sí

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre": "Champú Premium",
    "categoria": "Limpieza",
    "stock": 50.5,
    "stock_minimo": 10,
    "precio_unitario": 15000,
    "unidad": "Litro",
    "descripcion": "Champú concentrado para vehículos",
    "estado_stock": "normal"  // normal, bajo, critico
  }
]
```

---

### POST `/api/inventario`

Agregar un nuevo insumo al inventario.

**Autenticación requerida:** Sí

**Body:**
```json
{
  "nombre": "Cera líquida",
  "categoria": "Acabado",
  "stock": 30,
  "stock_minimo": 5,
  "precio_unitario": 35000,
  "unidad": "Litro",
  "descripcion": "Cera protectora de larga duración"
}
```

**Validaciones:**
- `nombre`: mínimo 3 caracteres, máximo 100
- `stock`: mayor o igual a 0
- `precio_unitario`: mayor a 0

**Respuesta exitosa (200):**
```json
{
  "message": "Insumo agregado",
  "id": 8
}
```

---

### PUT `/api/inventario/{id_insumo}`

Actualizar información de un insumo.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_insumo` (integer): ID del insumo

**Body:** Campos opcionales para actualizar

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Insumo actualizado"
}
```

---

### POST `/api/inventario/movimiento`

Registrar un movimiento de inventario (entrada/salida/ajuste).

**Autenticación requerida:** Sí

**Body:**
```json
{
  "id_insumo": 1,
  "tipo_movimiento": "salida",
  "cantidad": 5.5,
  "motivo": "Uso en servicio",
  "usuario": "admin"
}
```

**Tipos de movimiento:**
- `entrada`: Ingreso de stock
- `salida`: Consumo de stock
- `ajuste`: Corrección de inventario

**Respuesta exitosa (200):**
```json
{
  "message": "Movimiento registrado",
  "stock_actual": 45.0
}
```

---

### GET `/api/inventario/{id_insumo}/movimientos`

Obtener historial de movimientos de un insumo.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_insumo` (integer): ID del insumo

**Respuesta exitosa (200):**
```json
[
  {
    "id": 15,
    "tipo_movimiento": "salida",
    "cantidad": 5.5,
    "stock_anterior": 50.5,
    "stock_nuevo": 45.0,
    "motivo": "Uso en servicio",
    "usuario": "admin",
    "fecha": "2024-01-15 14:30:00"
  }
]
```

---

## Endpoints: Convenios

### GET `/api/convenios`

Obtener lista de convenios.

**Autenticación requerida:** Sí

**Query Parameters:**
- `estado` (opcional): activo, inactivo, vencido

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre_empresa": "Transportes XYZ",
    "nit_empresa": "900123456",
    "contacto": "Carlos López",
    "telefono": "3201234567",
    "email": "contacto@transportesxyz.com",
    "direccion": "Calle 123 #45-67",
    "tipo_descuento": "porcentaje",
    "valor_descuento": 15,
    "fecha_inicio": "2024-01-01",
    "fecha_termino": "2024-12-31",
    "estado": "activo",
    "observaciones": null,
    "cantidad_vehiculos": 5
  }
]
```

---

### POST `/api/convenios`

Crear un nuevo convenio.

**Autenticación requerida:** Sí

**Body:**
```json
{
  "nombre_empresa": "Transportes ABC",
  "nit_empresa": "900987654",
  "contacto": "Ana Martínez",
  "telefono": "3109876543",
  "email": "ana@transportesabc.com",
  "direccion": "Avenida 80 #10-20",
  "tipo_descuento": "monto_fijo",
  "valor_descuento": 5000,
  "fecha_inicio": "2024-02-01",
  "fecha_termino": "2024-12-31",
  "observaciones": "Renovación automática"
}
```

**Tipos de descuento:**
- `porcentaje`: Descuento en porcentaje (0-100)
- `monto_fijo`: Descuento en valor absoluto

**Respuesta exitosa (200):**
```json
{
  "message": "Convenio creado",
  "id": 4
}
```

---

### GET `/api/convenios/{id_convenio}/vehiculos`

Obtener vehículos asociados a un convenio.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_convenio` (integer): ID del convenio

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "placa": "XYZ789",
    "tipo_vehiculo": "Camioneta",
    "modelo": "Toyota Hilux 2022",
    "color": "Blanco",
    "fecha_registro": "2024-01-05"
  }
]
```

---

### POST `/api/convenios/{id_convenio}/vehiculos`

Agregar un vehículo a un convenio.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_convenio` (integer): ID del convenio

**Body:**
```json
{
  "placa": "DEF456",
  "tipo_vehiculo": "Camión",
  "modelo": "Chevrolet NPR 2023",
  "color": "Azul"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Vehículo agregado al convenio",
  "id": 8
}
```

---

## Endpoints: Tarifas

### GET `/api/tarifas`

Obtener lista de tarifas por tipo de vehículo.

**Autenticación requerida:** Sí

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "tipo_vehiculo": "Auto",
    "precio": 20000
  },
  {
    "id": 2,
    "tipo_vehiculo": "SUV",
    "precio": 30000
  },
  {
    "id": 3,
    "tipo_vehiculo": "Camioneta",
    "precio": 35000
  },
  {
    "id": 4,
    "tipo_vehiculo": "Camión",
    "precio": 50000
  }
]
```

---

### PUT `/api/tarifas/{tipo_vehiculo}`

Actualizar tarifa para un tipo de vehículo.

**Autenticación requerida:** Sí (Solo admin)

**Parámetros de ruta:**
- `tipo_vehiculo` (string): Auto, SUV, Camioneta, Camión

**Body:**
```json
{
  "precio": 25000
}
```

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Tarifa actualizada",
  "tipo_vehiculo": "Auto",
  "precio_nuevo": 25000
}
```

---

## Endpoints: Liquidaciones

### GET `/api/liquidaciones`

Obtener lista de liquidaciones.

**Autenticación requerida:** Sí

**Query Parameters:**
- `estado` (opcional): pendiente, pagada
- `id_empleado` (opcional): Filtrar por empleado

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "id_empleado": 1,
    "nombre_empleado": "Juan Pérez",
    "periodo_inicio": "2024-01-01",
    "periodo_fin": "2024-01-15",
    "total_servicios": 10,
    "monto_total": 250000,
    "total_comision": 37500,
    "estado": "pagada",
    "fecha_pago": "2024-01-16",
    "fecha_creacion": "2024-01-15 18:00:00"
  }
]
```

---

### POST `/api/liquidaciones`

Crear una nueva liquidación para un empleado.

**Autenticación requerida:** Sí

**Body:**
```json
{
  "id_empleado": 1,
  "periodo_inicio": "2024-02-01",
  "periodo_fin": "2024-02-15"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Liquidación creada",
  "id": 5,
  "total_servicios": 12,
  "monto_total": 300000,
  "total_comision": 45000
}
```

**Nota:** El sistema calcula automáticamente los totales basándose en los servicios del empleado en el período especificado.

---

### GET `/api/liquidaciones/{id_liquidacion}/detalle`

Obtener detalle de servicios de una liquidación.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_liquidacion` (integer): ID de la liquidación

**Respuesta exitosa (200):**
```json
{
  "liquidacion": {
    "id": 1,
    "periodo_inicio": "2024-01-01",
    "periodo_fin": "2024-01-15",
    "total_comision": 37500,
    "estado": "pagada"
  },
  "servicios": [
    {
      "id_servicio": 5,
      "fecha": "2024-01-05",
      "placa": "ABC123",
      "tipo_servicio": "Lavado completo",
      "monto": 25000,
      "comision": 3750
    }
  ]
}
```

---

### PUT `/api/liquidaciones/{id_liquidacion}/pagar`

Marcar una liquidación como pagada.

**Autenticación requerida:** Sí

**Parámetros de ruta:**
- `id_liquidacion` (integer): ID de la liquidación

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Liquidación marcada como pagada",
  "fecha_pago": "2024-01-20"
}
```

---

## Endpoints: Reportes

### GET `/api/reportes/servicios`

Generar reporte de servicios por período.

**Autenticación requerida:** Sí

**Query Parameters:**
- `fecha_inicio` (requerido): YYYY-MM-DD
- `fecha_fin` (requerido): YYYY-MM-DD
- `tipo_vehiculo` (opcional): Filtrar por tipo
- `id_empleado` (opcional): Filtrar por empleado

**Respuesta exitosa (200):**
```json
{
  "periodo": {
    "inicio": "2024-01-01",
    "fin": "2024-01-31"
  },
  "resumen": {
    "total_servicios": 150,
    "monto_total": 4500000,
    "promedio_por_servicio": 30000
  },
  "por_tipo_vehiculo": {
    "Auto": { "cantidad": 80, "monto": 2000000 },
    "SUV": { "cantidad": 40, "monto": 1500000 },
    "Camioneta": { "cantidad": 20, "monto": 700000 },
    "Camión": { "cantidad": 10, "monto": 300000 }
  },
  "por_empleado": [
    {
      "id_empleado": 1,
      "nombre": "Juan Pérez",
      "servicios": 50,
      "monto_total": 1500000
    }
  ]
}
```

---

### GET `/api/reportes/inventario`

Reporte de estado del inventario.

**Autenticación requerida:** Sí

**Respuesta exitosa (200):**
```json
{
  "resumen": {
    "total_insumos": 15,
    "valor_total_inventario": 2500000,
    "items_bajo_stock": 3,
    "items_stock_critico": 1
  },
  "detalle": [
    {
      "nombre": "Champú Premium",
      "stock_actual": 50.5,
      "stock_minimo": 10,
      "estado": "normal",
      "valor_stock": 757500
    }
  ]
}
```

---

## Endpoints: Dashboard

### GET `/api/dashboard/metricas`

Obtener métricas principales para el dashboard.

**Autenticación requerida:** Sí

**Query Parameters:**
- `periodo` (opcional): hoy, semana, mes (default: mes)

**Respuesta exitosa (200):**
```json
{
  "servicios": {
    "total": 150,
    "monto_total": 4500000,
    "promedio_diario": 50
  },
  "empleados": {
    "total_activos": 4,
    "mas_productivo": {
      "id": 1,
      "nombre": "Juan Pérez",
      "servicios": 60
    }
  },
  "inventario": {
    "items_bajo_stock": 3,
    "valor_total": 2500000
  },
  "convenios": {
    "activos": 5,
    "servicios_convenio": 45,
    "monto_convenios": 1350000
  }
}
```

---

### GET `/api/dashboard/grafico-servicios`

Datos para gráfico de servicios por día.

**Autenticación requerida:** Sí

**Query Parameters:**
- `dias` (opcional): Número de días hacia atrás (default: 30)

**Respuesta exitosa (200):**
```json
{
  "labels": ["2024-01-01", "2024-01-02", "2024-01-03"],
  "datos": [15, 18, 12],
  "montos": [450000, 540000, 360000]
}
```

---

## Códigos de Estado

| Código | Significado | Descripción |
|--------|------------|-------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos inválidos o incompletos |
| 401 | Unauthorized | No autenticado o token inválido |
| 403 | Forbidden | No tiene permisos para esta acción |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación |
| 500 | Internal Server Error | Error del servidor |

---

## Ejemplos de Uso

### Ejemplo completo: Registrar un servicio

```javascript
// 1. Iniciar sesión
const loginResponse = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const { token } = await loginResponse.json();

// 2. Obtener lista de empleados
const empleadosResponse = await fetch('http://localhost:8000/api/empleados', {
  headers: { 'Authorization': `Bearer ${token}` }
});

const empleados = await empleadosResponse.json();

// 3. Registrar servicio
const servicioResponse = await fetch('http://localhost:8000/api/servicios', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    placa: 'ABC123',
    tipo_vehiculo: 'Auto',
    tipo_servicio: 'Lavado completo',
    monto_total: 25000,
    id_empleado: empleados[0].id,
    observaciones: 'Cliente frecuente'
  })
});

const resultado = await servicioResponse.json();
console.log('Servicio registrado:', resultado);
```

### Ejemplo: Generar liquidación

```python
import requests

# Credenciales
BASE_URL = "http://localhost:8000"
username = "admin"
password = "admin123"

# Login
login_response = requests.post(f"{BASE_URL}/api/login", json={
    "username": username,
    "password": password
})
token = login_response.json()["token"]

# Headers con autenticación
headers = {"Authorization": f"Bearer {token}"}

# Crear liquidación
liquidacion_data = {
    "id_empleado": 1,
    "periodo_inicio": "2024-01-01",
    "periodo_fin": "2024-01-15"
}

response = requests.post(
    f"{BASE_URL}/api/liquidaciones",
    json=liquidacion_data,
    headers=headers
)

print(response.json())
```

---

## Manejo de Errores

Todas las respuestas de error siguen este formato:

```json
{
  "detail": "Descripción del error"
}
```

### Ejemplo de error de validación (422)

```json
{
  "detail": [
    {
      "loc": ["body", "monto_total"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Versionado

La API no tiene versionado explícito en la URL actualmente. Futuras versiones serán:

- v2: `/api/v2/...`
- v3: `/api/v3/...`

---

## Límites y Restricciones

| Límite | Valor |
|--------|-------|
| Tamaño máximo de request | 10 MB |
| Rate limiting | No implementado |
| Timeout | 30 segundos |
| Máximo de resultados por página | 100 |

---

## Soporte

Para reportar problemas o solicitar mejoras en la API:

- **Issues:** [GitHub Issues](https://github.com/tuusuario/LavaderoAl3.0/issues)
- **Email:** soporte@lavaderoal.com

---

**Última actualización:** 2025-11-26

**Versión de la documentación:** 1.0.0
