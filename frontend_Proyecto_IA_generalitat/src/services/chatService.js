import apiClient from './api';

/**
 * Crea un nuevo chat en el backend y devuelve su ID.
 * @returns {Promise<object>} Una promesa que se resuelve con la respuesta de la API, incluyendo el id_chat.
 */
export const createChat = () => {
  return apiClient.post('/api/v1/chats');
};

/**
 * Inicializa la conversación con la IA para un chat recién creado.
 * @param {number} chatId - El ID del chat a inicializar.
 * @returns {Promise<object>} Una promesa que se resuelve con la respuesta de la API, incluyendo el primer mensaje de la IA.
 */
export const initializeChat = (chatId) => {
  return apiClient.post('/api/v1/ai/initialize', { chat_id: chatId });
};

/**
 * Envía un mensaje a un chat existente y obtiene la respuesta de la IA.
 * @param {number} chatId - El ID del chat.
 * @param {string} message - El mensaje del usuario.
 * @returns {Promise<object>} Una promesa que se resuelve con la respuesta de la IA.
 */
export const getAiReply = (chatId, message) => {
  return apiClient.post('/api/v1/ai/reply', {
    chat_id: chatId,
    contenido: message,
  });
};

/**
 * Obtiene el historial de todos los chats del usuario autenticado.
 * @returns {Promise<Array<object>>} Una promesa que se resuelve con un array de objetos de chat.
 */
export const getChatHistory = () => {
  return apiClient.get('/api/v1/chats');
};

/**
 * Elimina un chat específico por su ID.
 * @param {number} chatId - El ID del chat a eliminar.
 * @returns {Promise<object>} Una promesa que se resuelve con la confirmación de la eliminación.
 */
export const deleteChat = (chatId) => {
  return apiClient.delete(`/api/v1/chats/${chatId}`);
};

/**
 * Obtiene los detalles de un chat específico (título, estado, etc.).
 * @param {number} chatId - El ID del chat a recuperar.
 * @returns {Promise<object>} Una promesa que se resuelve con los detalles del chat.
 */
export const getChatDetails = (chatId) => {
  return apiClient.get(`/api/v1/chats/${chatId}`);
};

/**
 * Obtiene todos los mensajes de una conversación específica.
 * @param {number} chatId - El ID del chat del que se quieren obtener los mensajes.
 * @returns {Promise<Array<object>>} Una promesa que se resuelve con un array de objetos de mensaje.
 */
export const getChatMessages = (chatId) => {
  return apiClient.get('/api/v1/messages', {
    params: { chat_id: chatId }
  });
};

/**
 * Actualiza el título de un chat específico.
 * @param {number} chatId - El ID del chat a actualizar.
 * @param {string} newTitle - El nuevo título para el chat.
 * @returns {Promise<object>} Una promesa que se resuelve con la confirmación de la actualización.
 */
export const updateChatTitle = (chatId, newTitle) => {
  const url = `/api/v1/chats/${chatId}/title`;
  const payload = { title: newTitle };
  return apiClient.put(url, payload);
};

/**
 * Solicita la generación de un informe en PDF para un chat específico.
 * @param {number} chatId - El ID del chat para el que se generará el informe.
 * @returns {Promise<Blob>} Una promesa que se resuelve con la respuesta de la API como un objeto Blob (el archivo PDF).
 */
export const generateDocument = (chatId) => {
  return apiClient.post('/api/v1/ai/generate-report',
    { chat_id: chatId },
    { responseType: 'blob' }
  );
};
