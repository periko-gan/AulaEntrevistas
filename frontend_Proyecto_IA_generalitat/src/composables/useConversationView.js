import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getChatDetails, getChatMessages, deleteChat, updateChatTitle, generateDocument } from '../services/chatService';
import { getUser, removeSession } from '../services/authService';
import { chatState } from '../services/chatState';
import {
  showDeleteConfirmation,
  showRenameChatPrompt,
  showGeneratingDocumentLoader,
  closeAlert,
  showSuccessAlert,
  showErrorAlert
} from '../services/alertService';
import { processAiMessage } from '../utils/messageProcessor'; // Importar la función

/**
 * @description Composable para gestionar la lógica de la vista de una conversación individual.
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useConversationView() {
  const route = useRoute();
  const router = useRouter();

  /** @type {object|null} */
  const chatDetails = ref(null);
  /** @type {Array<object>} */
  const chatMessages = ref([]);
  /** @type {object|null} */
  const currentUser = ref(null);
  /** @type {boolean} */
  const isLoading = ref(true);
  /** @type {string} */
  const error = ref('');
  /** @type {object|null} */
  const asideComponent = ref(null);

  // --- Estado del Aside ---
  /** @type {boolean} */
  const isAsideCollapsed = ref(false);
  /**
   * @description Cambia el estado de colapso del panel lateral.
   */
  const toggleAside = () => {
    isAsideCollapsed.value = !isAsideCollapsed.value;
  };

  // --- Lógica para el botón de scroll ---
  /** @type {HTMLElement|null} */
  const mainContent = ref(null);
  /** @type {boolean} */
  const showScrollTopButton = ref(false);

  /**
   * @description Maneja el evento de scroll para mostrar u ocultar el botón de "volver arriba".
   * @param {Event} event - El evento de scroll.
   */
  const handleScroll = (event) => {
    showScrollTopButton.value = event.target.scrollTop > 200;
  };

  /**
   * @description Desplaza la vista suavemente hasta la parte superior.
   */
  const scrollToTop = () => {
    if (mainContent.value) {
      mainContent.value.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  /**
   * @description Carga los detalles y mensajes de una conversación específica.
   * @param {string|number} chatId - El ID del chat a cargar.
   */
  const loadConversation = async (chatId) => {
    isLoading.value = true;
    error.value = '';
    chatDetails.value = null;
    chatMessages.value = [];
    const numericChatId = Number(chatId);
    if (!numericChatId) {
      error.value = 'El ID del chat no es válido.';
      isLoading.value = false;
      return;
    }
    try {
      const [detailsResponse, messagesResponse] = await Promise.all([
        getChatDetails(numericChatId),
        getChatMessages(numericChatId)
      ]);
      chatDetails.value = detailsResponse.data;
      chatMessages.value = messagesResponse.data.sort((a, b) => a.id_mensaje - b.id_mensaje).map(msg => ({
        id: msg.id_mensaje,
        parts: msg.emisor === 'IA' ? processAiMessage(msg.contenido) : [{ text: msg.contenido, style: '' }], // Aplicar formateo aquí
        emisor: msg.emisor // Mantener el emisor original
      }));
    } catch (err) {
      console.error('Error detallado al cargar la conversación:', err.response || err);
      error.value = 'No se pudo cargar la conversación. Revisa la consola para más detalles.';
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * @description Hook del ciclo de vida que carga los datos del usuario y la conversación al montar el componente.
   */
  onMounted(() => {
    currentUser.value = getUser();
    loadConversation(route.params.id);
  });

  /**
   * @description Observador que recarga la conversación si el ID en la URL cambia.
   */
  watch(() => route.params.id, (newId, oldId) => {
    if (newId && newId !== oldId) {
      loadConversation(newId);
    }
  });

  /**
   * @description Propiedad computada que devuelve el primer nombre del usuario con la primera letra en mayúscula.
   * @returns {string}
   */
  const userName = computed(() => {
    if (currentUser.value && currentUser.value.nombre) {
      const firstName = currentUser.value.nombre.split(' ')[0];
      return firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();
    }
    return 'Usuario';
  });

  /**
   * @description Guarda el ID del chat actual en el estado global y navega a la página de chat principal.
   */
  const goBackToChat = () => {
    chatState.loadChatId = route.params.id;
    router.push({ name: 'Chat' });
  };

  /**
   * @description Maneja el proceso de cierre de sesión.
   */
  const handleLogout = async () => {
    const result = await showDeleteConfirmation(); // Reutilizamos la confirmación
    if (result.isConfirmed) {
      removeSession();
      router.push({ name: 'Home' });
    }
  };

  /**
   * @description Maneja el renombramiento del chat actual.
   */
  const handleRenameChat = async () => {
    const { value: newTitle } = await showRenameChatPrompt(chatDetails.value.title);
    if (newTitle && newTitle !== chatDetails.value.title) {
      try {
        await updateChatTitle(route.params.id, newTitle);
        chatDetails.value.title = newTitle;
        showSuccessAlert('¡Éxito!', 'El nombre del chat ha sido actualizado.');
        asideComponent.value?.fetchChatHistory();
      } catch (err) {
        console.error('Error al renombrar el chat:', err);
        showErrorAlert('Error', 'No se pudo cambiar el nombre del chat.');
      }
    }
  };

  /**
   * @description Maneja la eliminación del chat actual.
   */
  const handleDeleteCurrentChat = async () => {
    const result = await showDeleteConfirmation();
    if (result.isConfirmed) {
      try {
        await deleteChat(route.params.id);
        showSuccessAlert('¡Borrado!', 'El chat ha sido eliminado.');
        chatDetails.value = null;
        chatMessages.value = [];
        error.value = 'El chat ha sido eliminado. Selecciona otro chat o vuelve a la página principal.';
        asideComponent.value?.fetchChatHistory();
      } catch (err) {
        console.error('Error al borrar el chat:', err);
        showErrorAlert('Error', 'No se pudo borrar el chat.');
      }
    }
  };

  /**
   * @description Maneja la generación y descarga del informe en PDF.
   */
  const handleGenerateDocument = async () => {
    showGeneratingDocumentLoader();
    try {
      const response = await generateDocument(route.params.id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `conversacion_${route.params.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      closeAlert();
      showSuccessAlert('¡Éxito!', 'El documento se ha descargado.');
    } catch (err) {
      console.error('Error al generar el documento:', err);
      showErrorAlert('Error', 'No se pudo generar el documento.');
    }
  };

  return {
    route,
    chatDetails,
    chatMessages,
    currentUser,
    isLoading,
    error,
    asideComponent,
    isAsideCollapsed,
    mainContent,
    showScrollTopButton,
    userName,
    toggleAside,
    handleScroll,
    scrollToTop,
    goBackToChat,
    handleLogout,
    handleRenameChat,
    handleDeleteCurrentChat,
    handleGenerateDocument
  };
}
