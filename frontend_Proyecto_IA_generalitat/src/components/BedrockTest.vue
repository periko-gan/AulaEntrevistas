<script setup>
import { ref, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
// import { invokeBedrock } from '../services/bedrock'; // Eliminada la dependencia de Bedrock
import Header from './Header.vue';
import Footer from './Footer.vue';
import Aside from './Aside.vue';

// --- Estado del Componente ---
const prompt = ref('');
const conversation = ref([]);
const loading = ref(false);
const error = ref('');
const chatWindow = ref(null);
const router = useRouter();

// Simulación de datos de usuario
const userEmail = ref('usuario@gva.es');

// --- Lógica de la Conversación (Simulada) ---
const askBedrock = async () => {
  if (!prompt.value || loading.value) return;

  const userMessage = prompt.value;
  conversation.value.push({ id: Date.now(), text: userMessage, sender: 'user' });
  prompt.value = '';
  loading.value = true;
  error.value = '';

  // SIMULACIÓN DE RESPUESTA DE LA IA
  setTimeout(() => {
    const aiResponse = `Esta es una respuesta simulada a tu pregunta: "${userMessage}". El servicio de Bedrock está desconectado de este componente.`;
    conversation.value.push({ id: Date.now() + 1, text: aiResponse, sender: 'ai' });
    loading.value = false;
  }, 1500); // Simula un tiempo de espera de 1.5 segundos
};

// --- Manejadores de Eventos ---
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    askBedrock();
  }
};

const handleLogout = () => {
  localStorage.removeItem('user-token');
  router.push({ name: 'Login' });
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
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userEmail="userEmail" @logout="handleLogout" />

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div class="col-md-3 col-lg-2 d-none d-md-block p-0 h-100">
          <Aside />
        </div>
        <main class="col-md-9 col-lg-10 d-flex flex-column h-100 p-0">
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
              <button @click="askBedrock" class="btn btn-primary" :disabled="loading || !prompt">
                <i class="bi bi-send-fill"></i>
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
.chat-window { overflow-y: auto; }
.message-bubble { padding: 10px 15px; border-radius: 20px; max-width: 85%; word-wrap: break-word; }
.user-bubble { background-color: var(--bs-primary); color: var(--bs-white); border-bottom-right-radius: 5px; }
.ai-bubble { background-color: var(--bs-light); color: var(--bs-dark); border: 1px solid #dee2e6; border-bottom-left-radius: 5px; }
.input-area { background-color: #f0f0f0; }
</style>
