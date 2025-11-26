<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-speedometer2 me-2"></i>
          Dashboard
        </h2>
        <p class="text-muted">Resumen general del lavadero</p>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2 text-muted">Actualizando tablero...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i> Error cargando datos: {{ error }}
    </div>

    <div v-else>
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="metric-card blue">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="metric-label">Servicios Hoy</div>
                <div class="metric-value">{{ metrics.serviciosHoy }}</div>
              </div>
              <i class="bi bi-water" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="metric-card green">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="metric-label">Ingresos Hoy</div>
                <div class="metric-value">${{ metrics.ingresosHoy?.toLocaleString() }}</div>
              </div>
              <i class="bi bi-cash-stack" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="metric-card orange">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="metric-label">Clientes Activos</div>
                <div class="metric-value">{{ metrics.clientesActivos }}</div>
              </div>
              <i class="bi bi-people" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="metric-card red">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="metric-label">Insumos Bajos</div>
                <div class="metric-value">{{ metrics.insumosBajos }}</div>
              </div>
              <i class="bi bi-exclamation-triangle" style="font-size: 3rem; opacity: 0.3;"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-8">
          <div class="card h-100 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">
                <i class="bi bi-clock-history me-2"></i>
                Servicios Recientes
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="bg-light">
                    <tr>
                      <th class="ps-3">ID</th>
                      <th>Cliente/Vehículo</th>
                      <th>Servicio</th>
                      <th>Empleado</th>
                      <th>Monto</th>
                      <th>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="servicio in serviciosRecientes" :key="servicio.id">
                      <td class="ps-3 text-muted">#{{ servicio.id }}</td>
                      <td>
                        <div class="fw-bold">{{ servicio.cliente }}</div>
                        <small class="text-muted">{{ servicio.vehiculo }}</small>
                      </td>
                      <td>{{ servicio.tipoServicio }}</td>
                      <td>{{ servicio.empleado }}</td>
                      <td class="fw-bold">${{ servicio.monto.toLocaleString() }}</td>
                      <td>
                        <span :class="'badge rounded-pill bg-' + servicio.estadoColor">
                          {{ servicio.estado }}
                        </span>
                      </td>
                    </tr>
                    <tr v-if="serviciosRecientes.length === 0">
                      <td colspan="6" class="text-center py-4 text-muted">No hay actividad reciente.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card mb-3 shadow-sm border-warning">
            <div class="card-header bg-warning bg-opacity-10 text-dark border-warning">
              <h5 class="mb-0 fs-6 fw-bold">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Stock Bajo / Crítico
              </h5>
            </div>
            <div class="card-body p-0">
              <ul class="list-group list-group-flush">
                <li v-if="alertasInventario.length === 0" class="list-group-item text-center text-muted py-3">
                  Todo en orden
                </li>
                <li 
                  v-for="alerta in alertasInventario" 
                  :key="alerta.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <div class="fw-bold">{{ alerta.nombre }}</div>
                    <small class="text-muted">Stock: {{ alerta.stock }} {{ alerta.unidad }}</small>
                  </div>
                  <span class="badge bg-danger">Reponer</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0 fs-6 fw-bold">
                <i class="bi bi-person-check me-2"></i>
                Top Empleados (Mes)
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div 
                  v-for="empleado in empleadosActivos" 
                  :key="empleado.id"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                      <div class="status-icon active me-2"></div>
                      <div>
                        <div class="fw-bold">{{ empleado.nombre }}</div>
                        <small class="text-muted">{{ empleado.serviciosHoy }} servicios</small>
                      </div>
                    </div>
                    <div class="text-end">
                      <span class="badge bg-success bg-opacity-10 text-success border border-success">
                        ${{ empleado.comisionHoy.toLocaleString() }}
                      </span>
                      <div style="font-size: 0.7rem;" class="text-muted mt-1">Comisión</div>
                    </div>
                  </div>
                </div>
                <div v-if="empleadosActivos.length === 0" class="p-3 text-center text-muted">
                  Sin actividad registrada este mes.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useApi } from '@/composables/useApi'

// 1. Estado Reactivo
const metrics = ref({ serviciosHoy: 0, ingresosHoy: 0, clientesActivos: 0, insumosBajos: 0 })
const serviciosRecientes = ref([])
const alertasInventario = ref([])
const empleadosActivos = ref([])

// 2. Funciones de Formato
const formatearTipoServicio = (tipo) => {
  const map = {
    'lavado_simple': 'Lavado Simple', 'lavado_completo': 'Lavado Completo',
    'encerado': 'Encerado', 'lavado_motor': 'Lavado Motor',
    'pulido': 'Pulido', 'descontaminacion': 'Descontaminación'
  }
  return map[tipo] || tipo
}

const formatearEstado = (estado) => {
  const map = { 'completado': 'Completado', 'pendiente': 'Pendiente', 'cancelado': 'Cancelado' }
  return map[estado] || estado
}

const getEstadoColor = (estado) => {
  const map = { 'completado': 'success', 'pendiente': 'warning', 'cancelado': 'secondary' }
  return map[estado] || 'secondary'
}

// 3. Función de Carga Unificada
const cargarTodo = async () => {
  // Ejecutamos todas las peticiones en paralelo para mayor velocidad
  const [resMetrics, resServicios, resAlertas, resEmpleados] = await Promise.all([
    api.getMetricasDashboard(),
    api.getServiciosRecientes(10),
    api.getAlertasInventarioDashboard(),
    api.getEmpleadosTop(5)
  ])

  // Mapeo de Métricas
  // Aseguramos que los datos existen o ponemos 0 por defecto
  const dataMetrics = resMetrics.data || resMetrics
  metrics.value = {
    serviciosHoy: dataMetrics.servicios_hoy || 0,
    ingresosHoy: dataMetrics.ingresos_hoy || 0,
    clientesActivos: dataMetrics.clientes_activos || 0,
    insumosBajos: dataMetrics.insumos_bajos || 0
  }

  // Mapeo de Servicios
  const listaServicios = resServicios.data || resServicios
  serviciosRecientes.value = listaServicios.map(s => ({
    id: s.id,
    cliente: s.placa,
    vehiculo: `${s.tipo_vehiculo || ''}`, // Ajustado para mostrar tipo
    tipoServicio: formatearTipoServicio(s.tipo_servicio),
    empleado: s.nombre_empleado || 'Sin asignar',
    monto: s.monto_total,
    estado: formatearEstado(s.estado),
    estadoColor: getEstadoColor(s.estado)
  }))

  // Mapeo de Alertas
  const listaAlertas = resAlertas.data || resAlertas
  alertasInventario.value = listaAlertas.map(a => ({
    id: a.id,
    nombre: a.nombre,
    stock: a.stock,
    unidad: a.unidad
  }))

  // Mapeo de Empleados
  const listaEmpleados = resEmpleados.data || resEmpleados
  empleadosActivos.value = listaEmpleados.map(e => ({
    id: e.id,
    nombre: e.nombre,
    serviciosHoy: e.total_servicios || 0,
    comisionHoy: e.total_comisiones || 0
  }))
}

// 4. Usar Composable
const { loading, error, exec: actualizarDashboard } = useApi(cargarTodo)

// 5. Ciclo de Vida
onMounted(() => {
  actualizarDashboard()
})
</script>

<style scoped>
/* Estilos específicos del Dashboard */
.metric-card {
  padding: 1.5rem;
  border-radius: 10px;
  color: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  height: 100%;
  transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }

.metric-card.blue { background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%); }
.metric-card.green { background: linear-gradient(45deg, #43e97b 0%, #38f9d7 100%); }
.metric-card.orange { background: linear-gradient(45deg, #fa709a 0%, #fee140 100%); }
.metric-card.red { background: linear-gradient(45deg, #ff0844 0%, #ffb199 100%); }

.metric-label { font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-value { font-size: 2.2rem; font-weight: 800; line-height: 1.2; }

.status-icon {
  width: 10px; height: 10px; border-radius: 50%; display: inline-block;
}
.status-icon.active { background-color: #198754; box-shadow: 0 0 5px #198754; }

.fade-in { animation: fadeIn 0.5s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
