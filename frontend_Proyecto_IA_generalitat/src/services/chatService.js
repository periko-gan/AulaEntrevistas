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
 * Obtiene los detalles de un chat (título, etc.).
 * @param {number} chatId - El ID del chat a recuperar.
 * @returns {Promise<object>}
 */
export const getChatDetails = (chatId) => {
  return apiClient.get(`/api/v1/chats/${chatId}`);
};

/**
 * Obtiene los mensajes de una conversación.
 * @param {number} chatId - El ID del chat.
 * @returns {Promise<Array<object>>}
 */
export const getChatMessages = (chatId) => {
  return apiClient.get('/api/v1/messages', {
    params: { chat_id: chatId }
  });
};

/**
 * Actualiza el título de un chat.
 * @param {number} chatId - El ID del chat a actualizar.
 * @param {string} newTitle - El nuevo título para el chat.
 * @returns {Promise<object>}
 */
export const updateChatTitle = (chatId, newTitle) => {
  const url = `/api/v1/chats/${chatId}/title`;
  const payload = { title: newTitle };
  console.log(`Enviando PUT a: ${url}`, payload);
  return apiClient.put(url, payload);
};

/**
 * Solicita la generación de un documento PDF para un chat.
 * @param {number} chatId - El ID del chat.
 * @returns {Promise<Blob>} - La respuesta de la API como un objeto Blob.
 */
export const generateDocument = (chatId) => {
  return apiClient.post('/api/v1/ai/generate-report',
    { chat_id: chatId },
    { responseType: 'blob' }
  );
};
