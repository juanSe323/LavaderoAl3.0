import apiClient from '../apiClient';

export default {
    async getConvenios() {
        const response = await apiClient.get('/convenios');
        return response.data;
    },
    async createConvenio(data) {
        const response = await apiClient.post('/convenios', data);
        return response.data;
    },
    async updateConvenio(id, data) {
        const response = await apiClient.put(`/convenios/${id}`, data);
        return response.data;
    },
    async deleteConvenio(id) {
        const response = await apiClient.delete(`/convenios/${id}`);
        return response.data;
    },
    // Vehículos
    async getVehiculosConvenio(idConvenio) {
        const response = await apiClient.get(`/convenios/${idConvenio}/vehiculos`);
        return response.data;
    },
    async addVehiculoConvenio(idConvenio, vehiculo) {
        const response = await apiClient.post(`/convenios/${idConvenio}/vehiculos`, vehiculo);
        return response.data;
    },
    async removeVehiculoConvenio(idVehiculo) {
        const response = await apiClient.delete(`/convenios/vehiculos/${idVehiculo}`);
        return response.data;
    },
    // Validación (necesaria para ServiciosView)
    async validarConvenioplaca(placa) {
        const response = await apiClient.get(`/convenios/validar/${placa}`);
        return response.data;
    }
}