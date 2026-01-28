/**
 * @file useHomeView.js
 * @description Composable para gestionar la lógica de la página de inicio (HomeView).
 */
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, removeSession } from '../services/authService';
import { showLogoutConfirmation } from '../services/alertService';

/**
 * @description Composable para gestionar la lógica de la página de inicio.
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useHomeView() {
  /** @type {boolean} */
  const isLoggedIn = ref(false);
  /** @type {string} */
  const userName = ref('');
  const router = useRouter();

  /**
   * @description Hook del ciclo de vida que comprueba si el usuario está logueado al montar el componente.
   */
  onMounted(() => {
    const user = getUser();
    if (user) {
      isLoggedIn.value = true;
      userName.value = user.nombre.split(' ')[0];
    }
  });

  /**
   * @description Maneja el proceso de cierre de sesión, mostrando una confirmación y recargando la página.
   */
  const handleLogout = async () => {
    const result = await showLogoutConfirmation();
    if (result.isConfirmed) {
      removeSession();
      isLoggedIn.value = false;
      userName.value = '';
      // Forzar recarga para asegurar que el estado se limpie completamente
      router.push({ name: 'Home' }).then(() => {
        window.location.reload();
      });
    }
  };

  return {
    isLoggedIn,
    userName,
    handleLogout,
  };
}
