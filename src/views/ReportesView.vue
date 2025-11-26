<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-graph-up me-2"></i> Reportes y Estadísticas
        </h2>
        <p class="text-muted">Analiza el rendimiento del lavadero en tiempo real</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-success" @click="exportarExcel" :disabled="loading || !tieneDatos">
          <i class="bi bi-file-earmark-excel me-2"></i>
          Exportar Reporte
        </button>
      </div>
    </div>
 
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <form @submit.prevent="cargarReporte" class="row g-3 align-items-end">
          <div class="col-md-3">
            <label class="form-label fw-bold">Tipo de Reporte</label>
            <select class="form-select" v-model="filtros.tipoReporte">
              <option value="general">General</option>
              <option value="empleados">Rendimiento Empleados</option>
              <option value="convenios">Convenios</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Fecha Inicio</label>
            <input type="date" class="form-control" v-model="filtros.fechaInicio" required>
          </div>
          <div class="col-md-3">
            <label class="form-label">Fecha Fin</label>
            <input type="date" class="form-control" v-model="filtros.fechaFin" required>
          </div>
          <div class="col-md-3">
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-search me-2"></i>
              {{ loading ? 'Generando...' : 'Generar Reporte' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i> {{ error }}
    </div>

    <div v-if="filtros.tipoReporte === 'general' && !loading && datosReporte">
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="card border-primary h-100">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Ingresos Totales</h6>
                <h3 class="mb-0 text-primary">${{ formatearDinero(metricas.ingresosTotales) }}</h3>
              </div>
              <i class="bi bi-cash-stack text-primary fs-1 opacity-25"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-success h-100">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Total Servicios</h6>
                <h3 class="mb-0 text-success">{{ metricas.totalServicios }}</h3>
              </div>
              <i class="bi bi-water text-success fs-1 opacity-25"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-warning h-100">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Ticket Promedio</h6>
                <h3 class="mb-0 text-warning">${{ formatearDinero(metricas.ticketPromedio) }}</h3>
              </div>
              <i class="bi bi-receipt text-warning fs-1 opacity-25"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-info h-100">
            <div class="card-body d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted mb-1">Comisiones Pagadas</h6>
                <h3 class="mb-0 text-info">${{ formatearDinero(metricas.totalComisiones) }}</h3>
              </div>
              <i class="bi bi-people text-info fs-1 opacity-25"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card h-100 shadow-sm">
            <div class="card-header bg-white"><h5 class="mb-0"><i class="bi bi-pie-chart me-2"></i>Servicios por Tipo</h5></div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table align-middle mb-0">
                  <thead class="bg-light"><tr><th>Servicio</th><th>Cant.</th><th>Ingresos</th></tr></thead>
                  <tbody>
                    <tr v-for="s in serviciosPorTipo" :key="s.tipo_servicio">
                      <td class="text-capitalize">{{ s.tipo_servicio?.replace(/_/g, ' ') }}</td>
                      <td><span class="badge bg-primary rounded-pill">{{ s.cantidad }}</span></td>
                      <td class="fw-bold">${{ formatearDinero(s.ingresos) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card h-100 shadow-sm">
            <div class="card-header bg-white"><h5 class="mb-0"><i class="bi bi-car-front me-2"></i>Ingresos por Vehículo</h5></div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table align-middle mb-0">
                  <thead class="bg-light"><tr><th>Vehículo</th><th>Cant.</th><th>Ingresos</th></tr></thead>
                  <tbody>
                    <tr v-for="v in serviciosPorVehiculo" :key="v.tipo_vehiculo">
                      <td class="text-capitalize">{{ v.tipo_vehiculo }}</td>
                      <td><span class="badge bg-info rounded-pill">{{ v.cantidad }}</span></td>
                      <td class="fw-bold">${{ formatearDinero(v.ingresos) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mt-4 shadow-sm">
        <div class="card-header bg-white"><h5 class="mb-0"><i class="bi bi-calendar-date me-2"></i>Evolución Diaria (Últimos 30 días)</h5></div>
        <div class="card-body p-0">
           <div class="table-responsive">
            <table class="table table-hover table-sm mb-0">
              <thead class="bg-light"><tr><th>Fecha</th><th>Servicios</th><th>Ingresos</th><th>Comisiones</th></tr></thead>
              <tbody>
                <tr v-for="dia in ingresosDiarios" :key="dia.fecha">
                  <td>{{ new Date(dia.fecha).toLocaleDateString() }}</td>
                  <td>{{ dia.total_servicios }}</td>
                  <td class="text-success fw-bold">${{ formatearDinero(dia.ingresos) }}</td>
                  <td class="text-danger">${{ formatearDinero(dia.comisiones) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filtros.tipoReporte === 'empleados' && !loading && datosReporte">
      <div class="card shadow-sm">
        <div class="card-header bg-white">
           <h5 class="mb-0"><i class="bi bi-person-badge me-2"></i>Rendimiento por Empleado</h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="bg-light">
                <tr>
                  <th>Nombre</th>
                  <th>CEDULA</th>
                  <th>% Com.</th>
                  <th>Servicios</th>
                  <th>Total Vendido</th>
                  <th>Comisiones</th>
                  <th>Ticket Prom.</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="emp in reporteEmpleados" :key="emp.id">
                  <td class="fw-bold">{{ emp.nombre }}</td>
                  <td>{{ emp.cedula }}</td>
                  <td>{{ emp.porcentaje_comision }}%</td>
                  <td><span class="badge bg-secondary">{{ emp.total_servicios }}</span></td>
                  <td class="text-success fw-bold">${{ formatearDinero(emp.total_vendido) }}</td>
                  <td class="text-primary fw-bold">${{ formatearDinero(emp.total_comisiones) }}</td>
                  <td>${{ formatearDinero(emp.ticket_promedio) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="filtros.tipoReporte === 'convenios' && !loading && datosReporte">
      <div class="card shadow-sm">
        <div class="card-header bg-white">
           <h5 class="mb-0"><i class="bi bi-briefcase me-2"></i>Reporte de Convenios</h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="bg-light">
                <tr>
                  <th>Empresa</th>
                  <th>RUT</th>
                  <th>Total Servicios</th>
                  <th>Total Facturado</th>
                  <th>Descuentos</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="reporteConvenios.length === 0"><td colspan="5" class="text-center py-4 text-muted">Sin datos.</td></tr>
                <tr v-for="conv in reporteConvenios" :key="conv.id">
                  <td class="fw-bold">{{ conv.nombre_empresa }}</td>
                  <td>{{ conv.nit_empresa }}</td>
                  <td><span class="badge bg-secondary">{{ conv.total_servicios }}</span></td>
                  <td class="text-success fw-bold">${{ formatearDinero(conv.total_facturado) }}</td>
                  <td class="text-danger fw-bold">${{ formatearDinero(conv.total_descuentos) }}</td>
                </tr>
              </tbody>
            </table>
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
import * as XLSX from 'xlsx'

// 1. Variables y Estado
const filtros = reactive({ tipoReporte: 'general', fechaInicio: '', fechaFin: '' })
const datosReporte = ref(null)
const ingresosDiarios = ref([])

// 2. Función de carga dinámica según tipo
const fetchReporte = async () => {
  const { tipoReporte, fechaInicio, fechaFin } = filtros
  
  // Limpiar datos anteriores
  datosReporte.value = null
  ingresosDiarios.value = []

  if (tipoReporte === 'general') {
    const [general, diarios] = await Promise.all([
      api.getReporteGeneral(fechaInicio, fechaFin),
      api.getReporteServiciosDiarios(30) // Fijo 30 días para gráfico/tabla evolución
    ])
    ingresosDiarios.value = diarios
    return general
  }
  
  if (tipoReporte === 'empleados') return api.getReporteEmpleados(fechaInicio, fechaFin)
  if (tipoReporte === 'convenios') return api.getReporteConvenios(fechaInicio, fechaFin)
}

// 3. Usar Composable
const { loading, error, exec: cargarReporte } = useApi(async () => {
  datosReporte.value = await fetchReporte()
})

// 4. Inicialización
onMounted(() => {
  const now = new Date()
  const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
  const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  
  filtros.fechaInicio = firstDay.toISOString().split('T')[0]
  filtros.fechaFin = lastDay.toISOString().split('T')[0]
  
  cargarReporte()
})

// 5. Computados para facilitar acceso en template
const metricas = computed(() => datosReporte.value?.totales || {})
const serviciosPorTipo = computed(() => datosReporte.value?.por_tipo_servicio || [])
const serviciosPorVehiculo = computed(() => datosReporte.value?.por_tipo_vehiculo || [])
const reporteEmpleados = computed(() => Array.isArray(datosReporte.value) ? datosReporte.value : [])
const reporteConvenios = computed(() => Array.isArray(datosReporte.value) ? datosReporte.value : [])
const tieneDatos = computed(() => !!datosReporte.value)

// 6. Helpers
const formatearDinero = (valor) => {
  if (!valor) return '0'
  return Number(valor).toLocaleString('es-CL')
}

// 7. Exportación a Excel
const exportarExcel = () => {
  if (loading.value || !datosReporte.value) return

  const workbook = XLSX.utils.book_new()
  const nombreArchivo = `Reporte_${filtros.tipoReporte}_${filtros.fechaInicio}.xlsx`

  if (filtros.tipoReporte === 'general') {
    // Hoja Resumen
    const resumen = [
      ["Reporte General", ""],
      ["Desde", filtros.fechaInicio],
      ["Hasta", filtros.fechaFin],
      ["", ""],
      ["Ingresos Totales", metricas.value.ingresos_totales || 0],
      ["Total Servicios", metricas.value.total_servicios || 0],
      ["Ticket Promedio", metricas.value.ticket_promedio || 0],
      ["Total Comisiones", metricas.value.total_comisiones || 0]
    ]
    const wsResumen = XLSX.utils.aoa_to_sheet(resumen)
    XLSX.utils.book_append_sheet(workbook, wsResumen, "Resumen")

    // Hoja Servicios
    if (serviciosPorTipo.value.length) {
      const ws = XLSX.utils.json_to_sheet(serviciosPorTipo.value)
      XLSX.utils.book_append_sheet(workbook, ws, "Por Tipo")
    }
  } 
  else if (filtros.tipoReporte === 'empleados') {
    const ws = XLSX.utils.json_to_sheet(reporteEmpleados.value)
    XLSX.utils.book_append_sheet(workbook, ws, "Empleados")
  } 
  else if (filtros.tipoReporte === 'convenios') {
    const ws = XLSX.utils.json_to_sheet(reporteConvenios.value)
    XLSX.utils.book_append_sheet(workbook, ws, "Convenios")
  }

  XLSX.writeFile(workbook, nombreArchivo)
}
</script>

<style scoped>
.fade-in { animation: fadeIn 0.5s; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.card { border: none; }
</style>