<script setup>
import { defineExpose } from 'vue';
import { useAside } from '../../composables/useAside';

const props = defineProps({
  activeChatId: {
    type: [String, Number],
    default: null
  },
  isCollapsed: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['toggle-aside']);

const {
  chatHistory,
  isLoading,
  error,
  fetchChatHistory,
  handleNewChat
} = useAside();

// Exponemos la función para que el padre pueda llamarla
defineExpose({
  fetchChatHistory
});
</script>

<template>
  <aside class="d-flex flex-column p-3 bg-light h-100" :class="{ 'collapsed': isCollapsed }">

    <!-- Contenedor del botón de hamburguesa -->
    <div class="d-flex mb-3" :class="{ 'justify-content-end': !isCollapsed, 'justify-content-center': isCollapsed }">
      <button class="btn btn-icon" @click="$emit('toggle-aside')" title="Ocultar/Mostrar historial">
        <i class="bi bi-list fs-4"></i>
      </button>
    </div>

    <!-- Enlace Nuevo Chat -->
    <div class="mb-3">
      <router-link
        :to="{ name: 'Chat' }"
        @click="handleNewChat"
        class="new-chat-link d-flex align-items-center justify-content-center py-2 px-3 rounded"
      >
        <i v-if="isCollapsed" class="bi bi-plus-lg"></i> <!-- Icono solo visible cuando está colapsado -->
        <h5 v-if="!isCollapsed" class="mb-0 fw-bold">Nuevo Chat</h5>
      </router-link>
    </div>

    <!-- Cabecera del panel lateral -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 v-if="!isCollapsed" class="text-secondary fw-bold mb-0">
        <i class="bi bi-clock-history me-2"></i>
        Historial
      </h5>
    </div>

    <!-- Estado de Carga: se muestra un spinner mientras isLoading es true. -->
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Estado de Error: se muestra una alerta si la variable 'error' tiene contenido. -->
    <div v-if="error" class="alert alert-warning small py-2">{{ error }}</div>

    <!-- Estado Vacío: se muestra un mensaje si no está cargando, no hay errores y el historial está vacío. -->
    <div v-if="!isLoading && chatHistory.length === 0 && !error" class="text-center text-muted small">
      <!-- El mensaje cambia dependiendo de si el panel está colapsado o no. -->
      <span v-if="!isCollapsed">No hay chats anteriores.</span>
      <i v-else class="bi bi-archive"></i>
    </div>

    <!-- Lista del Historial: se renderiza un enlace por cada chat en el array 'chatHistory'. -->
    <div class="list-group list-group-flush flex-grow-1 overflow-auto">
      <router-link
        v-for="chat in chatHistory"
        :key="chat.id_chat"
        :to="{ name: 'Conversation', params: { id: chat.id_chat } }"
        class="list-group-item list-group-item-action"
        :class="{ 'active': chat.id_chat == activeChatId }"
      >
        <!-- Si el panel no está colapsado, muestra el título del chat. -->
        <span v-if="!isCollapsed" class="chat-title text-truncate">
          {{ chat.title }}
        </span>
        <!-- Si está colapsado, muestra un icono genérico de chat. -->
        <i v-else class="bi bi-chat-left-text"></i>
      </router-link>
    </div>
  </aside>
</template>

<style scoped>
aside {
  border-right: 1px solid #dee2e6;
  transition: width 0.3s ease; /* Animación suave para el cambio de ancho. */
}
aside.collapsed {
  min-width: 60px; /* Ancho mínimo para mostrar iconos */
  align-items: center; /* Centra los iconos. */
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
}
aside.collapsed .list-group-item {
  text-align: center; /* Centra el contenido de cada elemento de la lista. */
  padding: 0.5rem 0.25rem; /* Ajusta el padding para iconos */
}
aside.collapsed .list-group-item .chat-title {
  display: none; /* Oculta el título cuando está colapsado */
}

.list-group-item {
  border: none;
  background-color: transparent;
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
  border-radius: 5px;
  color: var(--bs-dark);
  text-decoration: none;
}
.list-group-item:hover {
  background-color: #e9ecef;
}
/* Estilos para el elemento del historial que está activo (el que se está viendo). */
.list-group-item.active {
  background-color: var(--bs-primary);
  color: white;
  border-color: var(--bs-primary);
}
.chat-title {
  flex-grow: 1;
  margin-right: 10px;
}
.btn-icon {
  padding: 0.1rem 0.4rem;
  color: var(--bs-secondary);
  background: none;
  border: none;
}
.btn-icon:hover {
  color: var(--bs-primary);
}

/* Estilos para el enlace "Nuevo Chat" */
.new-chat-link {
  color: var(--bs-primary);
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 5px;
  transition: background-color 0.2s ease-in-out;
}
.new-chat-link:hover {
  background-color: rgba(var(--bs-primary-rgb), 0.1);
}
aside.collapsed .new-chat-link {
  padding: 0.5rem 0.25rem;
}
aside.collapsed .new-chat-link h5 {
  display: none;
}
aside.collapsed .new-chat-link i {
  margin-right: 0 !important;
}
</style>
