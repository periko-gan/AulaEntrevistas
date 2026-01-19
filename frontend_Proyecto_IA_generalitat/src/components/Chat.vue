<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, removeSession } from '../services/authService';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';
import ChatInterface from './parts/ChatInterface.vue';
import Swal from 'sweetalert2';

const router = useRouter();
const userData = ref(null);

// --- Estado del Aside ---
const isAsideCollapsed = ref(false); // Cambiado a false por defecto
const toggleAside = () => {
  isAsideCollapsed.value = !isAsideCollapsed.value;
};

// --- Datos del Usuario ---
onMounted(() => {
  userData.value = getUser();
});

// Nombre para el Header (solo el primer nombre)
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
</script>

<template>
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userName="userName" @logout="handleLogout" />

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div
          class="d-none d-md-block p-0 h-100"
          :class="isAsideCollapsed ? 'col-auto' : 'col-md-3'"
        >
          <Aside :is-collapsed="isAsideCollapsed" @toggle-aside="toggleAside" />
        </div>
        <div
          class="d-flex flex-column h-100 p-0"
          :class="isAsideCollapsed ? 'col' : 'col-md-9'"
        >
          <ChatInterface :user-data="userData" />
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
/* No se necesitan estilos aquí, ya que están en los componentes hijos */
</style>
