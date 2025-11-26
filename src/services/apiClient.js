import axios from 'axios';
import router from '@/router';

// AHORA SÍ: Lee la dirección IP desde el archivo .env
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            try { await router.push('/login'); } catch(e) {}
        } else if (error.code === 'ERR_NETWORK') {
            console.error('Error de conexión: Revisa la IP en tu archivo .env y que el backend esté corriendo.');
        }
        return Promise.reject(error);
    }
);

export default apiClient;