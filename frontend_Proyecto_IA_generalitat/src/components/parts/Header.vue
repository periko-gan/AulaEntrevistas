<script setup>
/**
 * @file Header.vue
 * @description Componente que muestra la cabecera de la aplicación.
 * La lógica de este componente está gestionada por el composable `useHeader`.
 */
import { useHeader } from '../../composables/useHeader';

/**
 * @property {boolean} isLoggedIn - Indica si el usuario está autenticado.
 * @property {string} userName - El nombre del usuario a mostrar.
 */
const props = defineProps({
  isLoggedIn: {
    type: Boolean,
    default: false
  },
  userName: {
    type: String,
    default: ''
  }
});

/**
 * @event logout - Evento que se emite para solicitar al componente padre que cierre la sesión.
 */
const emit = defineEmits(['logout']);

const { handleLogout } = useHeader(emit);
</script>

<template>
  <header class="bg-white shadow-sm px-5">
    <div class="container-fluid d-flex justify-content-between align-items-center py-3">
      <!-- Izquierda: Logo y Título -->
      <div class="d-flex align-items-center">
        <h1 class="h4 mb-0 text-primary fw-bold">AulaEntrevistas</h1>
      </div>

      <!-- Derecha: Contenido de usuario -->
      <div v-if="props.isLoggedIn" class="d-flex align-items-center gap-3">
        <span class="text-secondary small d-none d-md-block">{{ props.userName }}</span>
        <button @click="handleLogout" class="btn btn-outline-secondary btn-sm">
          Cerrar Sesión
        </button>
      </div>

      <!-- Contenido para usuarios no autenticados -->
      <div v-else class="d-flex align-items-center gap-2">
        <router-link :to="{ name: 'Login' }" class="btn btn-outline-primary btn-sm">
          Iniciar Sesión
        </router-link>
        <router-link :to="{ name: 'Register' }" class="btn btn-primary btn-sm">
          Registrarse
        </router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  border-bottom: 1px solid #e9ecef;
}
</style>
