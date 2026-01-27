<script setup>
/**
 * @file Footer.vue
 * @description Componente que muestra el pie de página de la aplicación.
 * La lógica de este componente está gestionada por el composable `useFooter`.
 */
import { useFooter } from '../../composables/useFooter';

const { currentYear } = useFooter();
</script>

<template>
  <footer class="text-center bg-white py-3 border-top mt-auto w-100">
    <div class="container">
      <small class="text-muted"><span class="rotate-180">CC BY-NC</span> {{ currentYear }} Generalitat Valenciana</small>
    </div>
  </footer>
</template>

<style scoped>
footer {
  /* Asegura que el footer tenga un estilo consistente */
  background-color: #fff;
}

</style>
