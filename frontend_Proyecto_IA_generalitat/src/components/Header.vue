<script setup>
defineProps({
  userEmail: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['logout']);

const handleLogout = () => {
  emit('logout');
};
</script>

<template>
  <header class="bg-white shadow-sm mb-4">
    <div class="container d-flex justify-content-between align-items-center py-3">
      <div class="d-flex align-items-center">
        <!-- <img alt="Vue logo" class="logo me-3" src="@/assets/logo.svg" width="40" height="40" /> -->
        <h1 class="h4 mb-0 text-primary fw-bold">Proyecto IA Generalitat</h1>
      </div>

      <div class="d-flex align-items-center gap-3">
        <span class="text-secondary small d-none d-md-block">{{ userEmail }}</span>
        <button @click="handleLogout" class="btn btn-outline-secondary btn-sm">
          Cerrar Sesión
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  border-bottom: 1px solid #e9ecef;
}
</style>
