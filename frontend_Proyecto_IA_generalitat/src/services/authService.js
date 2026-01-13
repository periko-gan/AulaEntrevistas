import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/auth'; // URL base de tu API

const apiClient = axios.create({
  baseURL: API_URL,
});

// Interceptor para añadir el token a todas las peticiones que lo necesiten
apiClient.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const register = (userData) => {
  return axios.post(`${API_URL}/register`, userData);
};

/**
 * Inicia sesión de un usuario.
 * @param {object} credentials - Credenciales del usuario { email, password }.
 * @returns {Promise<object>}
 */
export const login = (credentials) => {
  // CORRECCIÓN: Se envía como JSON, asumiendo que el backend espera un objeto.
  return axios.post(`${API_URL}/login`, {
    email: credentials.email,
    password: credentials.password,
  });
};

/**
 * Obtiene los datos del usuario actual.
 * @returns {Promise<object>}
 */
export const getMe = () => {
  return apiClient.get('/me');
};

// --- Gestión de Sesión ---

export const saveToken = (token) => {
  localStorage.setItem('user-token', token);
};

export const getToken = () => {
  return localStorage.getItem('user-token');
};

export const saveUser = (user) => {
  localStorage.setItem('user-data', JSON.stringify(user));
};

export const getUser = () => {
  const user = localStorage.getItem('user-data');
  return user ? JSON.parse(user) : null;
};

export const removeSession = () => {
  localStorage.removeItem('user-token');
  localStorage.removeItem('user-data');
};
