<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, removeSession } from '../services/authService';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';
import ChatInterface from './parts/ChatInterface.vue'; // Importamos el nuevo componente
import Swal from 'sweetalert2';

const router = useRouter();
const userData = ref(null);

// --- Datos del Usuario ---
onMounted(() => {
  userData.value = getUser();
});

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
    customClass: {
      confirmButton: 'btn btn-primary',
      cancelButton: 'btn btn-secondary ms-2'
    },
    buttonsStyling: false
  });

  if (result.isConfirmed) {
    removeSession();
    router.push({ name: 'Home' });
  }
};
</script>

<template>
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userName="userName" @logout="handleLogout" />

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div class="col-md-3 col-lg-2 d-none d-md-block p-0 h-100">
          <Aside />
        </div>
        <div class="col-md-9 col-lg-10 d-flex flex-column h-100 p-0">
          <!-- Aquí usamos el nuevo componente -->
          <ChatInterface />
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
/* No se necesitan estilos aquí, ya que están en los componentes hijos */
</style>
