import apiClient from './api';

/**
 * Crea una nueva sesión de chat.
 * @returns {Promise<object>}
 */
export const createChat = () => {
  return apiClient.post('/api/v1/chats');
};

/**
 * Envía un mensaje a un chat existente.
 * @param {number} chatId - El ID del chat.
 * @param {string} message - El mensaje del usuario.
 * @returns {Promise<object>}
 */
export const getAiReply = (chatId, message) => {
  return apiClient.post('/api/v1/ai/reply', {
    chat_id: chatId,
    contenido: message,
  });
};

/**
 * Obtiene el historial de chats de un usuario.
 * @returns {Promise<Array<object>>}
 */
export const getChatHistory = () => {
  return apiClient.get('/api/v1/chats');
};

/**
 * Elimina un chat específico por su ID.
 * @param {number} chatId - El ID del chat a eliminar.
 * @returns {Promise<object>}
 */
export const deleteChat = (chatId) => {
  return apiClient.delete(`/api/v1/chats/${chatId}`);
};

/**
 * Obtiene la conversación completa de un chat específico.
 * @param {number} chatId - El ID del chat a recuperar.
 * @returns {Promise<object>}
 */
export const getChatConversation = (chatId) => {
  return apiClient.get(`/api/v1/chats/${chatId}`);
};

/**
 * Actualiza el título de un chat.
 * @param {number} chatId - El ID del chat a actualizar.
 * @param {string} newTitle - El nuevo título para el chat.
 * @returns {Promise<object>}
 */
export const updateChatTitle = (chatId, newTitle) => {
  return apiClient.put(`/api/v1/chats/${chatId}`, {
    title: newTitle,
  });
};
