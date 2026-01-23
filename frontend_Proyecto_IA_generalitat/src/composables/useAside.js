import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getChatHistory } from '../services/chatService';
import { chatState } from '../services/chatState';

export function useAside() {
  const router = useRouter();
  const chatHistory = ref([]);
  const isLoading = ref(false);
  const error = ref('');

  // --- Lógica de Carga del Historial ---
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

  onMounted(fetchChatHistory);

  // --- Manejador de Nuevo Chat ---
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
