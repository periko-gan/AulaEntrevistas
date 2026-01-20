<script setup>
import { ref, watch, nextTick, onMounted } from 'vue';
import {
  createChat,
  initializeChat,
  getAiReply,
  updateChatTitle,
  generateDocument,
  deleteChat,
  getChatDetails
} from '../../services/chatService';
import Swal from 'sweetalert2';
import { Tooltip } from 'bootstrap';

// --- Estado del Componente ---
const prompt = ref('');
const conversation = ref([]);
const loading = ref(false);
const error = ref('');
const chatWindow = ref(null);
const chatId = ref(null);
const chatStatus = ref(null);
const chatTitle = ref('Nuevo Chat');
const isTextareaFocused = ref(false);

// --- Lógica de Tooltip ---
const initializeTooltips = () => {
  nextTick(() => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      const oldTooltip = Tooltip.getInstance(tooltipTriggerEl);
      if (oldTooltip) oldTooltip.dispose();
      return new Tooltip(tooltipTriggerEl);
    });
  });
};

// --- Lógica de Inicialización del Chat ---
const startNewChat = async () => {
  loading.value = true;
  error.value = '';
  conversation.value = [];
  chatId.value = null;
  chatStatus.value = null;
  chatTitle.value = 'Nuevo Chat';

  try {
    // Paso 1: Crear el chat para obtener el ID
    const createResponse = await createChat();
    const newChatId = createResponse.data.id_chat;
    chatId.value = newChatId;

    // Paso 2: Inicializar la conversación con la IA usando el nuevo ID
    const initResponse = await initializeChat(newChatId);
    const initialMessage = initResponse.data;

    chatTitle.value = initialMessage.title || 'Nueva Conversación';
    conversation.value.push({
      id: initialMessage.id_mensaje || Date.now(),
      text: initialMessage.contenido,
      sender: 'ai'
    });

    const details = await getChatDetails(newChatId);
    chatStatus.value = details.data.status;

  } catch (err) {
    error.value = 'No se pudo iniciar una nueva conversación con la IA.';
    console.error('Error al inicializar el chat:', err);
  } finally {
    loading.value = false;
    initializeTooltips();
  }
};

onMounted(startNewChat);

// --- Lógica de la Conversación ---
const askApi = async () => {
  if (!prompt.value || loading.value) return;
  const userMessage = prompt.value;
  conversation.value.push({ id: Date.now(), text: userMessage, sender: 'user' });
  prompt.value = '';
  loading.value = true;
  error.value = '';

  try {
    const replyResponse = await getAiReply(chatId.value, userMessage);
    conversation.value.push({ id: Date.now() + 1, text: replyResponse.data.contenido, sender: 'ai' });

    const details = await getChatDetails(chatId.value);
    chatStatus.value = details.data.status;

  } catch (err) {
    error.value = 'Ha ocurrido un error al contactar con la IA.';
    console.error('Error en la llamada al chat:', err);
  } finally {
    loading.value = false;
    initializeTooltips();
  }
};

// --- Manejadores de Eventos ---
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    askApi();
  }
};

const handleRenameChat = async () => {
  if (!chatId.value) return;
  const { value: newTitle } = await Swal.fire({
    title: 'Cambiar nombre del chat',
    input: 'text',
    inputValue: chatTitle.value,
    showCancelButton: true,
    confirmButtonText: 'Guardar',
  });
  if (newTitle && newTitle !== chatTitle.value) {
    await updateChatTitle(chatId.value, newTitle);
    chatTitle.value = newTitle;
    Swal.fire('¡Éxito!', 'Nombre actualizado.', 'success');
  }
};

const handleGenerateDocument = async () => {
  if (!chatId.value) return;
  Swal.fire({ title: 'Generando documento...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
  try {
    const response = await generateDocument(chatId.value);
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${chatTitle.value || 'informe'}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    Swal.close();
  } catch (err) {
    console.error('Error al generar el documento:', err);
    Swal.fire('Error', 'No se pudo generar el documento.', 'error');
  }
};

const handleDeleteChat = async () => {
  if (!chatId.value) return;
  const result = await Swal.fire({
    title: '¿Estás seguro?',
    text: 'Se borrará el chat actual y no se podrá recuperar.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, borrar',
    confirmButtonColor: '#d33',
  });
  if (result.isConfirmed) {
    await deleteChat(chatId.value);
    startNewChat(); // Inicia un nuevo chat
    Swal.fire('¡Borrado!', 'El chat ha sido eliminado.', 'success');
  }
};

// --- Auto-scroll ---
watch(conversation, () => {
  nextTick(() => {
    if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
  });
}, { deep: true });
</script>

<template>
  <main class="d-flex flex-column h-100 p-0">
    <div class="chat-window flex-grow-1 p-3" ref="chatWindow">
      <div v-for="message in conversation" :key="message.id" class="message-row d-flex align-items-end mb-3" :class="message.sender === 'user' ? 'justify-content-end' : 'justify-content-start'">
        <div v-if="message.sender === 'ai'" class="avatar me-2">
          <i class="bi bi-robot fs-4 text-secondary"></i>
        </div>
        <div class="message-bubble" :class="message.sender === 'user' ? 'user-bubble' : 'ai-bubble'">
          <p class="mb-0" style="white-space: pre-wrap;">{{ message.text }}</p>
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

<!--        <button @click="handleRenameChat" class="btn btn-outline-secondary" :disabled="!chatId" data-bs-toggle="tooltip" title="Renombrar Chat">-->
<!--          <i class="bi bi-pencil-square"></i>-->
<!--        </button>-->
<!--        <button v-if="chatStatus === 'completed'" @click="handleGenerateDocument" class="btn btn-outline-secondary" :disabled="!chatId" data-bs-toggle="tooltip" title="Descargar Informe">-->
<!--          <i class="bi bi-file-earmark-arrow-down"></i>-->
<!--        </button>-->
<!--        <button @click="handleDeleteChat" class="btn btn-outline-danger" :disabled="!chatId" data-bs-toggle="tooltip" title="Borrar Chat">-->
<!--          <i class="bi bi-trash3"></i>-->
<!--        </button>-->

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
