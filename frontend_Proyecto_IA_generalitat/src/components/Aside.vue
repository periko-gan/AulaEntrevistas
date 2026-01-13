<script setup>
// En un futuro, este array vendrá de una prop o un servicio de estado
const conversationHistory = [
  { id: 1, title: 'Fiestas populares en Valencia' },
  { id: 2, title: 'Ciclos formativos de informática' },
  { id: 3, title: 'Mejores playas de Castellón' },
  { id: 4, title: 'Rutas de senderismo en Alicante' },
];
</script>

<template>
  <aside class="d-flex flex-column p-3 bg-light h-100">
    <h5 class="text-secondary fw-bold mb-3">
      <i class="bi bi-clock-history me-2"></i>
      Historial
    </h5>

    <div class="list-group list-group-flush">
      <a
        href="#"
        v-for="item in conversationHistory"
        :key="item.id"
        class="list-group-item list-group-item-action py-2"
        aria-current="true"
      >
        {{ item.title }}
      </a>
    </div>
  </aside>
</template>

<style scoped>
aside {
  border-right: 1px solid #dee2e6;
}
.list-group-item {
  border: none;
  background-color: transparent;
  font-size: 0.9rem;
}
.list-group-item:hover {
  background-color: #e9ecef;
}
</style>
