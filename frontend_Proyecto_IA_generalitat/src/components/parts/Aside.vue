<script setup>
import { ref, onMounted, defineExpose } from 'vue';
import { getChatHistory } from '../../services/chatService';

const props = defineProps({
  activeChatId: {
    type: [String, Number],
    default: null
  }
});

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

// Exponemos la función para que el padre pueda llamarla
defineExpose({
  fetchChatHistory
});
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
      <router-link
        v-for="chat in chatHistory"
        :key="chat.id_chat"
        :to="{ name: 'Conversation', params: { id: chat.id_chat } }"
        class="list-group-item list-group-item-action"
        :class="{ 'active': chat.id_chat == activeChatId }"
      >
        <span class="chat-title text-truncate">
          {{ chat.title }}
        </span>
      </router-link>
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
  border-radius: 5px;
  color: var(--bs-dark);
  text-decoration: none;
}
.list-group-item:hover {
  background-color: #e9ecef;
}
.list-group-item.active {
  background-color: var(--bs-primary);
  color: white;
  border-color: var(--bs-primary);
}
.chat-title {
  flex-grow: 1;
  margin-right: 10px;
}
</style>
