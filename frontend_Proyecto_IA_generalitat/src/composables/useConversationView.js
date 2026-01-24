import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getChatDetails, getChatMessages, deleteChat, updateChatTitle, generateDocument } from '../services/chatService';
import { getUser, removeSession } from '../services/authService';
import { chatState } from '../services/chatState';
import Swal from 'sweetalert2';

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
      chatMessages.value = messagesResponse.data.sort((a, b) => a.id_mensaje - b.id_mensaje);
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
    const result = await Swal.fire({
      title: '¿Quieres cerrar la sesión?',
      text: 'Serás redirigido a la página de inicio.',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Sí, cerrar sesión',
      cancelButtonText: 'Cancelar',
    });
    if (result.isConfirmed) {
      removeSession();
      router.push({ name: 'Home' });
    }
  };

  /**
   * @description Maneja el renombramiento del chat actual.
   */
  const handleRenameChat = async () => {
    const { value: newTitle } = await Swal.fire({
      title: 'Cambiar nombre del chat',
      input: 'text',
      inputPlaceholder: chatDetails.value.title,
      showCancelButton: true,
      confirmButtonText: 'Guardar',
      cancelButtonText: 'Cancelar',
    });
    if (newTitle && newTitle !== chatDetails.value.title) {
      try {
        await updateChatTitle(route.params.id, newTitle);
        chatDetails.value.title = newTitle;
        Swal.fire('¡Éxito!', 'El nombre del chat ha sido actualizado.', 'success');
        asideComponent.value?.fetchChatHistory();
      } catch (err) {
        console.error('Error al renombrar el chat:', err);
        Swal.fire('Error', 'No se pudo cambiar el nombre del chat.', 'error');
      }
    }
  };

  /**
   * @description Maneja la eliminación del chat actual.
   */
  const handleDeleteCurrentChat = async () => {
    const result = await Swal.fire({
      title: '¿Estás seguro de que quieres borrar este chat?',
      text: "Esta acción no se puede deshacer.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, ¡bórralo!',
      cancelButtonText: 'Cancelar',
      confirmButtonColor: '#d33',
    });

    if (result.isConfirmed) {
      try {
        await deleteChat(route.params.id);
        await Swal.fire('¡Borrado!', 'El chat ha sido eliminado.', 'success');
        chatDetails.value = null;
        chatMessages.value = [];
        error.value = 'El chat ha sido eliminado. Selecciona otro chat o vuelve a la página principal.';
        asideComponent.value?.fetchChatHistory();
      } catch (err) {
        console.error('Error al borrar el chat:', err);
        Swal.fire('Error', 'No se pudo borrar el chat.', 'error');
      }
    }
  };

  /**
   * @description Maneja la generación y descarga del informe en PDF.
   */
  const handleGenerateDocument = async () => {
    Swal.fire({
      title: 'Generando documento...',
      text: 'Por favor, espera un momento.',
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });

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
      Swal.close();
      Swal.fire('¡Éxito!', 'El documento se ha descargado.', 'success');
    } catch (err) {
      console.error('Error al generar el documento:', err);
      Swal.fire('Error', 'No se pudo generar el documento.', 'error');
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
