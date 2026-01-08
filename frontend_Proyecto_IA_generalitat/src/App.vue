<script setup>
import { ref } from 'vue';
import BedrockTest from './components/BedrockTest.vue';
import LoginView from './components/LoginView.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

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
    <div v-else class="flex-grow-1 d-flex flex-column">
      <Header :userEmail="userEmail" @logout="logout" />

      <main class="container flex-grow-1">
        <BedrockTest />
      </main>
    </div>

    <!-- Footer global (visible siempre o condicionalmente según prefieras, aquí lo pongo global) -->
    <!-- Si quieres que el footer del Login sea este mismo, LoginView no debería tener su propio footer interno -->
    <Footer v-if="isLoggedIn" />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
