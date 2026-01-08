<script setup>
import { ref } from 'vue';
import BedrockTest from './components/BedrockTest.vue';
import LoginView from './components/LoginView.vue';

// Estado para controlar si el usuario está logueado
const isLoggedIn = ref(false);
const userEmail = ref('');

const onLoginSuccess = (userData) => {
  isLoggedIn.value = true;
  userEmail.value = userData.email;
};

const logout = () => {
  isLoggedIn.value = false;
  userEmail.value = '';
};
</script>

<template>
  <!-- Si NO está logueado, mostramos el Login -->
  <LoginView v-if="!isLoggedIn" @login-success="onLoginSuccess" />

  <!-- Si ESTÁ logueado, mostramos la aplicación principal -->
  <div v-else>
    <header class="bg-white shadow-sm mb-4">
      <div class="container d-flex justify-content-between align-items-center py-3">
        <div class="d-flex align-items-center">
          <img alt="Vue logo" class="logo me-3" src="./assets/logo.svg" width="40" height="40" />
          <h1 class="h4 mb-0 text-primary fw-bold">Proyecto IA Generalitat</h1>
        </div>

        <div class="d-flex align-items-center gap-3">
          <span class="text-secondary small d-none d-md-block">{{ userEmail }}</span>
          <button @click="logout" class="btn btn-outline-secondary btn-sm">
            Cerrar Sesión
          </button>
        </div>
      </div>
    </header>

    <main class="container">
      <BedrockTest />
    </main>
  </div>
</template>

<style scoped>
/* Estilos específicos para el layout principal */
header {
  border-bottom: 1px solid #e9ecef;
}
</style>
