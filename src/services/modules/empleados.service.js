import apiClient from '../apiClient';

export default {
    async getEmpleados() {
        const response = await apiClient.get('/empleados');
        return response.data;
    },
    async createEmpleado(empleado) {
        const response = await apiClient.post('/empleados', empleado);
        return response.data;
    },
    async updateEmpleado(id, empleado) {
        const response = await apiClient.put(`/empleados/${id}`, empleado);
        return response.data;
    },
    async deleteEmpleado(id) {
        const response = await apiClient.delete(`/empleados/${id}`);
        return response.data;
    },
    // En src/services/modules/empleados.service.js (o api.js según tu estructura)
    // En el objeto de servicios de empleados
     reactivarEmpleado(id) {
    return apiClient.put(`/empleados/${id}/reactivar`);
}
}
