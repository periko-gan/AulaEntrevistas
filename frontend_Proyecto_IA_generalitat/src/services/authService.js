import apiClient from './api';

/**
 * Registra un nuevo usuario en el sistema.
 * @param {object} userData - Los datos del usuario a registrar.
 * @param {string} userData.nombre - El nombre completo del usuario.
 * @param {string} userData.email - El correo electrónico del usuario.
 * @param {string} userData.password - La contraseña del usuario.
 * @returns {Promise<object>} Una promesa que se resuelve con la respuesta de la API, incluyendo el token de acceso.
 */
export const register = (userData) => {
  return apiClient.post('/api/v1/auth/register', userData);
};

/**
 * Inicia sesión de un usuario con sus credenciales.
 * @param {object} credentials - Las credenciales del usuario.
 * @param {string} credentials.email - El correo electrónico del usuario.
 * @param {string} credentials.password - La contraseña del usuario.
 * @returns {Promise<object>} Una promesa que se resuelve con la respuesta de la API, incluyendo el token de acceso.
 */
export const login = (credentials) => {
  return apiClient.post('/api/v1/auth/login', {
    email: credentials.email,
    password: credentials.password,
  });
};

/**
 * Obtiene los datos del usuario autenticado actualmente.
 * @returns {Promise<object>} Una promesa que se resuelve con los datos del usuario.
 */
export const getMe = () => {
  return apiClient.get('/api/v1/auth/me');
};

// --- Gestión de Sesión ---

/**
 * Guarda el token de autenticación en el localStorage.
 * @param {string} token - El token JWT a guardar.
 */
export const saveToken = (token) => {
  localStorage.setItem('user-token', token);
};

/**
 * Obtiene el token de autenticación del localStorage.
 * @returns {string|null} El token JWT si existe, o null si no.
 */
export const getToken = () => {
  return localStorage.getItem('user-token');
};

/**
 * Guarda los datos del usuario en el localStorage.
 * @param {object} user - El objeto de usuario a guardar.
 */
export const saveUser = (user) => {
  localStorage.setItem('user-data', JSON.stringify(user));
};

/**
 * Obtiene los datos del usuario del localStorage.
 * @returns {object|null} El objeto de usuario si existe, o null si no.
 */
export const getUser = () => {
  const user = localStorage.getItem('user-data');
  return user ? JSON.parse(user) : null;
};

/**
 * Elimina la sesión del usuario del localStorage (token y datos).
 */
export const removeSession = () => {
  localStorage.removeItem('user-token');
  localStorage.removeItem('user-data');
};
