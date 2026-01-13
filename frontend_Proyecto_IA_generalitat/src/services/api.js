import axios from 'axios';
import { getToken } from './authService';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Interceptor para AÑADIR EL TOKEN a las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // --- LOG DE PETICIÓN ---
    console.log('--- Petición Enviada ---');
    console.log(`URL: ${config.baseURL}${config.url}`);
    console.log('Método:', config.method.toUpperCase());
    if (config.data) {
      console.log('Cuerpo (data):', config.data);
    }
    console.log('------------------------');

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para LOGUEAR LA RESPUESTA
apiClient.interceptors.response.use(
  (response) => {
    // --- LOG DE RESPUESTA ---
    console.log('--- Respuesta Recibida ---');
    console.log('Status:', response.status);
    console.log('Datos:', response.data);
    console.log('--------------------------');

    return response;
  },
  (error) => {
    if (error.response) {
      console.error('--- Error en Respuesta ---');
      console.error('Status:', error.response.status);
      console.error('Datos del error:', error.response.data);
      console.error('--------------------------');
    } else {
      console.error('Error de red o configuración:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
