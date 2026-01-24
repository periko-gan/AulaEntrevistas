import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getChatHistory } from '../services/chatService';
import { chatState } from '../services/chatState';

/**
 * @description Composable para gestionar la lógica del panel lateral (Aside).
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useAside() {
  const router = useRouter();
  /** @type {Array<object>} */
  const chatHistory = ref([]);
  /** @type {boolean} */
  const isLoading = ref(false);
  /** @type {string} */
  const error = ref('');

  /**
   * @description Obtiene y ordena el historial de chats del usuario.
   */
  const fetchChatHistory = async () => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await getChatHistory();
      const sortedChats = response.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
      chatHistory.value = sortedChats;
    } catch (err) {
      console.error('Error al cargar el historial:', err);
      error.value = 'No se pudo cargar el historial.';
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * @description Hook del ciclo de vida que carga el historial de chats al montar el componente.
   */
  onMounted(fetchChatHistory);

  /**
   * @description Maneja la creación de un nuevo chat, actualizando el estado global y navegando a la página de chat.
   */
  const handleNewChat = () => {
    chatState.forceNewChat = true;
    chatState.loadChatId = null;
    router.push({ name: 'Chat' });
  };

  return {
    chatHistory,
    isLoading,
    error,
    fetchChatHistory,
    handleNewChat
  };
}
