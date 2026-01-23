import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { register, saveToken, getMe, saveUser } from '../services/authService';
import Swal from 'sweetalert2';

export function useRegisterView() {
  const name = ref('');
  const email = ref('');
  const password = ref('');
  const errorMessage = ref('');
  const isLoading = ref(false);
  const router = useRouter();

  const handleRegister = async () => {
    errorMessage.value = '';
    if (!name.value || !email.value || !password.value) {
      errorMessage.value = 'Por favor, completa todos los campos.';
      return;
    }

    isLoading.value = true;

    try {
      const registerResponse = await register({
        nombre: name.value,
        email: email.value,
        password: password.value,
      });

      saveToken(registerResponse.data.access_token);

      const meResponse = await getMe();
      const user = meResponse.data;
      saveUser(user);

      Swal.fire({
        position: 'center',
        icon: 'success',
        title: '¡Registro completado!',
        text: `Bienvenido, ${user.nombre}.`,
        showConfirmButton: false,
        timer: 2000
      });

      setTimeout(() => {
        router.push({ name: 'Chat' });
      }, 2000);

    } catch (error) {
      if (error.response) {
        if (error.response.status === 422) {
          errorMessage.value = error.response.data.detail[0].msg || 'Los datos introducidos no son válidos.';
        } else {
          errorMessage.value = error.response.data.detail || 'Ha ocurrido un error durante el registro.';
        }
      } else {
        errorMessage.value = 'No se pudo conectar con el servidor.';
      }
      console.error('Error en el registro:', error);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    name,
    email,
    password,
    errorMessage,
    isLoading,
    handleRegister
  };
}
