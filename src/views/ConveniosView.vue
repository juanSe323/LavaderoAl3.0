<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-briefcase me-2"></i>
          Convenios Corporativos
        </h2>
        <p class="text-muted">Gestiona empresas, descuentos y flotas autorizadas</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="abrirModalCrear">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Convenio
        </button>
      </div>
    </div>

    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-5">
            <div class="input-group">
              <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
              <input type="text" class="form-control border-start-0" placeholder="Buscar por empresa o NIT..." v-model="busqueda">
            </div>
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="filtroEstado">
              <option value="">Todos los estados</option>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else-if="error" class="alert alert-danger m-3">{{ error }}</div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-3">Empresa / Cliente</th>
                <th>Contacto</th>
                <th>Descuento</th>
                <th>Vigencia</th>
                <th class="text-center">Flota</th>
                <th>Estado</th>
                <th class="text-end pe-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in conveniosFiltrados" :key="c.id">
                <td class="ps-3">
                  <div class="fw-bold">{{ c.nombre_empresa }}</div>
                  <small class="text-muted">NIT: {{ c.nit_empresa }}</small>
                </td>
                <td>
                  <div>{{ c.contacto }}</div>
                  <small class="text-muted"><i class="bi bi-telephone me-1"></i>{{ c.telefono }}</small>
                </td>
                <td>
                  <span class="badge" :class="c.tipo_descuento === 'porcentaje' ? 'bg-primary' : 'bg-info'">
                    {{ c.tipo_descuento === 'porcentaje' ? '%' : '$' }}
                  </span>
                  <span class="fw-bold ms-1">
                     {{ c.tipo_descuento === 'porcentaje' ? c.valor_descuento + '%' : '$' + c.valor_descuento.toLocaleString() }}
                  </span>
                </td>
                <td>
                  <small>{{ formatDate(c.fecha_inicio) }}</small> <br>
                  <small class="text-muted">hasta {{ formatDate(c.fecha_termino) }}</small>
                </td>
                <td class="text-center">
                  <button class="btn btn-sm btn-outline-secondary position-relative" @click="verVehiculos(c)">
                    <i class="bi bi-car-front-fill"></i>
                    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" v-if="c.total_vehiculos > 0">
                      {{ c.total_vehiculos }}
                    </span>
                  </button>
                </td>
                <td>
                  <span :class="'badge rounded-pill bg-' + (c.estado === 'activo' ? 'success' : 'secondary')">
                    {{ c.estado }}
                  </span>
                </td>
                <td class="text-end pe-3">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" title="Editar" @click="editarConvenio(c)">
                      <i class="bi bi-pencil"></i>
                    </button>
                    
                    <button 
                      v-if="c.estado === 'activo'" 
                      class="btn btn-outline-danger" 
                      title="Desactivar" 
                      @click="eliminarConvenio(c)"
                    >
                      <i class="bi bi-slash-circle"></i>
                    </button>

                    <button 
                      v-else 
                      class="btn btn-outline-success" 
                      title="Reactivar" 
                      @click="reactivarConvenio(c)"
                    >
                      <i class="bi bi-check-circle"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalConvenio" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">{{ form.id ? 'Editar Convenio' : 'Nuevo Convenio Corporativo' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarConvenio">
              <h6 class="text-primary border-bottom pb-2 mb-3">Información de la Empresa</h6>
              <div class="row g-3 mb-4">
                <div class="col-md-6">
                  <label class="form-label fw-bold">Razón Social *</label>
                  <input type="text" class="form-control" v-model="form.nombre_empresa" required placeholder="Ej: Transportes SAS">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">NIT *</label>
                  <input type="text" class="form-control" v-model="form.nit_empresa" required placeholder="Ej: 900.123.456-7">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Persona de Contacto</label>
                  <input type="text" class="form-control" v-model="form.contacto">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Teléfono *</label>
                  <input type="text" class="form-control" v-model="form.telefono" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Email Corporativo</label>
                  <input type="email" class="form-control" v-model="form.email">
                </div>
              </div>

              <h6 class="text-primary border-bottom pb-2 mb-3">Condiciones del Convenio</h6>
              <div class="row g-3 mb-4">
                <div class="col-md-3">
                  <label class="form-label fw-bold">Tipo Descuento</label>
                  <select class="form-select" v-model="form.tipo_descuento">
                    <option value="porcentaje">Porcentaje (%)</option>
                    <option value="monto_fijo">Monto Fijo ($)</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-bold">Valor</label>
                  <input type="number" class="form-control" v-model="form.valor_descuento" required min="0">
                </div>
                <div class="col-md-3">
                  <label class="form-label">Inicio</label>
                  <input type="date" class="form-control" v-model="form.fecha_inicio" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Término</label>
                  <input type="date" class="form-control" v-model="form.fecha_termino">
                </div>
              </div>

              <div v-if="!form.id">
                <h6 class="text-primary border-bottom pb-2 mb-3 d-flex justify-content-between align-items-center">
                  Vehículos Iniciales (Opcional)
                  <button type="button" class="btn btn-sm btn-outline-success" @click="agregarFilaVehiculoTemp">
                    <i class="bi bi-plus"></i> Agregar Fila
                  </button>
                </h6>
                <div class="table-responsive bg-light p-2 rounded">
                  <table class="table table-sm table-borderless mb-0">
                    <thead>
                      <tr class="text-muted small">
                        <th>placa *</th>
                        <th>Tipo *</th>
                        <th>Modelo</th>
                        <th>Color</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(v, index) in vehiculosTemp" :key="index">
                        <td><input type="text" class="form-control form-control-sm text-uppercase" v-model="v.placa" placeholder="ABC-123"></td>
                        <td>
                          <select class="form-select form-select-sm" v-model="v.tipo_vehiculo">
                            <option value="auto">Auto</option>
                            <option value="camioneta">Camioneta</option>
                            <option value="suv">SUV</option>
                            <option value="furgon">Furgón</option>
                          </select>
                        </td>
                        <td><input type="text" class="form-control form-control-sm" v-model="v.modelo" placeholder="Ej: Hilux"></td>
                        <td><input type="text" class="form-control form-control-sm" v-model="v.color" placeholder="Blanco"></td>
                        <td><button type="button" class="btn btn-sm text-danger" @click="vehiculosTemp.splice(index, 1)"><i class="bi bi-x-lg"></i></button></td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="text-muted small mt-2" v-if="vehiculosTemp.length === 0">No se añadirán vehículos por ahora. Podrás hacerlo después.</div>
                </div>
              </div>
              
              <div class="mt-4 text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar Convenio</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalVehiculos" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Flota de {{ convenioSeleccionado?.nombre_empresa }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="card bg-light border-0 mb-3" v-if="convenioSeleccionado?.estado === 'activo'">
              <div class="card-body">
                <h6 class="card-title small fw-bold text-muted mb-2">AGREGAR VEHÍCULO NUEVO</h6>
                <div class="row g-2 align-items-end">
                  <div class="col-md-3">
                    <label class="small">placa</label>
                    <input type="text" class="form-control form-control-sm text-uppercase" v-model="nuevoVehiculo.placa" placeholder="AAA-123">
                  </div>
                  <div class="col-md-3">
                     <label class="small">Tipo</label>
                     <select class="form-select form-select-sm" v-model="nuevoVehiculo.tipo_vehiculo">
                        <option value="auto">Auto</option>
                        <option value="camioneta">Camioneta</option>
                        <option value="suv">SUV</option>
                        <option value="furgon">Furgón</option>
                     </select>
                  </div>
                  <div class="col-md-3">
                    <label class="small">Modelo</label>
                    <input type="text" class="form-control form-control-sm" v-model="nuevoVehiculo.modelo">
                  </div>
                  <div class="col-md-2">
                    <label class="small">Color</label>
                    <input type="text" class="form-control form-control-sm" v-model="nuevoVehiculo.color" placeholder="Ej: Rojo">
                  </div>
                  <div class="col-md-3">
                    <button class="btn btn-sm btn-success w-100" @click="agregarVehiculoIndividual">
                      <i class="bi bi-plus-lg"></i> Agregar
                    </button>
                    
                  </div>
                </div>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-hover table-sm">
                <thead>
                  <tr>
                    <th>placa</th>
                    <th>Tipo</th>
                    <th>Modelo</th>
                    <th>Color</th>
                    <th class="text-end">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="v in vehiculosLista" :key="v.id">
                    <td class="fw-bold">{{ v.placa }}</td>
                    <td>{{ v.tipo_vehiculo.toUpperCase() }}</td>
                    <td>{{ v.modelo || '-' }}</td>
                    <td>{{ v.color || '-' }}</td>
                    <td class="text-end">
                      <button class="btn btn-sm btn-outline-danger border-0" @click="eliminarVehiculo(v.id)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="vehiculosLista.length === 0">
                    <td colspan="5" class="text-center text-muted py-3">No hay vehículos registrados en este convenio.</td>
                  </tr>
                </tbody>
              </table>
            </div>
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
const { data: convenios, loading, error, exec: cargarConvenios } = useApi(api.getConvenios)

// 2. Variables y Estado
const { showModal, hideModal } = useBootstrap()
const busqueda = ref('')
const filtroEstado = ref('activo')

const form = reactive({
  id: null,
  nombre_empresa: '',
  nit_empresa: '',
  contacto: '',
  telefono: '',
  email: '',
  tipo_descuento: 'porcentaje',
  valor_descuento: 0,
  fecha_inicio: '',
  fecha_termino: '',
  observaciones: ''
})

// Vehículos Temporales (Creación masiva)
const vehiculosTemp = ref([])

// Gestión Modal Vehículos
const convenioSeleccionado = ref(null)
const vehiculosLista = ref([])
const nuevoVehiculo = reactive({ placa: '', tipo_vehiculo: 'auto', modelo: '', color: '' })

// 3. Ciclo de vida
onMounted(() => {
  cargarConvenios()
})

// 4. Computados
const conveniosFiltrados = computed(() => {
  if (!convenios.value) return []
  return convenios.value.filter(c => {
    const term = busqueda.value.toLowerCase()
    const matchText = c.nombre_empresa.toLowerCase().includes(term) || c.nit_empresa.includes(term)
    const matchEst = filtroEstado.value ? c.estado === filtroEstado.value : true
    return matchText && matchEst
  })
})

// 5. Acciones (CRUD Convenio)
const limpiarForm = () => {
  Object.assign(form, {
    id: null, nombre_empresa: '', nit_empresa: '', contacto: '', telefono: '', 
    email: '', tipo_descuento: 'porcentaje', valor_descuento: 0, 
    fecha_inicio: new Date().toISOString().split('T')[0], fecha_termino: '', observaciones: ''
  })
}

const abrirModalCrear = () => {
  limpiarForm()
  vehiculosTemp.value = []
  showModal('modalConvenio')
}

const editarConvenio = (c) => {
  Object.assign(form, c)
  // Ajuste fechas para input date (YYYY-MM-DD)
  if(form.fecha_inicio) form.fecha_inicio = form.fecha_inicio.toString().split('T')[0]
  if(form.fecha_termino) form.fecha_termino = form.fecha_termino.toString().split('T')[0]
  
  showModal('modalConvenio')
}

const guardarConvenio = async () => {
  try {
    const payload = { ...form }
    
    let idConvenio
    if (payload.id) {
      await api.updateConvenio(payload.id, payload)
      alert("Convenio actualizado correctamente")
    } else {
      // 1. Crear el Convenio
      const res = await api.createConvenio(payload)
      idConvenio = res.id
      
      // 2. Agregar vehículos (Manejo de errores individual)
      let vehiculosGuardados = 0
      let vehiculosFallidos = []

      if (vehiculosTemp.value.length > 0) {
        for (const v of vehiculosTemp.value) {
          if (v.placa) {
            try {
              await api.addVehiculoConvenio(idConvenio, v)
              vehiculosGuardados++
            } catch (errorVehiculo) {
              console.error("Error agregando vehículo:", v.placa, errorVehiculo)
              vehiculosFallidos.push(v.placa)
            }
          }
        }
      }

      // 3. Mensaje final inteligente
      if (vehiculosFallidos.length > 0) {
        alert(`Convenio creado con éxito.\n\nSe agregaron ${vehiculosGuardados} vehículos.\nNO se pudieron agregar las siguientes placas (posiblemente duplicadas): ${vehiculosFallidos.join(', ')}`)
      } else {
        alert("Convenio y vehículos registrados exitosamente")
      }
    }

    hideModal('modalConvenio')
    cargarConvenios()
    
  } catch (err) {
    alert("Error al guardar convenio: " + (err.response?.data?.detail || err.message))
  }
}

const eliminarConvenio = async (c) => {
  if(!confirm(`¿Desactivar convenio con ${c.nombre_empresa}?`)) return
  try {
    await api.deleteConvenio(c.id)
    cargarConvenios()
  } catch(e) { alert("Error al eliminar") }
}

// 6. Acciones (Vehículos)
const agregarFilaVehiculoTemp = () => {
  vehiculosTemp.value.push({ placa: '', tipo_vehiculo: 'auto', modelo: '', color: '' })
}

const verVehiculos = async (c) => {
  convenioSeleccionado.value = c
  Object.assign(nuevoVehiculo, { placa: '', tipo_vehiculo: 'auto', modelo: '', color: '' })
  try {
    vehiculosLista.value = await api.getVehiculosConvenio(c.id)
    showModal('modalVehiculos')
  } catch(e) { console.error(e) }
}
const reactivarConvenio = async (c) => {
  if(!confirm(`¿Reactivar el convenio con ${c.nombre_empresa}?`)) return
  try {
    // Reutilizamos el endpoint de update enviando solo el estado
    await api.updateConvenio(c.id, { estado: 'activo' })
    alert("Convenio reactivado exitosamente")
    cargarConvenios()
  } catch(e) { 
    alert("Error al reactivar: " + (e.response?.data?.detail || e.message)) 
  }
}
const agregarVehiculoIndividual = async () => {
  if(!nuevoVehiculo.placa) return alert("Falta placa")
  try {
    await api.addVehiculoConvenio(convenioSeleccionado.value.id, nuevoVehiculo)
    // Reset y recargar
    Object.assign(nuevoVehiculo, { placa: '', tipo_vehiculo: 'auto', modelo: '', color: '' })
    vehiculosLista.value = await api.getVehiculosConvenio(convenioSeleccionado.value.id)
    cargarConvenios() // Actualizar contador
  } catch (err) {
    alert("Error: " + (err.response?.data?.detail || "No se pudo agregar"))
  }
}

const eliminarVehiculo = async (idVehiculo) => {
  if(!confirm("¿Quitar vehículo del convenio?")) return
  try {
    await api.removeVehiculoConvenio(idVehiculo)
    vehiculosLista.value = vehiculosLista.value.filter(v => v.id !== idVehiculo)
    cargarConvenios()
  } catch(e) { alert("Error al quitar vehículo") }
}

// Helpers
const formatDate = (dateStr) => {
  if(!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-CO')
}
</script>

<style scoped>
.fade-in { animation: fadeIn 0.4s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>