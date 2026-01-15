import apiClient from './api'; // Usamos el cliente centralizado

export const register = (userData) => {
  return apiClient.post('/api/v1/auth/register', userData);
};

export const login = (credentials) => {
  // CORRECCIÓN: Enviamos los datos como un objeto JSON.
  // Eliminamos la creación de FormData y el header 'Content-Type'.
  // El cliente 'apiClient' se encargará de enviar esto como application/json por defecto.
  return apiClient.post('/api/v1/auth/login', {
    email: credentials.email,
    password: credentials.password,
  });
};

export const getMe = () => {
  return apiClient.get('/api/v1/auth/me');
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
