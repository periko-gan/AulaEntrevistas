import { ref, watch, nextTick, onMounted } from 'vue';
import {
  createChat,
  initializeChat,
  getAiReply,
  getChatDetails,
  getChatMessages,
  updateChatTitle,
} from '../services/chatService';
import { chatState } from '../services/chatState';
import { showInterviewFinishedAlert } from '../services/alertService';

/**
 * @description Composable para gestionar toda la lógica de la interfaz de chat.
 * @param {object} props - Las props del componente que usa el composable.
 * @param {object} props.userData - Los datos del usuario autenticado.
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useChatInterface(props) {
  // --- Estado Reactivo ---
  /** @type {string} */
  const prompt = ref('');
  /** @type {Array<object>} */
  const conversation = ref([]);
  /** @type {boolean} */
  const loading = ref(false);
  /** @type {string} */
  const error = ref('');
  /** @type {HTMLElement|null} */
  const chatWindow = ref(null);
  /** @type {number|null} */
  const chatId = ref(null);
  /** @type {string|null} */
  const chatStatus = ref(null);
  /** @type {string} */
  const chatTitle = ref('Nuevo Chat');
  /** @type {boolean} */
  const isTextareaFocused = ref(false);

  /**
   * @description Carga el historial de mensajes de un chat existente.
   * @param {number} existingChatId - El ID del chat a cargar.
   */
  const loadExistingChat = async (existingChatId) => {
    loading.value = true;
    error.value = '';
    conversation.value = [];

    try {
      const [detailsResponse, messagesResponse] = await Promise.all([
        getChatDetails(existingChatId),
        getChatMessages(existingChatId)
      ]);

      chatId.value = existingChatId;
      sessionStorage.setItem('activeChatId', existingChatId);
      chatTitle.value = detailsResponse.data.title;
      chatStatus.value = detailsResponse.data.status;

      conversation.value = messagesResponse.data.sort((a, b) => a.id_mensaje - b.id_mensaje).map(msg => ({
        id: msg.id_mensaje,
        parts: [{ text: msg.contenido, style: '' }],
        sender: msg.emisor === 'USER' ? 'user' : 'ai'
      }));

    } catch (err) {
      error.value = 'No se pudo cargar el chat anterior. Empezando uno nuevo.';
      console.error('Error al cargar chat existente:', err);
      await startNewChat();
    } finally {
      loading.value = false;
    }
  };

  /**
   * @description Inicia una nueva conversación desde cero, creando un nuevo chat y asignándole un título.
   */
  const startNewChat = async () => {
    loading.value = true;
    error.value = '';
    conversation.value = [];
    chatId.value = null;
    chatStatus.value = null;
    chatTitle.value = 'Nuevo Chat';
    sessionStorage.removeItem('activeChatId');

    try {
      const createResponse = await createChat();
      const newChatId = createResponse.data.id_chat;
      chatId.value = newChatId;
      sessionStorage.setItem('activeChatId', newChatId);

      const now = new Date();
      const date = now.toLocaleDateString('es-ES');
      const time = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
      const userName = props.userData?.nombre || 'Usuario';
      const newTitle = `${userName} - ${date} ${time}`;

      await updateChatTitle(newChatId, newTitle);
      chatTitle.value = newTitle;

      const initResponse = await initializeChat(newChatId);
      const initialMessage = initResponse.data;

      conversation.value.push({
        id: initialMessage.id_mensaje || Date.now(),
        parts: [{ text: initialMessage.contenido, style: '' }],
        sender: 'ai'
      });

      const details = await getChatDetails(newChatId);
      chatStatus.value = details.data.status;

    } catch (err) {
      error.value = 'No se pudo iniciar una nueva conversación con la IA.';
      console.error('Error al inicializar el chat:', err);
    } finally {
      loading.value = false;
    }
  };

  /**
   * @description Hook del ciclo de vida que se ejecuta al montar el componente. Decide si cargar un chat o empezar uno nuevo.
   */
  onMounted(async () => {
    if (chatState.forceNewChat) {
      chatState.forceNewChat = false;
      await startNewChat();
      return;
    }

    const idFromState = chatState.loadChatId;
    chatState.loadChatId = null;

    if (idFromState) {
      try {
        const details = await getChatDetails(idFromState);
        if (details.data.status === 'completed') {
          await showInterviewFinishedAlert();
          await startNewChat();
        } else {
          await loadExistingChat(idFromState);
        }
      } catch (error) {
        console.error("Error al verificar el estado del chat, iniciando uno nuevo:", error);
        await startNewChat();
      }
      return;
    }

    const idFromSession = sessionStorage.getItem('activeChatId');
    if (idFromSession) {
      try {
        const details = await getChatDetails(idFromSession);
        if (details.data.status === 'completed') {
          await showInterviewFinishedAlert();
          await startNewChat();
        } else {
          await loadExistingChat(idFromSession);
        }
      } catch (error) {
        console.error("Error al verificar el estado del chat en sesión, iniciando uno nuevo:", error);
        await startNewChat();
      }
      return;
    }

    await startNewChat();
  });

  /**
   * @description Envía el prompt del usuario a la API y procesa la respuesta de la IA.
   */
  const askApi = async () => {
    if (!prompt.value || loading.value) return;
    const userMessage = prompt.value;
    conversation.value.push({ id: Date.now(), parts: [{ text: userMessage, style: '' }], sender: 'user' });
    prompt.value = '';
    loading.value = true;
    error.value = '';

    try {
      const replyResponse = await getAiReply(chatId.value, userMessage);
      conversation.value.push({
        id: Date.now() + 1,
        parts: [{ text: replyResponse.data.contenido, style: '' }],
        sender: 'ai'
      });

      const details = await getChatDetails(chatId.value);
      chatStatus.value = details.data.status;

    } catch (err) {
      error.value = 'Ha ocurrido un error al contactar con la IA.';
      console.error('Error en la llamada al chat:', err);
    } finally {
      loading.value = false;
    }
  };

  /**
   * @description Maneja el evento de pulsar una tecla en el textarea, enviando el mensaje con Enter.
   * @param {KeyboardEvent} event - El evento del teclado.
   */
  const handleKeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      askApi();
    }
  };

  /**
   * @description Observador que hace auto-scroll hacia el final de la ventana de chat cada vez que la conversación cambia.
   */
  watch(conversation, () => {
    nextTick(() => {
      if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
    });
  }, { deep: true });

  return {
    prompt,
    conversation,
    loading,
    error,
    chatWindow,
    isTextareaFocused,
    askApi,
    handleKeydown,
    startNewChat
  };
}
