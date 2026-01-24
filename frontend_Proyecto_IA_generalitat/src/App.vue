<script setup>
/**
 * @file App.vue
 * @description Componente raíz de la aplicación. Actúa como el punto de entrada principal
 * y se encarga de renderizar el componente de la ruta actual a través de `router-view`.
 */
</script>

<template>
  <div class="container-fluid">
    <router-view />
  </div>
</template>

<style>
/* Estilos globales para asegurar que la app ocupe toda la altura */
html, body, #app {
  height: 100%;
  padding: 0;
  margin: 0;
}
</style>
