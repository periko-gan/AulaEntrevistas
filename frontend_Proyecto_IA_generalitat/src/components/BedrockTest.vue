<script setup>
import { ref, watch, nextTick } from 'vue';
import { invokeBedrock } from '../services/bedrock';

// --- Estado del Componente ---
const prompt = ref('');
const conversation = ref([]); // Array para guardar el historial de la conversación actual
const loading = ref(false);
const error = ref('');
const chatWindow = ref(null); // Referencia al contenedor del chat para el auto-scroll

// --- Lógica de la Conversación ---
const askBedrock = async () => {
  if (!prompt.value || loading.value) return;

  const userMessage = prompt.value;
  // 1. Añadir el mensaje del usuario a la conversación
  conversation.value.push({
    id: Date.now(),
    text: userMessage,
    sender: 'user',
  });

  // 2. Limpiar el input
  prompt.value = '';
  loading.value = true;
  error.value = '';

  try {
    // 3. Llamar a la IA
    const result = await invokeBedrock(userMessage);
    // 4. Añadir la respuesta de la IA a la conversación
    conversation.value.push({
      id: Date.now() + 1,
      text: result,
      sender: 'ai',
    });
  } catch (err) {
    error.value = "Error al conectar con Bedrock. Revisa la consola y tus credenciales.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// --- Manejadores de Eventos ---
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    askBedrock();
  }
};

// --- Auto-scroll ---
watch(conversation, () => {
  nextTick(() => {
    if (chatWindow.value) {
      chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
    }
  });
}, { deep: true });

</script>

<template>
  <div class="d-flex flex-column h-100">
    <!-- Ventana del Chat -->
    <div class="chat-window flex-grow-1 p-3" ref="chatWindow">
      <div v-for="message in conversation" :key="message.id" class="message-row d-flex align-items-end mb-3" :class="message.sender === 'user' ? 'justify-content-end' : 'justify-content-start'">

        <!-- Avatar de la IA (a la izquierda) -->
        <div v-if="message.sender === 'ai'" class="avatar me-2">
          <i class="bi bi-robot fs-4 text-secondary"></i>
        </div>

        <!-- Burbuja del Mensaje -->
        <div class="message-bubble" :class="message.sender === 'user' ? 'user-bubble' : 'ai-bubble'">
          <p class="mb-0" style="white-space: pre-wrap;">{{ message.text }}</p>
        </div>

        <!-- Avatar del Usuario (a la derecha) -->
        <div v-if="message.sender === 'user'" class="avatar ms-2">
          <i class="bi bi-person-fill fs-4 text-primary"></i>
        </div>

      </div>
      <!-- Indicador de "Escribiendo..." -->
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

    <!-- Área de Input -->
    <div class="input-area p-3 bg-light border-top">
      <div v-if="error" class="alert alert-danger small py-2">{{ error }}</div>
      <div class="input-group">
        <textarea
          id="promptInput"
          v-model="prompt"
          class="form-control"
          rows="1"
          placeholder="Escribe tu mensaje..."
          @keydown="handleKeydown"
          style="resize: none;"
        ></textarea>
        <button
          @click="askBedrock"
          class="btn btn-primary"
          :disabled="loading || !prompt"
        >
          <i class="bi bi-send-fill"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  overflow-y: auto;
  height: calc(100vh - 250px); /* Altura ajustable, puedes cambiarla */
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 85%; /* Ajustado para dejar espacio al avatar */
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
  border: 1px solid #dee2e6;
  border-bottom-left-radius: 5px;
}

.input-area {
  background-color: #f0f0f0;
}
</style>
