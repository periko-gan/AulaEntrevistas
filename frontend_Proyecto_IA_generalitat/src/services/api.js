/**
 * @file api.js
 * @description Configuración centralizada del cliente Axios para las peticiones a la API.
 * Incluye la URL base y los interceptores para la autenticación y el logging.
 */

import axios from 'axios';
import { getToken } from './authService';

/**
 * @description Instancia de Axios pre-configurada.
 * @type {object}
 */
const apiClient = axios.create({
  /**
   * La URL base para todas las peticiones a la API.
   * Se toma de la variable de entorno VITE_API_URL, o se usa un valor por defecto.
   */
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

/**
 * Interceptor de peticiones de Axios.
 * Se ejecuta antes de que cada petición sea enviada.
 * - Añade el token de autenticación a las cabeceras si existe.
 * - Registra los detalles de la petición en la consola para depuración.
 */
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

/**
 * Interceptor de respuestas de Axios.
 * Se ejecuta cada vez que se recibe una respuesta (exitosa o con error).
 * - Registra los detalles de la respuesta o del error en la consola para depuración.
 */
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
