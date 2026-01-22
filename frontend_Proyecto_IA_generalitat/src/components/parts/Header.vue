<script setup>
defineProps({
  isLoggedIn: {
    type: Boolean,
    default: false
  },
  userName: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['logout']);

const handleLogout = () => {
  emit('logout');
};
</script>

<template>
  <header class="bg-white shadow-sm px-5">
    <div class="container-fluid d-flex justify-content-between align-items-center py-3">
      <!-- Logo y Título (siempre visible) -->
      <div class="d-flex align-items-center">
        <h1 class="h4 mb-0 text-primary fw-bold">AulaEntrevistas</h1>
      </div>

      <!-- Contenido para usuarios autenticados -->
      <div v-if="isLoggedIn" class="d-flex align-items-center gap-3">
        <span class="text-secondary small d-none d-md-block">{{ userName }}</span>
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
