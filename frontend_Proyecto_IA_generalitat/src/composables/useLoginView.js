import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login, saveToken, getMe, saveUser } from '../services/authService';
import Swal from 'sweetalert2';

export function useLoginView() {
  const email = ref('');
  const password = ref('');
  const errorMessage = ref('');
  const isLoading = ref(false);
  const router = useRouter();

  const handleLogin = async () => {
    errorMessage.value = '';
    if (!email.value || !password.value) {
      errorMessage.value = 'Por favor, introduce tu correo y contraseña.';
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

      Swal.fire({
        position: 'center',
        icon: 'success',
        title: `¡Bienvenido, ${user.nombre}!`,
        showConfirmButton: false,
        timer: 1500
      });

      setTimeout(() => {
        router.push({ name: 'Chat' });
      }, 1500);

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
