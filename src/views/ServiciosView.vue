<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4 align-items-center">
      <div class="col">
        <h2 class="fw-bold text-primary">
          <i class="bi bi-droplet-half me-2"></i>Gestión de Servicios
        </h2>
        <p class="text-muted mb-0">Administración de lavados, convenios y asignación de personal</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary shadow-sm" @click="abrirModalCrear">
          <i class="bi bi-plus-lg me-2"></i>Nuevo Servicio
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Cargando servicios...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger m-3">
      <i class="bi bi-exclamation-triangle me-2"></i> {{ error }}
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light text-secondary">
              <tr>
                <th class="ps-4">Fecha / Hora</th>
                <th>Vehículo</th>
                <th>Tipo Cliente</th>
                <th>Servicio</th>
                <th>Empleado</th>
                <th class="text-end">Monto</th>
                <th class="text-center">Estado</th>
                <th class="text-end pe-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in serviciosProcesados" :key="s.id" :class="{'table-active text-muted opacity-75': s.estado === 'cancelado'}">
                <td class="ps-4">
                  <div class="fw-bold text-dark">{{ s.fecha_fmt }}</div>
                  <small class="text-muted">{{ s.hora_fmt }}</small>
                </td>
                <td>
                  <div class="fw-bold font-monospace">{{ s.placa }}</div>
                  <small class="text-muted text-capitalize">{{ s.tipo_vehiculo }}</small>
                </td>
                <td>
                  <div v-if="s.es_convenio" class="d-flex align-items-center">
                    <span class="badge bg-indigo text-white me-2">Convenio</span>
                    <small class="text-truncate" style="max-width: 150px;" :title="s.nombre_empresa">
                      {{ s.nombre_empresa }}
                    </small>
                  </div>
                  <span v-else class="badge bg-light text-dark border">Particular</span>
                </td>
                <td>{{ formatearServicio(s.tipo_servicio) }}</td>
                <td>
                  <i class="bi bi-person-circle text-muted me-1"></i>
                  {{ s.nombre_empleado || 'Sin asignar' }}
                </td>
                <td class="text-end fw-bold">
                  <span :class="s.estado === 'cancelado' ? 'text-decoration-line-through' : 'text-success'">
                    ${{ s.monto_total?.toLocaleString() }}
                  </span>
                </td>
                <td class="text-center">
                  <span :class="`badge rounded-pill bg-${getColorEstado(s.estado)}`">
                    {{ s.estado }}
                  </span>
                </td>
                <td class="text-end pe-4">
                  <div class="btn-group" v-if="s.estado !== 'cancelado'">
                    <button class="btn btn-sm btn-outline-secondary" @click="abrirModalEditar(s)" title="Editar">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="cancelarServicio(s)" title="Cancelar">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="servicios.length === 0">
                <td colspan="8" class="text-center py-5 text-muted">
                  <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                  No hay servicios registrados recientemente.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalServicio" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header text-white" :class="modoEdicion ? 'bg-warning' : 'bg-primary'">
            <h5 class="modal-title fw-bold">
              <i :class="modoEdicion ? 'bi bi-pencil-square' : 'bi bi-magic'"></i>
              {{ modoEdicion ? 'Editar Servicio' : 'Nuevo Servicio' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          
          <div class="modal-body p-4">
            <div v-if="!modoEdicion" class="d-flex justify-content-center mb-4">
              <div class="btn-group shadow-sm" role="group">
                <input type="radio" class="btn-check" name="tipoReg" id="regNormal" value="normal" v-model="tipoRegistro" @change="limpiarFormulario(false)">
                <label class="btn btn-outline-primary px-4" for="regNormal">Particular</label>
                
                <input type="radio" class="btn-check" name="tipoReg" id="regConvenio" value="convenio" v-model="tipoRegistro" @change="limpiarFormulario(false)">
                <label class="btn btn-outline-primary px-4" for="regConvenio">Empresa / Convenio</label>
              </div>
            </div>

            <form @submit.prevent="guardarServicio">
              
              <div v-if="tipoRegistro === 'convenio'" class="card bg-light border-primary mb-4">
                <div class="card-body">
                  <label class="form-label fw-bold text-primary">Paso 1: Validar placa</label>
                  <div class="input-group mb-2">
                    <input 
                      type="text" 
                      class="form-control text-uppercase fw-bold" 
                      v-model="form.placa" 
                      placeholder="Ej: AB1234" 
                      :disabled="modoEdicion"
                      @keyup.enter="!modoEdicion && validarConvenio()"
                    >
                    <button class="btn btn-primary" type="button" @click="validarConvenio" :disabled="validando || modoEdicion">
                      <span v-if="validando" class="spinner-border spinner-border-sm me-1"></span>
                      Validar
                    </button>
                  </div>
                  
                  <div v-if="convenioDetectado" class="alert alert-success d-flex align-items-center py-2 mb-0">
                    <i class="bi bi-check-circle-fill me-2 fs-5"></i>
                    <div>
                      <strong>{{ convenioDetectado.nombre_empresa }}</strong>
                      <div class="small">
                        Descuento: {{ convenioDetectado.tipo_descuento === 'porcentaje' ? convenioDetectado.valor_descuento + '%' : '$' + convenioDetectado.valor_descuento }}
                        | Vehículo: <span class="text-uppercase">{{ convenioDetectado.tipo_vehiculo || 'N/A' }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="errorConvenio" class="text-danger small mt-1">
                    <i class="bi bi-exclamation-circle-fill me-1"></i> {{ errorConvenio }}
                  </div>
                </div>
              </div>

              <div class="row g-3">
                <div class="col-md-4" v-if="tipoRegistro === 'normal'">
                  <label class="form-label fw-bold" >Placa</label>
                  <input placeholder="ABC###" type="text" class="form-control text-uppercase" v-model="form.placa" required maxlength="8">
                </div>

                <div class="col-md-4">
                  <label class="form-label fw-bold">Tipo Vehículo</label>
                  <select class="form-select" v-model="form.tipo_vehiculo" required @change="calcularPrecio">
                    <option value="auto">Auto</option>
                    <option value="camioneta">Camioneta</option>
                    <option value="suv">SUV</option>
                    <option value="furgon">Furgón</option>
                  </select>
                </div>

                <div class="col-md-4">
                  <label class="form-label fw-bold">Servicio</label>
                  <select class="form-select" v-model="form.tipo_servicio" required @change="calcularPrecio">
                    <option value="">Seleccione...</option>
                    <option v-for="(precio, key) in tarifas[form.tipo_vehiculo]" :key="key" :value="key">
                       {{ formatearServicio(key) }}
                    </option>
                  </select>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-bold">Asignar a Empleado</label>
                  <select class="form-select" v-model="form.id_empleado" required>
                    <option value="">Seleccione...</option>
                    <option v-for="emp in empleados" :key="emp.id" :value="emp.id">
                      {{ emp.nombre }}
                    </option>
                  </select>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-bold text-success">Total a Cobrar</label>
                  <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input type="number" class="form-control fw-bold fs-5 text-end text-success" v-model="form.monto_total" required>
                  </div>
                  <div v-if="montoDescuento > 0" class="form-text text-end text-muted small">
                    <span class="text-decoration-line-through">Lista: ${{ precioLista }}</span> 
                    <span class="text-success ms-1">(-${{ montoDescuento }})</span>
                  </div>
                </div>

                <div class="col-12">
                  <label class="form-label">Observaciones</label>
                  <textarea class="form-control" v-model="form.observaciones" rows="2"></textarea>
                </div>
              </div>
            </form>

          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn" :class="modoEdicion ? 'btn-warning' : 'btn-primary'" @click="guardarServicio">
              <i class="bi" :class="modoEdicion ? 'bi-pencil-square' : 'bi-save'"></i>
              {{ modoEdicion ? 'Actualizar' : 'Registrar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import api from '@/services/api'
import { useApi } from '@/composables/useApi'
import { useBootstrap } from '@/composables/useBootstrap'

// 1. Variables y Estado
const { showModal, hideModal } = useBootstrap()
const servicios = ref([])
const empleados = ref([])
const tarifas = ref({})

const modoEdicion = ref(false)
const tipoRegistro = ref('normal')
const validando = ref(false)
const convenioDetectado = ref(null)
const errorConvenio = ref(null)

const precioLista = ref(0)
const montoDescuento = ref(0)

const form = reactive({
  id: null,
  placa: '',
  tipo_vehiculo: 'auto',
  tipo_servicio: '',
  monto_total: 0,
  id_empleado: '',
  id_convenio: null,
  descuento: 0,
  observaciones: ''
})

// 2. Carga Inicial
const cargarDatosIniciales = async () => {
  // Carga paralela eficiente
  const [resServ, resEmp, resTarif] = await Promise.all([
    api.getServicios(),
    api.getEmpleados(),
    api.getTarifas()
  ])

  servicios.value = resServ.data || resServ
  empleados.value = resEmp.data || resEmp
  
  // Procesar tarifas para acceso rápido
  const listaTarifas = resTarif.data || resTarif
  tarifas.value = {}
  listaTarifas.forEach(t => {
    if (!tarifas.value[t.tipo_vehiculo]) tarifas.value[t.tipo_vehiculo] = {}
    tarifas.value[t.tipo_vehiculo][t.tipo_servicio] = t.precio
  })
  
  return true
}

// Usamos el composable para manejar la carga
const { loading, error, exec: recargar } = useApi(cargarDatosIniciales)

onMounted(() => {
  recargar()
})

// 3. Propiedades Computadas
const serviciosProcesados = computed(() => {
  return servicios.value.map(s => ({
    ...s,
    fecha_fmt: new Date(s.fecha).toLocaleDateString(),
    hora_fmt: new Date(s.fecha).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
  }))
})

// 4. Lógica de Negocio
const validarConvenio = async () => {
  if (!form.placa) return
  validando.value = true
  errorConvenio.value = null
  convenioDetectado.value = null
  form.id_convenio = null

  try {
    const res = await api.validarConvenioplaca(form.placa) // Asegúrate de tener esta función en api.js (ver nota abajo)
    
    if (res.tiene_convenio) {
      const datos = res.convenio
      convenioDetectado.value = datos
      form.id_convenio = datos.id_convenio
      if (datos.tipo_vehiculo) form.tipo_vehiculo = datos.tipo_vehiculo
      calcularPrecio()
    } else {
      errorConvenio.value = "placa no asociada a convenio vigente."
    }
  } catch (e) {
    errorConvenio.value = "Error al validar la placa."
  } finally {
    validando.value = false
  }
}

const calcularPrecio = () => {
  const v = form.tipo_vehiculo
  const s = form.tipo_servicio

  // Precio Base
  if (v && s && tarifas.value[v] && tarifas.value[v][s]) {
    precioLista.value = parseFloat(tarifas.value[v][s])
  } else {
    precioLista.value = 0
  }

  montoDescuento.value = 0

  // Descuento
  if (tipoRegistro.value === 'convenio' && convenioDetectado.value && precioLista.value > 0) {
    const c = convenioDetectado.value
    if (c.tipo_descuento === 'porcentaje') {
      montoDescuento.value = Math.round(precioLista.value * (c.valor_descuento / 100))
    } else {
      montoDescuento.value = parseFloat(c.valor_descuento)
    }
  }

  form.monto_total = Math.max(0, precioLista.value - montoDescuento.value)
  form.descuento = montoDescuento.value
}

const limpiarFormulario = (borrarTodo = true) => {
  // Reset parcial o total según necesidad
  if (borrarTodo) {
    Object.assign(form, { id: null, placa: '', tipo_vehiculo: 'auto', tipo_servicio: '', monto_total: 0, id_empleado: '', id_convenio: null, descuento: 0, observaciones: '' })
  } else {
    // Al cambiar de tipo de registro, solo reseteamos convenios
    form.id_convenio = null
    form.descuento = 0
    convenioDetectado.value = null
    errorConvenio.value = null
    calcularPrecio()
  }
}

const abrirModalCrear = () => {
  modoEdicion.value = false
  limpiarFormulario(true)
  showModal('modalServicio')
}

const abrirModalEditar = (s) => {
  modoEdicion.value = true
  tipoRegistro.value = s.es_convenio ? 'convenio' : 'normal'
  
  // Copiar datos
  Object.assign(form, {
    id: s.id,
    placa: s.placa,
    tipo_vehiculo: s.tipo_vehiculo,
    tipo_servicio: s.tipo_servicio,
    monto_total: s.monto_total,
    id_empleado: s.id_empleado,
    id_convenio: s.id_convenio,
    descuento: s.descuento,
    observaciones: s.observaciones || ''
  })

  // Simular convenio visualmente si es edición
  if (s.es_convenio) {
    convenioDetectado.value = {
      nombre_empresa: s.nombre_empresa || 'Convenio Registrado',
      tipo_descuento: 'histórico', 
      valor_descuento: 0
    }
  } else {
    convenioDetectado.value = null
  }
  
  showModal('modalServicio')
}

const guardarServicio = async () => {
  if (!form.placa || !form.tipo_servicio || !form.id_empleado) {
    alert("Por favor complete los campos obligatorios.")
    return
  }
  
  if (tipoRegistro.value === 'convenio' && !form.id_convenio && !modoEdicion.value) {
     alert("Debe validar la placa del convenio primero.")
     return
  }

  try {
    const payload = { ...form, placa: form.placa.toUpperCase() }
    
    if (modoEdicion.value) {
      await api.updateServicio(form.id, payload)
      alert("Servicio actualizado correctamente")
    } else {
      await api.createServicio(payload)
      alert("Servicio registrado exitosamente")
    }
    
    hideModal('modalServicio')
    recargar()
  } catch (err) {
    const msg = err.response?.data?.detail || "Error al guardar"
    alert("Error: " + msg)
  }
}

const cancelarServicio = async (item) => {
  if (!confirm(`¿Cancelar servicio de ${item.placa}?`)) return
  try {
    await api.deleteServicio(item.id)
    recargar()
  } catch (e) {
    alert("No se pudo cancelar.")
  }
}

// Helpers de formato
const formatearServicio = (slug) => slug ? slug.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : ''
const getColorEstado = (e) => ({ 'completado': 'success', 'pendiente': 'warning', 'cancelado': 'secondary' }[e] || 'primary')

// Nota: Si necesitas la función `api.validarConvenioplaca`, asegúrate de que apunte a:
// GET /api/convenios/validar/{placa}
</script>

<style scoped>
.fade-in { animation: fadeIn 0.4s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.bg-indigo { background-color: #6610f2; }
.opacity-75 { opacity: 0.75; }
</style>