<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-cash-coin me-2"></i>
          Liquidaciones de Empleados
        </h2>
        <p class="text-muted">Gestiona pagos, comisiones y nómina</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="abrirModalCrear">
          <i class="bi bi-calculator me-2"></i>
          Nueva Liquidación
        </button>
      </div>
    </div>

    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
             <label class="form-label small fw-bold">Filtrar por Empleado</label>
             <select class="form-select" v-model="filtros.empleado">
               <option value="">Todos los empleados</option>
               <option v-for="emp in empleados" :key="emp.id" :value="emp.nombre">{{ emp.nombre }}</option>
             </select>
          </div>
          <div class="col-md-3">
             <label class="form-label small fw-bold">Estado</label>
             <select class="form-select" v-model="filtros.estado">
               <option value="">Todos los estados</option>
               <option value="Pendiente">Pendiente</option>
               <option value="Pagada">Pagada</option>
             </select>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-start border-4 border-primary h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Total Liquidaciones</h6>
            <h3 class="mb-0">{{ liquidaciones?.length || 0 }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-start border-4 border-warning h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Pendientes de Pago</h6>
            <h3 class="mb-0 text-warning">{{ pendientesCount }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-start border-4 border-success h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Pagadas</h6>
            <h3 class="mb-0 text-success">{{ (liquidaciones?.length || 0) - pendientesCount }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-start border-4 border-info h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Monto Pendiente</h6>
            <h3 class="mb-0 text-info">${{ totalPendiente.toLocaleString() }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-2 text-muted">Cargando datos...</p>
        </div>
        
        <div v-else-if="error" class="alert alert-danger m-3">{{ error }}</div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-3">ID</th>
                <th>Empleado</th>
                <th>Período</th>
                <th class="text-center">Servicios</th>
                <th class="text-end">Total Ventas</th>
                <th class="text-center">% Com.</th>
                <th class="text-end">A Pagar</th>
                <th class="text-center">Estado</th>
                <th class="text-end pe-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="liq in liquidacionesFiltradas" :key="liq.id">
                <td class="ps-3 text-muted">#{{ liq.id }}</td>
                <td>
                  <div class="fw-bold text-dark">{{ liq.nombre_empleado }}</div>
                  <small class="text-muted" style="font-size: 0.8rem;">{{ liq.cedula }}</small>
                </td>
                <td>
                  <small>{{ formatDate(liq.periodo_inicio) }} <br> {{ formatDate(liq.periodo_fin) }}</small>
                </td>
                <td class="text-center">
                   <span class="badge bg-secondary rounded-pill">{{ liq.total_servicios }}</span>
                </td>
                <td class="text-end text-muted">${{ liq.monto_total_servicios?.toLocaleString() }}</td>
                <td class="text-center">{{ liq.porcentaje_comision }}%</td>
                <td class="text-end fw-bold text-success fs-6">${{ liq.total_comisiones?.toLocaleString() }}</td>
                <td class="text-center">
                  <span :class="'badge rounded-pill bg-' + (liq.estado === 'pagada' ? 'success' : 'warning text-dark')">
                    {{ liq.estado === 'pagada' ? 'Pagada' : 'Pendiente' }}
                  </span>
                </td>
                <td class="text-end pe-3">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" @click="verDetalle(liq)" title="Ver Detalle">
                      <i class="bi bi-eye"></i>
                    </button>
                    
                    <button v-if="liq.estado === 'pendiente'" class="btn btn-outline-success" @click="marcarPagada(liq)" title="Marcar como Pagada">
                      <i class="bi bi-check-lg"></i>
                    </button>

                    <button v-if="liq.estado === 'pendiente'" class="btn btn-outline-danger" @click="eliminarLiquidacion(liq)" title="Eliminar Registro">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="liquidacionesFiltradas.length === 0">
                <td colspan="9" class="text-center py-4 text-muted">
                  No se encontraron liquidaciones con los filtros actuales.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalLiquidacion" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title"><i class="bi bi-calculator me-2"></i>Generar Liquidación</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="calcularLiquidacion">
              <div class="mb-3">
                <label class="form-label fw-bold">Empleado</label>
                <select class="form-select" v-model="nuevaLiquidacion.id_empleado" required>
                  <option value="">Seleccione un empleado...</option>
                  <option v-for="emp in empleados" :key="emp.id" :value="emp.id">{{ emp.nombre }}</option>
                </select>
              </div>
              <div class="row">
                <div class="col-6 mb-3">
                  <label class="form-label fw-bold">Fecha Inicio</label>
                  <input type="date" class="form-control" v-model="nuevaLiquidacion.periodo_inicio" required>
                </div>
                <div class="col-6 mb-3">
                  <label class="form-label fw-bold">Fecha Fin</label>
                  <input type="date" class="form-control" v-model="nuevaLiquidacion.periodo_fin" required>
                </div>
              </div>
              <div class="alert alert-info d-flex align-items-center small">
                <i class="bi bi-info-circle fs-4 me-2"></i>
                <div>
                  El sistema calculará automáticamente las comisiones sumando los servicios "completados" en este rango.
                </div>
              </div>
              <div class="modal-footer px-0 pb-0 border-top-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-primary">Generar</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalDetalleLiquidacion" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalle Liquidación #{{ liquidacionSeleccionada.id }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body bg-light" v-if="liquidacionSeleccionada.id">
            <div class="card mb-3 border-0 shadow-sm">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-md-6">
                    <h5 class="fw-bold mb-1">{{ liquidacionSeleccionada.nombre_empleado }}</h5>
                    <p class="text-muted mb-0">{{ liquidacionSeleccionada.cedula }}</p>
                    <small class="text-primary">{{ liquidacionSeleccionada.email }}</small>
                  </div>
                  <div class="col-md-6 text-md-end mt-3 mt-md-0">
                    <div class="text-muted small">Total a Pagar</div>
                    <h2 class="text-success fw-bold mb-0">${{ liquidacionSeleccionada.total_comisiones?.toLocaleString() }}</h2>
                    <span :class="'badge mt-2 bg-' + (liquidacionSeleccionada.estado === 'pagada' ? 'success' : 'warning text-dark')">
                      {{ liquidacionSeleccionada.estado === 'pagada' ? 'Pagada' : 'Pendiente' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white fw-bold">Desglose de Servicios</div>
              <div class="card-body p-0">
                <div class="table-responsive" style="max-height: 350px;">
                  <table class="table table-striped mb-0 small">
                    <thead class="sticky-top bg-white">
                      <tr>
                        <th>Fecha</th>
                        <th>Vehículo</th>
                        <th>Servicio</th>
                        <th class="text-end">Monto Total</th>
                        <th class="text-end">Comisión Ganada</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="serv in detalleServicios" :key="serv.id">
                        <td>{{ formatDate(serv.fecha) }}</td>
                        <td>{{ serv.tipo_vehiculo }} <span class="text-muted">({{ serv.placa }})</span></td>
                        <td>{{ formatearServicio(serv.tipo_servicio) }}</td>
                        <td class="text-end text-muted">${{ serv.monto_total?.toLocaleString() }}</td>
                        <td class="text-end fw-bold text-success">${{ serv.monto_comision?.toLocaleString() }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            <button class="btn btn-outline-dark"><i class="bi bi-printer me-1"></i> Imprimir</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useApi } from '@/composables/useApi'
import { useBootstrap } from '@/composables/useBootstrap'

// 1. Carga de Datos
const { data: liquidaciones, loading, error, exec: cargarLiquidaciones } = useApi(api.getLiquidaciones)
const empleados = ref([])

// 2. Variables UI
const { showModal, hideModal } = useBootstrap()
const nuevaLiquidacion = reactive({ id_empleado: '', periodo_inicio: '', periodo_fin: '' })
const filtros = reactive({ empleado: '', estado: '' })
const liquidacionSeleccionada = ref({})
const detalleServicios = ref([])

// 3. Cargar al inicio
onMounted(async () => {
  cargarLiquidaciones()
  try {
    empleados.value = await api.getEmpleados()
  } catch (e) { console.error("Error cargando empleados para select", e) }
})

// 4. Computados
const liquidacionesFiltradas = computed(() => {
  if (!liquidaciones.value) return []
  return liquidaciones.value.filter(l => {
    // Nota: El backend devuelve 'estado' en minúsculas ('pendiente', 'pagada')
    const estadoFiltro = filtros.estado.toLowerCase()
    
    const matchEmp = filtros.empleado ? l.nombre_empleado === filtros.empleado : true
    const matchEst = filtros.estado ? l.estado === estadoFiltro : true
    return matchEmp && matchEst
  })
})

const pendientesCount = computed(() => {
  if (!liquidaciones.value) return 0
  return liquidaciones.value.filter(l => l.estado === 'pendiente').length
})

const totalPendiente = computed(() => {
  if (!liquidaciones.value) return 0
  return liquidaciones.value
    .filter(l => l.estado === 'pendiente')
    .reduce((sum, l) => sum + (l.total_comisiones || 0), 0)
})

// 5. Acciones
const abrirModalCrear = () => {
  Object.assign(nuevaLiquidacion, { id_empleado: '', periodo_inicio: '', periodo_fin: '' })
  showModal('modalLiquidacion')
}

const calcularLiquidacion = async () => {
  try {
    await api.calcularLiquidacion(nuevaLiquidacion)
    hideModal('modalLiquidacion')
    cargarLiquidaciones()
    alert("Liquidación generada con éxito")
  } catch (e) {
    alert("Error: " + (e.response?.data?.detail || e.message))
  }
}

const verDetalle = async (liq) => {
  try {
    const data = await api.getLiquidacionDetalle(liq.id)
    liquidacionSeleccionada.value = data
    detalleServicios.value = data.servicios || []
    showModal('modalDetalleLiquidacion')
  } catch (e) { alert("No se pudo cargar el detalle") }
}

const marcarPagada = async (liq) => {
  if(!confirm(`¿Confirmas el pago a ${liq.nombre_empleado}?`)) return
  try {
    await api.marcarLiquidacionPagada(liq.id)
    cargarLiquidaciones()
  } catch (e) { alert("Error al procesar el pago") }
}

const eliminarLiquidacion = async (liq) => {
  if (!confirm(`⚠️ ¿Estás seguro de ELIMINAR la liquidación de ${liq.nombre_empleado}?`)) return
  try {
    await api.deleteLiquidacion(liq.id)
    cargarLiquidaciones()
    alert("Liquidación eliminada")
  } catch (e) { 
    alert("Error: " + (e.response?.data?.detail || e.message)) 
  }
}

// Helpers
const formatDate = (dateStr) => {
  if(!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-CL')
}
const formatearServicio = (texto) => texto ? texto.replace(/_/g, ' ').toUpperCase() : ''
</script>

<style scoped>
.fade-in { animation: fadeIn 0.4s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.card { border-radius: 0.5rem; }
</style>