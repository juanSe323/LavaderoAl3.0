# Arquitectura del Sistema - Lavadero AL

## Tabla de Contenidos

- [Visión General](#visión-general)
- [Arquitectura de Alto Nivel](#arquitectura-de-alto-nivel)
- [Stack Tecnológico](#stack-tecnológico)
- [Arquitectura del Backend](#arquitectura-del-backend)
- [Arquitectura del Frontend](#arquitectura-del-frontend)
- [Base de Datos](#base-de-datos)
- [Patrones de Diseño](#patrones-de-diseño)
- [Flujo de Datos](#flujo-de-datos)
- [Seguridad](#seguridad)
- [Escalabilidad](#escalabilidad)

---

## Visión General

Lavadero AL es un sistema web full-stack construido con arquitectura cliente-servidor moderna, siguiendo el patrón de separación de responsabilidades entre frontend y backend.

### Características Arquitectónicas

- **Arquitectura en capas:** Separación clara entre presentación, lógica de negocio y datos
- **API RESTful:** Comunicación mediante HTTP/JSON
- **SPA (Single Page Application):** Experiencia de usuario fluida
- **Patrón Repository:** Abstracción de acceso a datos
- **Estrategia de negocio:** Lógica de descuentos mediante Strategy Pattern
- **Autenticación JWT:** Sistema de tokens para seguridad

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTE                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Navegador Web (Chrome/Firefox)            │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         Vue.js SPA (Port 5173)                  │  │  │
│  │  │  - Vue Router                                   │  │  │
│  │  │  - Pinia Store                                  │  │  │
│  │  │  - Bootstrap UI                                 │  │  │
│  │  │  - Axios HTTP Client                            │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/JSON
                            │ (REST API)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        SERVIDOR                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │       FastAPI Backend (Port 8000)                     │  │
│  │                                                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │   Routers    │  │  Services    │  │ Strategies  │ │  │
│  │  │ (Endpoints)  │──│  (Business)  │──│  (Patterns) │ │  │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │  │
│  │         │                                              │  │
│  │  ┌──────────────┐                                     │  │
│  │  │ Repositories │                                     │  │
│  │  │ (Data Layer) │                                     │  │
│  │  └──────────────┘                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL Queries
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              MySQL 5.7+ / MariaDB 10.3+               │  │
│  │                                                         │  │
│  │  [usuarios] [empleados] [servicios] [inventario]      │  │
│  │  [convenios] [tarifas] [liquidaciones] ...            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Vue.js | 3.5+ | Framework JavaScript reactivo |
| Vite | 7.1+ | Build tool y dev server |
| Vue Router | 4.5+ | Enrutamiento SPA |
| Pinia | 3.0+ | State management |
| Bootstrap | 5.3+ | Framework CSS |
| Axios | 1.13+ | Cliente HTTP |
| XLSX | 0.18+ | Exportación Excel |

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje de programación |
| FastAPI | 0.100+ | Framework web moderno |
| Uvicorn | - | Servidor ASGI |
| Pydantic | - | Validación de datos |
| MySQL Connector | - | Driver de base de datos |

### Base de Datos

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| MySQL | 5.7+ | Base de datos relacional |
| MariaDB | 10.3+ | Alternativa compatible |

---

## Arquitectura del Backend

### Estructura de Capas

```
backend/
├── main.py                    # Aplicación FastAPI principal
├── config.py                  # Configuración global
├── database.py                # Conexión a BD
├── schemas.py                 # Modelos Pydantic
├── auth_utils.py              # Utilidades de autenticación
│
├── routers/                   # CAPA DE PRESENTACIÓN
│   ├── auth.py               # Endpoints de autenticación
│   ├── empleados.py          # Endpoints de empleados
│   ├── servicios.py          # Endpoints de servicios
│   ├── inventario.py         # Endpoints de inventario
│   ├── liquidaciones.py      # Endpoints de liquidaciones
│   ├── convenios.py          # Endpoints de convenios
│   ├── tarifas.py            # Endpoints de tarifas
│   ├── reportes.py           # Endpoints de reportes
│   └── dashboard.py          # Endpoints de métricas
│
├── services/                  # CAPA DE NEGOCIO
│   ├── servicio_service.py   # Lógica de servicios
│   └── calculo_service.py    # Cálculos de comisiones
│
├── strategies/                # PATRONES DE DISEÑO
│   └── descuento_strategy.py # Estrategias de descuento
│
└── repositories/              # CAPA DE DATOS
    ├── auth_repository.py
    ├── empleado_repository.py
    ├── servicio_repository.py
    ├── inventario_repository.py
    ├── liquidacion_repository.py
    ├── convenio_repository.py
    ├── tarifa_repository.py
    ├── reporte_repository.py
    └── dashboard_repository.py
```

### Responsabilidades por Capa

#### 1. Routers (Controladores)

**Responsabilidad:** Manejar requests HTTP y validaciones iniciales

```python
# routers/empleados.py
@router.get("/api/empleados")
def get_empleados():
    """
    - Recibe request HTTP
    - Delega a repository
    - Retorna response JSON
    """
    try:
        return repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Características:**
- No contienen lógica de negocio compleja
- Validación de entrada mediante Pydantic
- Manejo de errores HTTP
- Retornan respuestas JSON

#### 2. Services (Servicios de Negocio)

**Responsabilidad:** Lógica de negocio compleja y orquestación

```python
# services/calculo_service.py
class CalculoService:
    def calcular_liquidacion(self, id_empleado, periodo_inicio, periodo_fin):
        """
        - Obtiene servicios del empleado
        - Calcula comisiones
        - Aplica reglas de negocio
        - Retorna resultado calculado
        """
        servicios = servicio_repo.get_by_empleado(id_empleado, ...)
        total_comision = self._calcular_comisiones(servicios)
        return total_comision
```

**Características:**
- Operaciones complejas
- Coordinación entre múltiples repositorios
- Cálculos y transformaciones
- Aplicación de reglas de negocio

#### 3. Repositories (Acceso a Datos)

**Responsabilidad:** Interacción con la base de datos

```python
# repositories/empleado_repository.py
class EmpleadoRepository:
    def get_all(self):
        """Obtiene todos los empleados de la BD"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados WHERE activo = TRUE")
        return cursor.fetchall()

    def create(self, empleado: EmpleadoCreate):
        """Inserta un nuevo empleado"""
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO empleados (...) VALUES (...)"
        cursor.execute(query, valores)
        conn.commit()
        return cursor.lastrowid
```

**Características:**
- Operaciones CRUD
- Queries SQL
- Transacciones de BD
- Sin lógica de negocio

#### 4. Strategies (Patrones de Estrategia)

**Responsabilidad:** Algoritmos intercambiables

```python
# strategies/descuento_strategy.py
class DescuentoStrategy:
    def calcular(self, monto: float) -> float:
        raise NotImplementedError

class DescuentoPorcentaje(DescuentoStrategy):
    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje

    def calcular(self, monto: float) -> float:
        return monto * (self.porcentaje / 100)

class DescuentoMontoFijo(DescuentoStrategy):
    def __init__(self, monto_fijo: float):
        self.monto_fijo = monto_fijo

    def calcular(self, monto: float) -> float:
        return self.monto_fijo
```

**Características:**
- Algoritmos intercambiables
- Facilita extensión
- Reduce complejidad condicional

---

## Arquitectura del Frontend

### Estructura de Componentes

```
src/
├── main.js                    # Punto de entrada
├── App.vue                    # Componente raíz
│
├── views/                     # PÁGINAS/VISTAS
│   ├── LoginView.vue
│   ├── DashboardView.vue
│   ├── EmpleadosView.vue
│   ├── ServiciosView.vue
│   ├── InventarioView.vue
│   ├── LiquidacionesView.vue
│   ├── ConveniosView.vue
│   ├── ReportesView.vue
│   └── TarifasView.vue
│
├── components/                # COMPONENTES REUTILIZABLES
│   ├── Navbar.vue
│   ├── EmpleadoCard.vue
│   ├── ServicioForm.vue
│   └── ...
│
├── composables/               # LÓGICA REUTILIZABLE
│   ├── useAuth.js
│   ├── useEmpleados.js
│   └── useNotification.js
│
├── stores/                    # STATE MANAGEMENT (PINIA)
│   ├── auth.js
│   ├── empleados.js
│   └── servicios.js
│
├── services/                  # SERVICIOS HTTP
│   └── api.js                # Cliente Axios configurado
│
├── router/                    # ENRUTAMIENTO
│   └── index.js              # Configuración de rutas
│
└── assets/                    # RECURSOS ESTÁTICOS
    ├── styles/
    └── images/
```

### Patrón de Componentes

#### Views (Páginas)

```vue
<!-- views/EmpleadosView.vue -->
<template>
  <div class="empleados-view">
    <Navbar />
    <div class="container">
      <h1>Gestión de Empleados</h1>
      <EmpleadoForm @submit="handleCreate" />
      <EmpleadoList :empleados="empleados" @edit="handleEdit" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useEmpleados } from '@/composables/useEmpleados';

const { empleados, cargarEmpleados, crearEmpleado } = useEmpleados();

onMounted(async () => {
  await cargarEmpleados();
});
</script>
```

**Responsabilidad:** Composición de componentes y orquestación

#### Composables (Lógica Reutilizable)

```javascript
// composables/useEmpleados.js
import { ref } from 'vue';
import api from '@/services/api';

export function useEmpleados() {
  const empleados = ref([]);
  const loading = ref(false);

  const cargarEmpleados = async () => {
    loading.value = true;
    try {
      const response = await api.get('/empleados');
      empleados.value = response.data;
    } finally {
      loading.value = false;
    }
  };

  return { empleados, loading, cargarEmpleados };
}
```

**Responsabilidad:** Lógica de negocio del frontend

#### Stores (Estado Global)

```javascript
// stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  actions: {
    async login(credentials) {
      const response = await api.post('/login', credentials);
      this.token = response.data.token;
      this.user = response.data.user;
      this.isAuthenticated = true;
      localStorage.setItem('token', this.token);
    },

    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    }
  }
});
```

**Responsabilidad:** Estado compartido entre componentes

---

## Base de Datos

### Modelo Entidad-Relación

```
┌─────────────┐         ┌──────────────┐
│  usuarios   │         │  empleados   │
├─────────────┤         ├──────────────┤
│ id (PK)     │         │ id (PK)      │
│ username    │         │ nombre       │
│ password    │         │ cedula       │
│ rol         │         │ telefono     │
└─────────────┘         │ email        │
                        │ porcentaje   │
                        │ activo       │
                        └──────────────┘
                               │
                               │ 1:N
                               │
                        ┌──────────────┐
                        │  servicios   │
                        ├──────────────┤
                        │ id (PK)      │
                        │ placa        │
                        │ tipo_vehic.  │
                        │ tipo_servic. │
                        │ monto_total  │
      ┌─────────────────│ id_empleado  │
      │                 │ id_convenio  │────────┐
      │                 │ descuento    │        │
      │                 │ fecha        │        │
      │                 └──────────────┘        │
      │                        │                │
      │                        │ N:1            │ N:1
      │                        │                │
      │                 ┌──────────────┐  ┌────────────┐
      │                 │liquidaciones │  │ convenios  │
      │                 ├──────────────┤  ├────────────┤
      │                 │ id (PK)      │  │ id (PK)    │
      │                 │ id_empleado  │  │ nombre_emp │
      │     ┌───────────│ periodo_ini  │  │ nit        │
      │     │           │ periodo_fin  │  │ contacto   │
      │     │           │ monto_total  │  │ descuento  │
      │     │           │ comision     │  │ estado     │
      │     │           │ estado       │  └────────────┘
      │     │           └──────────────┘        │
      │     │                  │                │ 1:N
      │     │                  │ 1:N            │
      │     │           ┌──────────────┐  ┌────────────────┐
      │     │           │det_liquidac. │  │vehiculos_conv. │
      │     │           ├──────────────┤  ├────────────────┤
      │     └───────────│ id_liquidac. │  │ id (PK)        │
      │                 │ id_servicio  │──│ id_convenio    │
      │                 │ monto        │  │ placa          │
      │                 │ comision     │  │ tipo_vehiculo  │
      │                 └──────────────┘  └────────────────┘
      │
      │
      │                 ┌──────────────┐
      │                 │  tarifas     │
      │                 ├──────────────┤
      │                 │ id (PK)      │
      │                 │ tipo_vehic.  │
      │                 │ precio       │
      │                 └──────────────┘
      │
      │                 ┌──────────────┐
      │                 │ inventario   │
      │                 ├──────────────┤
      │                 │ id (PK)      │
      │                 │ nombre       │
      │                 │ categoria    │
      │                 │ stock        │
      │                 │ precio_unit. │
      │                 └──────────────┘
      │                        │
      │                        │ 1:N
      │                        │
      │                 ┌──────────────┐
      │                 │ movimientos  │
      │                 ├──────────────┤
      │                 │ id (PK)      │
      └─────────────────│ id_insumo    │
                        │ tipo_movim.  │
                        │ cantidad     │
                        │ fecha        │
                        └──────────────┘
```

### Principales Tablas

#### usuarios
Almacena credenciales de autenticación

#### empleados
Información de empleados del lavadero

#### servicios
Registro de servicios realizados

#### convenios
Empresas con convenio especial

#### vehiculos_convenio
Vehículos asociados a convenios

#### inventario
Productos e insumos

#### movimientos_inventario
Historial de cambios de stock

#### liquidaciones
Pagos a empleados

#### detalle_liquidaciones
Detalle de servicios por liquidación

#### tarifas
Precios por tipo de vehículo

---

## Patrones de Diseño

### 1. Repository Pattern

**Propósito:** Abstraer el acceso a datos

**Implementación:**
```python
class EmpleadoRepository:
    def get_all(self): ...
    def get_by_id(self, id): ...
    def create(self, data): ...
    def update(self, id, data): ...
    def delete(self, id): ...
```

**Beneficios:**
- Separación de responsabilidades
- Fácil testing (mocking)
- Cambio de BD sin afectar lógica

### 2. Strategy Pattern

**Propósito:** Algoritmos de descuento intercambiables

**Implementación:**
```python
class DescuentoStrategy(ABC):
    @abstractmethod
    def calcular(self, monto): ...

# Estrategias concretas
class DescuentoPorcentaje(DescuentoStrategy): ...
class DescuentoMontoFijo(DescuentoStrategy): ...
```

**Beneficios:**
- Fácil agregar nuevos tipos de descuento
- Código más limpio (sin if/else)
- Cumple Open/Closed Principle

### 3. Dependency Injection

**Propósito:** Inyección de dependencias

**Implementación:**
```python
# FastAPI inyecta dependencias automáticamente
def verify_token(authorization: Optional[str] = Header(None)):
    # Verifica token
    return payload

@router.get("/api/empleados")
def get_empleados(user = Depends(verify_token)):
    # user ya viene autenticado
    ...
```

### 4. Singleton (Conexión BD)

**Propósito:** Una única instancia de conexión

**Implementación:**
```python
# database.py
_connection = None

def get_db_connection():
    global _connection
    if _connection is None:
        _connection = mysql.connector.connect(**DB_CONFIG)
    return _connection
```

---

## Flujo de Datos

### Ejemplo: Crear un Servicio

```
1. USUARIO
   │
   ├─→ Click "Guardar Servicio"
   │
2. FRONTEND (Vue)
   │
   ├─→ ServicioForm.vue emite evento
   ├─→ ServiciosView.vue captura evento
   ├─→ composable useServicios()
   ├─→ api.post('/servicios', data)
   │
3. HTTP REQUEST
   │
   ├─→ POST /api/servicios
   ├─→ Headers: { Authorization: "Bearer token" }
   ├─→ Body: { placa, tipo_vehiculo, ... }
   │
4. BACKEND (FastAPI)
   │
   ├─→ Router: servicios.py
   │   ├─→ Validación: ServicioCreate schema
   │   ├─→ Autenticación: verify_token()
   │   └─→ Repository: servicio_repo.create()
   │
   ├─→ Repository: servicio_repository.py
   │   ├─→ Conexión: get_db_connection()
   │   ├─→ Query: INSERT INTO servicios
   │   ├─→ Commit: conn.commit()
   │   └─→ Return: lastrowid
   │
5. DATABASE (MySQL)
   │
   ├─→ INSERT ejecutado
   ├─→ Registro creado
   └─→ ID retornado
   │
6. HTTP RESPONSE
   │
   ├─→ Status: 200 OK
   ├─→ Body: { message: "Servicio creado", id: 15 }
   │
7. FRONTEND (Vue)
   │
   ├─→ Recibe response
   ├─→ Actualiza lista de servicios
   ├─→ Muestra notificación success
   └─→ Usuario ve confirmación
```

---

## Seguridad

### Autenticación JWT

```python
# 1. Usuario hace login
credentials = { "username": "admin", "password": "..." }

# 2. Backend verifica y genera token
user = verificar_credenciales(credentials)
token = create_access_token(data={"sub": user.username, "id": user.id})

# 3. Frontend almacena token
localStorage.setItem('token', token)

# 4. Frontend envía token en cada request
headers = { 'Authorization': f'Bearer {token}' }

# 5. Backend verifica token en cada endpoint protegido
def verify_token(authorization: str = Header(None)):
    payload = decode_token(token)
    return payload
```

### Protección de Rutas (Frontend)

```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (!token && to.name !== 'login') {
    next({ name: 'login' });  // Redirigir a login
  } else {
    next();  // Permitir acceso
  }
});
```

### Validación de Datos

```python
# Pydantic valida automáticamente
class ServicioCreate(BaseModel):
    placa: str = Field(..., min_length=5, max_length=10)
    monto_total: float = Field(..., ge=0)  # >= 0

# Si los datos no cumplen, FastAPI retorna 422
```

### CORS

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Escalabilidad

### Horizontal Scaling

**Frontend:**
- Servir desde CDN
- Multiple instancias detrás de load balancer

**Backend:**
- Múltiples instancias de Uvicorn
- Load balancer (Nginx, HAProxy)
- Session storage compartido (Redis)

**Base de Datos:**
- Replica read-only para reportes
- Master-Slave replication
- Connection pooling

### Optimizaciones

#### Backend

```python
# Paginación
@router.get("/api/servicios")
def get_servicios(limite: int = 50, offset: int = 0):
    return repo.get_paginated(limite, offset)

# Caching (futuro)
@lru_cache(maxsize=128)
def get_tarifas():
    return repo.get_all()

# Conexiones asíncronas (futuro)
async def get_empleados():
    async with get_async_db() as db:
        return await db.fetch_all(query)
```

#### Frontend

```javascript
// Lazy loading de rutas
const routes = [
  {
    path: '/reportes',
    component: () => import('./views/ReportesView.vue')
  }
];

// Memoización de computed
const empleadosActivos = computed(() => {
  return empleados.value.filter(e => e.activo);
});

// Debouncing en búsquedas
const buscarEmpleado = debounce((texto) => {
  // Búsqueda
}, 300);
```

---

## Decisiones Arquitectónicas

### ¿Por qué FastAPI?

- Alto rendimiento (comparable a Node/Go)
- Documentación automática (Swagger)
- Validación de datos integrada (Pydantic)
- Type hints nativos
- Async support

### ¿Por qué Vue 3?

- Curva de aprendizaje suave
- Composition API moderna
- Excelente documentación
- Ecosistema maduro
- Performance optimizado

### ¿Por qué MySQL?

- Ampliamente soportado
- ACID compliant
- Buen rendimiento para OLTP
- Compatible con XAMPP (facilita desarrollo)

### ¿Por qué Pinia sobre Vuex?

- Más simple y ligero
- Mejor TypeScript support
- Composition API first
- Menos boilerplate
- Recomendado oficialmente

---

## Diagrama de Secuencia: Generar Liquidación

```
Usuario    Frontend    Router       Service      Repository    Database
  │           │          │            │              │            │
  │  Click    │          │            │              │            │
  ├──────────>│          │            │              │            │
  │           │ POST /liquidaciones   │              │            │
  │           ├─────────>│            │              │            │
  │           │          │ validate   │              │            │
  │           │          ├───┐        │              │            │
  │           │          │   │        │              │            │
  │           │          │<──┘        │              │            │
  │           │          │ calcular_liquidacion      │            │
  │           │          ├───────────>│              │            │
  │           │          │            │ get_servicios│            │
  │           │          │            ├─────────────>│            │
  │           │          │            │              │ SELECT ... │
  │           │          │            │              ├───────────>│
  │           │          │            │              │<───────────┤
  │           │          │            │<─────────────┤            │
  │           │          │            │ calcular comisiones       │
  │           │          │            ├───┐          │            │
  │           │          │            │   │          │            │
  │           │          │            │<──┘          │            │
  │           │          │            │ create_liquidacion        │
  │           │          │            ├─────────────>│            │
  │           │          │            │              │ INSERT ... │
  │           │          │            │              ├───────────>│
  │           │          │            │              │<───────────┤
  │           │          │            │<─────────────┤            │
  │           │          │<───────────┤              │            │
  │           │<─────────┤            │              │            │
  │<──────────┤          │            │              │            │
  │  Success  │          │            │              │            │
```

---

## Futuras Mejoras Arquitectónicas

1. **Microservicios:** Separar módulos grandes en servicios independientes
2. **Message Queue:** RabbitMQ/Redis para tareas asíncronas
3. **Caching:** Redis para cache de datos frecuentes
4. **Docker:** Containerización para deployment
5. **CI/CD:** GitHub Actions para testing y deployment
6. **Monitoring:** Prometheus + Grafana para métricas
7. **Logging:** ELK Stack para logs centralizados
8. **Testing:** Pytest + Jest para cobertura completa

---

**Última actualización:** 2025-11-26

**Versión de la arquitectura:** 1.0.0
