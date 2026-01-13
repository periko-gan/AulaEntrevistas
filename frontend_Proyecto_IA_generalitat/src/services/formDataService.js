// src/services/formDataService.js

import provinciasData from '../assets/provincias.json';
import municipiosData from '../assets/municipios.json';
import centrosData from '../assets/centros.json';

/**
 * Devuelve la lista completa de provincias.
 * @returns {Array}
 */
export const getProvincias = () => {
  return provinciasData;
};

/**
 * Devuelve la lista completa de municipios.
 * @returns {Array}
 */
export const getMunicipios = () => {
  return municipiosData;
};

/**
 * Devuelve la lista completa de centros.
 * @returns {Array}
 */
export const getCentros = () => {
  return centrosData;
};

/**
 * Filtra y devuelve los municipios de una provincia específica.
 * @param {string} provinciaId - El código de la provincia (ej: '03', '12', '46').
 * @returns {Array}
 */
export const getMunicipiosByProvincia = (provinciaId) => {
  if (!provinciaId) return [];
  return municipiosData.filter(m => m.codigo.startsWith(provinciaId));
};

/**
 * Filtra y devuelve los centros de una provincia específica.
 * @param {string} provinciaId - El código de la provincia.
 * @returns {Array}
 */
export const getCentrosByProvincia = (provinciaId) => {
  if (!provinciaId) return [];
  return centrosData.filter(c => c.codigo_provincia === provinciaId);
};
