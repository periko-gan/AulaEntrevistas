import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login, saveToken, getMe, saveUser } from '../services/authService';
import { getChatHistory } from '../services/chatService';
import { showWelcomeAlert } from '../services/alertService';
import { isValidPassword } from '../utils/validators'; // Importar la función de validación

/**
 * @description Composable para gestionar la lógica de la vista de inicio de sesión.
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useLoginView() {
  /** @type {string} */
  const email = ref('');
  /** @type {string} */
  const password = ref('');
  /** @type {string} */
  const errorMessage = ref('');
  /** @type {boolean} */
  const isLoading = ref(false);
  const router = useRouter();

  /**
   * @description Maneja el envío del formulario de inicio de sesión.
   */
  const handleLogin = async () => {
    errorMessage.value = '';
    if (!email.value || !password.value) {
      errorMessage.value = 'Por favor, introduce tu correo y contraseña.';
      return;
    }

    // Validar la contraseña
    if (!isValidPassword(password.value)) {
      errorMessage.value = 'La contraseña debe tener al menos 8 caracteres, una letra y un número.';
      return;
    }

    isLoading.value = true;

    try {
      const loginResponse = await login({
        email: email.value,
        password: password.value,
      });

      saveToken(loginResponse.data.access_token);

      const meResponse = await getMe();
      const user = meResponse.data;
      saveUser(user);

      await showWelcomeAlert(user.nombre);

      // Lógica para redirigir al chat más antiguo o iniciar uno nuevo
      const chatHistoryResponse = await getChatHistory();
      let chatHistory = chatHistoryResponse.data;

      if (chatHistory && chatHistory.length > 0) {
        // Ordenar los chats por la fecha de creación (ascendente para obtener el más antiguo primero)
        chatHistory.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
        const oldestChat = chatHistory[0];
        // setTimeout(() => {
          router.push({ name: 'Conversation', params: { id: oldestChat.id_chat } });
        // }, 1500);
      } else {
        // Si no hay historial, redirigir a la página de chat para iniciar uno nuevo
        // setTimeout(() => {
          router.push({ name: 'Chat' });
        // }, 1500);
      }

    } catch (error) {
      if (error.response) {
        if (error.response.status === 422) {
          errorMessage.value = error.response.data.detail[0].msg || 'Los datos introducidos no son válidos.';
        } else {
          errorMessage.value = error.response.data.detail || 'Credenciales incorrectas o error en el servidor.';
        }
      } else {
        errorMessage.value = 'No se pudo conectar con el servidor.';
      }
      console.error('Error en el login:', error);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    email,
    password,
    errorMessage,
    isLoading,
    handleLogin
  };
}
