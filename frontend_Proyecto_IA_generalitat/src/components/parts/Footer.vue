<script setup>
import { computed } from 'vue';

// Año actual dinámico
const currentYear = computed(() => new Date().getFullYear());
</script>

<template>
  <footer class="text-center bg-white py-3 border-top mt-auto w-100">
    <div class="container">
      <small class="text-muted"><span class="rotate-180">©</span> {{ currentYear }} Generalitat Valenciana</small>
    </div>
  </footer>
</template>

<style scoped>
footer {
  /* Asegura que el footer tenga un estilo consistente */
  background-color: #fff;
}

.rotate-180 {
  display: inline-block;
  transform: rotate(180deg);
}
</style>
