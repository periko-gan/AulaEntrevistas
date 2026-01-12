<script setup>
import { ref } from 'vue';
import BedrockTest from './components/BedrockTest.vue';
import LoginView from './components/LoginView.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import HistoryAside from './components/HistoryAside.vue';

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
  <div class="app-container d-flex flex-column min-vh-100">
    <!-- Si NO está logueado, mostramos el Login -->
    <LoginView v-if="!isLoggedIn" @login-success="onLoginSuccess" />

    <!-- Si ESTÁ logueado, mostramos la aplicación principal -->
    <div v-else class="d-flex flex-column flex-grow-1">
      <Header :userEmail="userEmail" @logout="logout" />

      <div class="container-fluid flex-grow-1">
        <div class="row h-100">
          <!-- Columna del Historial (Aside) -->
          <div class="col-md-3 col-lg-2 d-none d-md-block p-0">
            <HistoryAside />
          </div>

          <!-- Columna del Contenido Principal -->
          <main class="col-md-9 col-lg-10">
            <BedrockTest />
          </main>
        </div>
      </div>

      <Footer />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
