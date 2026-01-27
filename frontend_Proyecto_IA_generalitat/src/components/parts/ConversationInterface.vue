<script setup>
/**
 * @file ConversationInterface.vue
 * @description Componente que renderiza el contenido principal de la vista de una conversación (historial, mensajes y acciones).
 */
import { useConversationInterface } from '../../composables/useConversationInterface';

/**
 * @property {boolean} isLoading - Indica si se están cargando los datos.
 * @property {string} error - Mensaje de error, si lo hay.
 * @property {object} chatDetails - Detalles del chat actual.
 * @property {Array<object>} chatMessages - Array de mensajes de la conversación.
 * @property {object} route - Objeto de la ruta actual para acceder a los parámetros.
 * @property {string} currentUserName - El nombre del usuario actual.
 */
defineProps({
  isLoading: Boolean,
  error: String,
  chatDetails: Object,
  chatMessages: Array,
  route: Object,
  currentUserName: String,
});

/**
 * @event rename-chat - Se emite cuando se hace clic en el botón de renombrar.
 * @event generate-document - Se emite cuando se hace clic en el botón de generar documento.
 * @event delete-chat - Se emite cuando se hace clic en el botón de borrar.
 * @event go-back - Se emite cuando se hace clic en el botón de reanudar chat.
 */
const emit = defineEmits([
  'rename-chat',
  'generate-document',
  'delete-chat',
  'go-back',
]);

const { renameButtonRef, downloadButtonRef, deleteButtonRef } = useConversationInterface();
</script>

<template>
  <div v-if="isLoading" class="text-center mt-5">
    <div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div>
  </div>
  <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
  <div v-else-if="chatDetails">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="d-flex align-items-center">
        <h2 class="fw-bold mb-0">{{ chatDetails.title }}</h2>
        <button
          @click="$emit('rename-chat')"
          class="btn btn-sm btn-icon ms-2"
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Renombrar chat"
          ref="renameButtonRef"
        >
          <i class="bi bi-pencil-square fs-5"></i>
        </button>
        <button
          v-if="chatDetails.status === 'completed'"
          @click="$emit('generate-document')"
          class="btn btn-sm btn-icon"
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Generar documento"
          ref="downloadButtonRef"
        >
          <i class="bi bi-file-earmark-arrow-down fs-5"></i>
        </button>
        <button
          @click="$emit('delete-chat')"
          class="btn btn-sm btn-icon delete-btn"
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Borrar chat"
          ref="deleteButtonRef"
        >
          <i class="bi bi-trash3 fs-5"></i>
        </button>
      </div>
      <button v-if="chatDetails.status !== 'completed'" @click="$emit('go-back')" class="btn btn-outline-secondary">
        Reanudar chat
      </button>
    </div>
    <p class="text-muted mb-4">
      Iniciado por: <span class="fw-semibold">{{ currentUserName }}</span>
    </p>
    <div class="chat-history">
      <div v-for="message in chatMessages" :key="message.id_mensaje" class="message-row d-flex align-items-end mb-3" :class="message.emisor === 'USER' ? 'justify-content-end' : 'justify-content-start'">
        <div v-if="message.emisor === 'IA'" class="avatar me-2">
          <i class="bi bi-robot fs-4 text-secondary"></i>
        </div>
        <div class="message-bubble" :class="message.emisor === 'USER' ? 'user-bubble' : 'ai-bubble'">
          <p class="mb-0" style="white-space: pre-wrap;">
            <span v-for="(part, index) in message.parts" :key="index" :class="part.style">
              {{ part.text }}
            </span>
          </p>
        </div>
        <div v-if="message.emisor === 'USER'" class="avatar ms-2">
          <i class="bi bi-person-circle fs-4 text-primary"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-history {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
}
.message-bubble {
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 80%;
  word-wrap: break-word;
}
.user-bubble {
  background-color: var(--bs-primary);
  color: var(--bs-white);
  border-bottom-right-radius: 5px;
}
.ai-bubble {
  background-color: var(--bs-light);
  color: var(--bs-dark);
  border: 1px solid #e9ecef;
  border-bottom-left-radius: 5px;
}
.btn-icon {
  color: var(--bs-secondary);
}
.btn-icon:hover {
  color: var(--bs-primary);
}
.delete-btn:hover {
  color: var(--bs-danger);
}
</style>
