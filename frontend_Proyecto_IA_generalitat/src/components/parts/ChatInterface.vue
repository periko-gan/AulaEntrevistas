<script setup>
/**
 * @file ChatInterface.vue
 * @description Componente que renderiza la interfaz de chat, incluyendo la ventana de mensajes y el área de entrada.
 * La lógica de este componente está gestionada por el composable `useChatInterface`.
 */
import { defineExpose } from 'vue';
import { useChatInterface } from '../../composables/useChatInterface.js';

/**
 * @property {object|null} userData - Los datos del usuario autenticado, pasados desde el componente padre.
 */
const props = defineProps({
  userData: {
    type: Object,
    default: () => null
  }
});

const {
  prompt,
  conversation,
  loading,
  error,
  chatWindow,
  isTextareaFocused,
  askApi,
  handleKeydown,
  startNewChat
} = useChatInterface(props);

// Exponemos la función startNewChat para que el padre pueda llamarla.
defineExpose({
  startNewChat
});
</script>

<template>
  <main class="d-flex flex-column h-100 p-0">
    <div class="chat-window flex-grow-1 p-3" ref="chatWindow">
      <div v-for="message in conversation" :key="message.id" class="message-row d-flex align-items-end mb-3" :class="message.sender === 'user' ? 'justify-content-end' : 'justify-content-start'">
        <div v-if="message.sender === 'ai'" class="avatar me-2">
          <i class="bi bi-robot fs-4 text-secondary"></i>
        </div>
        <div class="message-bubble" :class="message.sender === 'user' ? 'user-bubble' : 'ai-bubble'">
          <p class="mb-0" style="white-space: pre-wrap;">
            <span v-for="(part, index) in message.parts" :key="index" :class="part.style">
              {{ part.text }}
            </span>
          </p>
        </div>
        <div v-if="message.sender === 'user'" class="avatar ms-2">
          <i class="bi bi-person-circle fs-4 text-primary"></i>
        </div>
      </div>
      <div v-if="loading" class="message-row d-flex align-items-end mb-3 justify-content-start">
        <div class="avatar me-2">
          <i class="bi bi-robot fs-4 text-secondary"></i>
        </div>
        <div class="message-bubble ai-bubble">
          <div class="spinner-grow spinner-grow-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>
    <div class="input-area p-3 bg-light border-top">
      <div v-if="error" class="alert alert-danger small py-2">{{ error }}</div>
      <div class="input-group" :class="{ 'is-focused': isTextareaFocused }">
        <textarea id="promptInput" v-model="prompt" class="form-control" placeholder="Escribe tu mensaje..." @keydown="handleKeydown" @focus="isTextareaFocused = true" @blur="isTextareaFocused = false" style="resize: none;"></textarea>
        <button @click="askApi" class="btn btn-primary" :disabled="loading || !prompt">
          <i class="bi bi-send-fill"></i>
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped>
.chat-window { overflow-y: auto; }
.message-bubble { padding: 10px 15px; border-radius: 20px; max-width: 85%; word-wrap: break-word; }
.user-bubble { background-color: var(--bs-primary); color: var(--bs-white); border-bottom-right-radius: 5px; }
.ai-bubble { background-color: var(--bs-light); color: var(--bs-dark); border: 1px solid #dee2e6; border-bottom-left-radius: 5px; }
.input-area { background-color: #f0f0f0; }
.avatar small { font-size: 0.7rem; }
.input-group.is-focused {
  box-shadow: 0 0 0 0.25rem rgba(var(--bs-primary-rgb), 0.25);
  border-radius: var(--bs-border-radius, 0.375rem);
}
.input-group .form-control:focus { box-shadow: none; }
.input-group .btn:focus { box-shadow: none; }
</style>
