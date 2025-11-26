<template>
  <div class="container-fluid py-4 fade-in">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">
          <i class="bi bi-person-badge me-2"></i>
          Gestión de Empleados
        </h2>
        <p class="text-muted">Administra el personal del lavadero</p>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="abrirModalCrear">
          <i class="bi bi-plus-circle me-2"></i>
          Nuevo Empleado
        </button>
      </div>
    </div>

    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-search"></i></span>
              <input 
                type="text" 
                class="form-control" 
                placeholder="Buscar por nombre o Cédula..."
                v-model="busqueda"
              >
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

    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card border-start border-4 border-primary h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Total Personal</h6>
            <h3 class="mb-0">{{ empleados?.length || 0 }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-start border-4 border-success h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Activos</h6>
            <h3 class="mb-0 text-success">{{ empleadosActivos }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-start border-4 border-warning h-100">
          <div class="card-body">
            <h6 class="text-muted mb-1 text-uppercase small">Comisión Promedio</h6>
            <h3 class="mb-0 text-warning">40% - 50%</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger m-3">
          <i class="bi bi-exclamation-triangle me-2"></i> {{ error }}
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-3">Nombre</th>
                <th>Cédula (C.C.)</th>
                <th>Contacto</th>
                <th>% Comisión</th>
                <th>Estado</th>
                <th class="text-end pe-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="empleadosFiltrados.length === 0">
                <td colspan="6" class="text-center py-5 text-muted">
                  <i class="bi bi-people fs-1 d-block mb-2"></i>
                  No hay empleados registrados con esos criterios.
                </td>
              </tr>
              <tr v-for="empleado in empleadosFiltrados" :key="empleado.id">
                <td class="ps-3">
                  <div class="fw-bold">{{ empleado.nombre }}</div>
                  <small class="text-muted" style="font-size: 0.75rem;">ID: {{ empleado.id }}</small>
                </td>
                <td>{{ empleado.cedula }}</td>
                <td>
                  <div v-if="empleado.telefono">
                    <i class="bi bi-whatsapp text-success me-1"></i> {{ empleado.telefono }}
                  </div>
                  <div v-if="empleado.email" class="small text-muted">{{ empleado.email }}</div>
                </td>
                <td>
                  <span :class="`badge bg-${empleado.porcentaje_comision >= 50 ? 'success' : 'primary'}`">
                    {{ empleado.porcentaje_comision }}%
                  </span>
                </td>
                <td>
                  <span :class="`badge rounded-pill bg-${empleado.estado === 'activo' ? 'success' : 'secondary'}`">
                    {{ empleado.estado === 'activo' ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="text-end pe-3">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" title="Editar" @click="editarEmpleado(empleado)">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button 
                      v-if="empleado.estado === 'activo'"
                      class="btn btn-outline-danger" 
                      title="Desactivar" 
                      @click="eliminarEmpleado(empleado)"
                    >
                      <i class="bi bi-person-x"></i>
                    </button>
                    <button 
                      v-else
                      class="btn btn-outline-success" 
                      title="Reactivar" 
                      @click="reactivarEmpleado(empleado)"
                    >
                      <i class="bi bi-person-check"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalEmpleado" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="bi" :class="form.id ? 'bi-pencil-square' : 'bi-person-plus'"></i>
              {{ form.id ? 'Editar Empleado' : 'Nuevo Empleado' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarEmpleado">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold">Nombre Completo *</label>
                  <input type="text" class="form-control" v-model="form.nombre" required placeholder="Ej: Juan Pérez">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">Cédula (C.C.) *</label>
                  <input type="number" class="form-control" v-model="form.cedula" placeholder="Ej: 1045678900" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">Celular / WhatsApp *</label>
                  <input type="tel" class="form-control" v-model="form.telefono" placeholder="Ej: 300 123 4567" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Correo Electrónico</label>
                  <input type="email" class="form-control" v-model="form.email" placeholder="juan@ejemplo.com">
                </div>
                <div class="col-md-12">
                  <label class="form-label fw-bold">Porcentaje de Comisión *</label>
                  <div class="row g-2">
                    <div class="col-md-6">
                       <select class="form-select" v-model="form.porcentaje_comision" required>
                        <option value="40">40% (Estándar)</option>
                        <option value="50">50% (Convenios / Senior)</option>
                        <option value="0">Sin comisión (Sueldo fijo)</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="col-12 mt-4">
                   <div class="alert alert-light border d-flex align-items-center mb-0">
                    <i class="bi bi-info-circle fs-4 text-primary me-3"></i>
                    <div>
                      <strong>Nota sobre pagos:</strong> Las comisiones se calcularán automáticamente al cerrar el servicio basado en este porcentaje.
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer mt-3 px-0 pb-0 border-top-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-primary">
                  <i class="bi bi-save me-2"></i>
                  {{ form.id ? 'Actualizar Datos' : 'Guardar Empleado' }}
                </button>
              </div>
            </form>
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

// 1. Usar el Composable para manejo de API (Carga de datos)
const { 
  data: empleados, 
  loading, 
  error, 
  exec: cargarEmpleados 
} = useApi(api.getEmpleados)

// 2. Variables reactivas y herramientas
const { showModal, hideModal } = useBootstrap()
const busqueda = ref('')
const filtroEstado = ref('activo')

const form = reactive({
  id: null,
  nombre: '',
  rut: '',
  telefono: '',
  email: '',
  porcentaje_comision: 40
})

// 3. Ciclo de vida
onMounted(() => {
  cargarEmpleados()
})

// 4. Propiedades Computadas (Filtros)
const empleadosFiltrados = computed(() => {
  if (!empleados.value) return []
  return empleados.value.filter(emp => {
    const term = busqueda.value.toLowerCase()
    const rutStr = emp.cedula ? String(emp.cedula) : ''
    
    const matchText = emp.nombre.toLowerCase().includes(term) || cedulaStr.includes(term)
    const matchEstado = filtroEstado.value ? emp.estado === filtroEstado.value : true
    
    return matchText && matchEstado
  })
})

const empleadosActivos = computed(() => {
  if (!empleados.value) return 0
  return empleados.value.filter(e => e.estado === 'activo').length
})

// 5. Funciones (Acciones)
const limpiarFormulario = () => {
  Object.assign(form, {
    id: null,
    nombre: '',
    ceula: '',
    telefono: '',
    email: '',
    porcentaje_comision: 40
  })
}

const abrirModalCrear = () => {
  limpiarFormulario()
  showModal('modalEmpleado')
}

const editarEmpleado = (emp) => {
  // Copiamos los valores al formulario reactivo
  Object.assign(form, {
    id: emp.id,
    nombre: emp.nombre,
    rut: emp.cedula,
    telefono: emp.telefono,
    email: emp.email || '',
    // Nota: El backend devuelve 'porcentaje_comision' (snake_case)
    porcentaje_comision: emp.porcentaje_comision 
  })
  showModal('modalEmpleado')
}

const guardarEmpleado = async () => {
  if (!form.nombre || !form.cedula || !form.telefono) {
    alert("Completa los campos obligatorios (*)")
    return
  }

  try {
    const payload = {
      nombre: form.nombre,
      cedula: String(form.cedula),
      telefono: form.telefono,
      email: form.email,
      porcentaje_comision: parseInt(form.porcentaje_comision)
    }

    if (form.id) {
      await api.updateEmpleado(form.id, payload)
      alert("Empleado actualizado correctamente")
    } else {
      await api.createEmpleado(payload)
      alert("Empleado registrado correctamente")
    }
    
    hideModal('modalEmpleado')
    cargarEmpleados() // Recargar la lista
    limpiarFormulario()
    
  } catch (err) {
    console.error("Error guardar:", err)
    const msg = err.response?.data?.detail || "Verifica la Cédula o conexión"
    alert("Error: " + msg)
  }
}

const eliminarEmpleado = async (emp) => {
  if (!confirm(`¿Estás seguro de desactivar a ${emp.nombre}?\nYa no aparecerá en nuevos servicios.`)) {
    return
  }
  try {
    await api.deleteEmpleado(emp.id)
    alert("Empleado desactivado.")
    cargarEmpleados()
  } catch (err) {
    alert("Error al desactivar empleado")
  }
}

const reactivarEmpleado = (emp) => {
  alert("Funcionalidad de reactivación pendiente de backend")
}
</script>

<style scoped>
.fade-in { animation: fadeIn 0.4s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>