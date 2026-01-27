/**
 * @file alertService.js
 * @description Módulo centralizado para gestionar todas las notificaciones y modales de SweetAlert2.
 */

import Swal from 'sweetalert2';

/**
 * Muestra una alerta de bienvenida centrada después de un inicio de sesión exitoso.
 * @param {string} userName - El nombre del usuario para mostrar en el saludo.
 * @returns {Promise<object>}
 */
export const showWelcomeAlert = (userName) => {
  return Swal.fire({
    position: 'center',
    icon: 'success',
    title: `¡Bienvenido, ${userName}!`,
    showConfirmButton: false,
    timer: 1500
  });
};

/**
 * Muestra una alerta de registro completado.
 * @param {string} userName - El nombre del usuario para mostrar en el saludo.
 * @returns {Promise<object>}
 */
export const showRegistrationSuccessAlert = (userName) => {
  return Swal.fire({
    position: 'center',
    icon: 'success',
    title: '¡Registro completado!',
    text: `Bienvenido, ${userName}.`,
    showConfirmButton: false,
    timer: 2000
  });
};

/**
 * Muestra una alerta de confirmación antes de realizar una acción destructiva (ej. borrar un chat).
 * @returns {Promise<object>}
 */
export const showDeleteConfirmation = () => {
  return Swal.fire({
    title: '¿Estás seguro?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, borrar',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#d33',
  });
};

/**
 * Muestra un modal con un campo de texto para que el usuario renombre un chat.
 * @param {string} currentTitle - El título actual del chat, para pre-rellenar el campo.
 * @returns {Promise<object>}
 */
export const showRenameChatPrompt = (currentTitle) => {
  return Swal.fire({
    title: 'Cambiar nombre del chat',
    input: 'text',
    inputValue: currentTitle,
    inputPlaceholder: 'Nuevo nombre',
    showCancelButton: true,
    confirmButtonText: 'Guardar',
    cancelButtonText: 'Cancelar',
  });
};

/**
 * Muestra una notificación de éxito centrada.
 * @param {string} title - El título de la notificación.
 * @param {string} [text=''] - El texto opcional de la notificación.
 * @returns {Promise<object>}
 */
export const showSuccessAlert = (title, text = '') => {
  return Swal.fire({
    position: 'center',
    icon: 'success',
    title,
    text,
    showConfirmButton: false,
    timer: 1500
  });
};

/**
 * Muestra una notificación de error centrada.
 * @param {string} title - El título de la notificación.
 * @param {string} [text=''] - El texto opcional de la notificación.
 * @returns {Promise<object>}
 */
export const showErrorAlert = (title, text = '') => {
  return Swal.fire({
    position: 'center',
    icon: 'error',
    title,
    text,
    showConfirmButton: true
  });
};

/**
 * Muestra una alerta informativa para notificar que una entrevista ha finalizado.
 * @returns {Promise<object>}
 */
export const showInterviewFinishedAlert = () => {
  return Swal.fire({
    title: 'Entrevista Finalizada',
    text: 'Esta entrevista ya ha concluido. Se iniciará un nuevo chat.',
    icon: 'info',
  });
};

/**
 * Muestra un modal de confirmación al finalizar un chat, preguntando si se desea descargar el PDF.
 * @returns {Promise<object>}
 */
export const showCompletionPrompt = () => {
  return Swal.fire({
    title: '¡Chat Finalizado!',
    text: '¿Deseas descargar el informe de esta conversación?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Sí, descargar PDF',
    cancelButtonText: 'No, gracias',
    reverseButtons: true,
  });
};

/**
 * Muestra un modal de "cargando" sin botones, útil para operaciones asíncronas largas.
 */
export const showGeneratingDocumentLoader = () => {
  Swal.fire({
    title: 'Generando documento...',
    text: 'Por favor, espera un momento.',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });
};

/**
 * Cierra cualquier modal de SweetAlert2 que esté abierto actualmente.
 */
export const closeAlert = () => {
  Swal.close();
};
