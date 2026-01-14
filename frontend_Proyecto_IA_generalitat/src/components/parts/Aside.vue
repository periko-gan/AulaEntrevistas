<script setup>
import { ref, onMounted } from 'vue';
import { getChatHistory, deleteChat } from '../../services/chatService';
import Swal from 'sweetalert2';

const chatHistory = ref([]);
const isLoading = ref(false);
const error = ref('');

// --- Carga del Historial ---
const fetchChatHistory = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const response = await getChatHistory();
    const sortedChats = response.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    chatHistory.value = sortedChats;
  } catch (err) {
    console.error('Error al cargar el historial:', err);
    error.value = 'No se pudo cargar el historial.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchChatHistory);

// --- Acciones del Chat ---
const handleDeleteChat = async (chatId) => {
  const result = await Swal.fire({
    title: '¿Estás seguro?',
    text: "No podrás revertir esta acción.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, ¡bórralo!',
    cancelButtonText: 'Cancelar',
    customClass: {
      confirmButton: 'btn btn-danger',
      cancelButton: 'btn btn-secondary ms-2'
    },
    buttonsStyling: false
  });

  if (result.isConfirmed) {
    try {
      await deleteChat(chatId);
      chatHistory.value = chatHistory.value.filter(chat => chat.id_chat !== chatId);
      Swal.fire('¡Borrado!', 'El chat ha sido eliminado.', 'success');
    } catch (err) {
      console.error('Error al borrar el chat:', err);
      Swal.fire('Error', 'No se pudo borrar el chat.', 'error');
    }
  }
};
</script>

<template>
  <aside class="d-flex flex-column p-3 bg-light h-100">
    <h5 class="text-secondary fw-bold mb-3">
      <i class="bi bi-clock-history me-2"></i>
      Historial
    </h5>

    <div v-if="isLoading" class="text-center">
      <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <div v-if="error" class="alert alert-warning small py-2">{{ error }}</div>

    <div v-if="!isLoading && chatHistory.length === 0 && !error" class="text-center text-muted small">
      No hay chats anteriores.
    </div>

    <div class="list-group list-group-flush flex-grow-1 overflow-auto">
      <div
        v-for="chat in chatHistory"
        :key="chat.id_chat"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span class="chat-title text-truncate">
          <small class="text-muted me-2">#{{ chat.id_chat }} (User: {{ chat.id_usuario }})</small>
          {{ chat.title }}
        </span>
        <div class="chat-actions">
          <router-link :to="{ name: 'Conversation', params: { id: chat.id_chat } }" class="btn btn-sm btn-icon" title="Ver conversación">
            <i class="bi bi-pencil-square"></i>
          </router-link>
          <button @click="handleDeleteChat(chat.id_chat)" class="btn btn-sm btn-icon" title="Borrar chat">
            <i class="bi bi-trash3"></i>
          </button>
        </div>
      </div>
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
  padding: 0.5rem 0.75rem;
}
.list-group-item:hover {
  background-color: #e9ecef;
}
.chat-title {
  flex-grow: 1;
  margin-right: 10px;
}
.chat-actions {
  display: none;
  flex-shrink: 0;
}
.list-group-item:hover .chat-actions {
  display: block;
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
</style>
