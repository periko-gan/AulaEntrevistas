import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, removeSession } from '../services/authService';
import { chatState } from '../services/chatState';
import Swal from 'sweetalert2';

/**
 * @description Composable para gestionar la lógica de la vista principal del chat (ChatView).
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useChatView() {
  const router = useRouter();
  /** @type {object|null} */
  const userData = ref(null);
  /** @type {object|null} */
  const chatInterfaceRef = ref(null);

  // --- Estado del Aside ---
  /** @type {boolean} */
  const isAsideCollapsed = ref(false);
  /**
   * @description Cambia el estado de colapso del panel lateral.
   */
  const toggleAside = () => {
    isAsideCollapsed.value = !isAsideCollapsed.value;
  };

  /**
   * @description Hook del ciclo de vida que obtiene los datos del usuario al montar el componente.
   */
  onMounted(() => {
    userData.value = getUser();
  });

  /**
   * @description Observador que reacciona al estado global `forceNewChat` para iniciar una nueva conversación.
   */
  watch(() => chatState.forceNewChat, (newValue) => {
    if (newValue) {
      chatInterfaceRef.value?.startNewChat();
      chatState.forceNewChat = false; // Reseteamos el estado
    }
  });

  // --- Propiedades Computadas ---
  /**
   * @description Propiedad computada que devuelve el primer nombre del usuario con la primera letra en mayúscula.
   * @returns {string}
   */
  const userName = computed(() => {
    if (userData.value && userData.value.nombre) {
      const firstName = userData.value.nombre.split(' ')[0];
      return firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();
    }
    return 'Usuario';
  });

  /**
   * @description Maneja el proceso de cierre de sesión, mostrando una confirmación y redirigiendo al inicio.
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
      sessionStorage.removeItem('activeChatId'); // Limpiamos el chat activo de la sesión
      router.push({ name: 'Home' });
    }
  };

  return {
    userData,
    chatInterfaceRef,
    isAsideCollapsed,
    userName,
    toggleAside,
    handleLogout
  };
}
