<script setup>
// App.vue es el punto de entrada principal y solo se encarga de mostrar la ruta actual.
// Cada página (Login, Chat, etc.) es responsable de su propia maquetación.
</script>

<template>
  <router-view />
</template>

<style>
/* Estilos globales para asegurar que la app ocupe toda la altura */
html, body, #app {
  height: 100%;
}
</style>
