import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, removeSession } from '../services/authService';
import { chatState } from '../services/chatState';
import Swal from 'sweetalert2';

export function useChatView() {
  const router = useRouter();
  const userData = ref(null);
  const chatInterfaceRef = ref(null);

  // --- Estado del Aside ---
  const isAsideCollapsed = ref(false);
  const toggleAside = () => {
    isAsideCollapsed.value = !isAsideCollapsed.value;
  };

  // --- Datos del Usuario ---
  onMounted(() => {
    userData.value = getUser();
  });

  // --- Observador para forzar un nuevo chat ---
  watch(() => chatState.forceNewChat, (newValue) => {
    if (newValue) {
      chatInterfaceRef.value?.startNewChat();
      chatState.forceNewChat = false; // Reseteamos el estado
    }
  });

  // --- Propiedades Computadas ---
  const userName = computed(() => {
    if (userData.value && userData.value.nombre) {
      const firstName = userData.value.nombre.split(' ')[0];
      return firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();
    }
    return 'Usuario';
  });

  // --- Manejador de Cierre de Sesión ---
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

  return {
    userData,
    chatInterfaceRef,
    isAsideCollapsed,
    userName,
    toggleAside,
    handleLogout
  };
}
