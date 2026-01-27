<script setup>
/**
 * @file RegisterView.vue
 * @description Vista para el registro de nuevos usuarios.
 * La lógica de este componente está gestionada por el composable `useRegisterView`.
 */
import {useRegisterView} from '../composables/useRegisterView';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';

const {
  name,
  email,
  password,
  errorMessage,
  isLoading,
  handleRegister
} = useRegisterView();
</script>

<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header :isLoggedIn="false"/>
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="card shadow-lg border-0">
        <div class="card-header bg-primary text-white text-center py-4">
          <h3 class="mb-0 fw-bold">Crear una Cuenta</h3>
        </div>
        <div class="card-body p-4">
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="name" class="form-label text-secondary fw-semibold">Nombre
                Completo</label>
              <input type="text" class="form-control" id="name" v-model="name"
                     placeholder="Nombre y Apellidos" required/>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label text-secondary fw-semibold">Correo
                Electrónico</label>
              <input type="email" class="form-control" id="email" v-model="email"
                     placeholder="usuario@gva.es" required/>
            </div>
            <div class="mb-4">
              <label for="password" class="form-label text-secondary fw-semibold">Contraseña</label>
              <input type="password" class="form-control" id="password" v-model="password"
                     placeholder="••••••••" required/>
            </div>
            <div v-if="errorMessage" class="alert alert-danger py-2 small" role="alert">
              {{ errorMessage }}
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg fw-bold" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"
                      aria-hidden="true"></span>
                {{ isLoading ? 'Registrando...' : 'Crear Cuenta' }}
              </button>
            </div>
            <div class="text-center mt-3">
              <small class="text-muted">
                ¿Ya tienes una cuenta?
                <router-link :to="{ name: 'Login' }">Inicia sesión aquí</router-link>
              </small>
            </div>
          </form>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<style scoped>
.card {
  //border-radius: 10px;
  max-width: 400px;
  width: 100%
}
</style>
