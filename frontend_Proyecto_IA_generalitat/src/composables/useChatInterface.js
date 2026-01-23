import { ref, watch, nextTick, onMounted } from 'vue';
import {
  createChat,
  initializeChat,
  getAiReply,
  getChatDetails,
  getChatMessages,
  updateChatTitle,
  deleteChat
} from '../services/chatService';
import { chatState } from '../services/chatState';
import Swal from 'sweetalert2';

export function useChatInterface(props) {
  // --- Estado del Componente ---
  const prompt = ref('');
  const conversation = ref([]);
  const loading = ref(false);
  const error = ref('');
  const chatWindow = ref(null);
  const chatId = ref(null);
  const chatStatus = ref(null);
  const chatTitle = ref('Nuevo Chat');
  const isTextareaFocused = ref(false);

  // --- Lógica de Carga de Chat Existente ---
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

  // --- Lógica de Inicialización de Chat Nuevo ---
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

  // --- Hook de Ciclo de Vida ---
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
          await Swal.fire({
            title: 'Entrevista Finalizada',
            text: 'Esta entrevista ya ha concluido. Se iniciará un nuevo chat.',
            icon: 'info',
          });
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
          await Swal.fire({
            title: 'Entrevista Finalizada',
            text: 'Esta entrevista ya ha concluido. Se iniciará un nuevo chat.',
            icon: 'info',
          });
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

  // --- Lógica de la Conversación ---
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

  // --- Manejadores de Eventos ---
  const handleKeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      askApi();
    }
  };

  // --- Auto-scroll ---
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
