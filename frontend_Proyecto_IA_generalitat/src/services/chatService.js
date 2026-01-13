import apiClient from './api';

/**
 * Crea una nueva sesión de chat.
 * Solo necesita el token, que es añadido por el interceptor de apiClient.
 * @returns {Promise<object>} - La respuesta de la API, que contiene { id_chat }.
 */
export const createChat = () => {
  return apiClient.post('/api/v1/chats');
};

/**
 * Envía un mensaje a un chat existente y obtiene una respuesta de la IA.
 * @param {number} chatId - El ID del chat.
 * @param {string} message - El mensaje del usuario.
 * @returns {Promise<object>} - La respuesta de la API.
 */
export const getAiReply = (chatId, message) => {
  return apiClient.post('/api/v1/ai/reply', {
    chat_id: chatId,
    contenido: message,
  });
};
