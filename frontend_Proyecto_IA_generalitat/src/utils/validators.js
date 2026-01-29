/**
 * @file validators.js
 * @description Funciones de utilidad para validaciones comunes.
 */

/**
 * @description Valida que una contraseña cumpla con los requisitos de seguridad.
 * Requisitos:
 * - Mínimo 8 caracteres.
 * - Al menos una letra.
 * - Al menos un número.
 * @param {string} password - La contraseña a validar.
 * @returns {boolean} `true` si la contraseña es válida, `false` en caso contrario.
 */
export const isValidPassword = (password) => {
  if (!password) {
    return false;
  }

  // Comprobar la longitud
  if (password.length < 8) {
    return false;
  }

  // Comprobar que tenga al menos una letra
  const hasLetter = /[a-zA-Z]/.test(password);
  if (!hasLetter) {
    return false;
  }

  // Comprobar que tenga al menos un número
  const hasNumber = /[0-9]/.test(password);
  if (!hasNumber) {
    return false;
  }

  return true;
};
