<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {getChatDetails, getChatMessages, deleteChat, updateChatTitle} from '../services/chatService';
import {getUser, removeSession} from '../services/authService';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';
import Swal from 'sweetalert2';

const route = useRoute();
const router = useRouter();

const chatDetails = ref(null);
const chatMessages = ref([]);
const currentUser = ref(null);
const isLoading = ref(true);
const error = ref('');

// --- Lógica para el botón de scroll ---
const mainContent = ref(null);
const showScrollTopButton = ref(false);

const handleScroll = (event) => {
  showScrollTopButton.value = event.target.scrollTop > 200;
};

const scrollToTop = () => {
  if (mainContent.value) {
    mainContent.value.scrollTo({top: 0, behavior: 'smooth'});
  }
};

// --- Lógica de Carga de Datos ---
const loadConversation = async (chatId) => {
  isLoading.value = true;
  error.value = '';
  chatDetails.value = null;
  chatMessages.value = [];
  const numericChatId = Number(chatId);
  if (!numericChatId) {
    error.value = 'El ID del chat no es válido.';
    isLoading.value = false;
    return;
  }
  try {
    const [detailsResponse, messagesResponse] = await Promise.all([
      getChatDetails(numericChatId),
      getChatMessages(numericChatId)
    ]);
    chatDetails.value = detailsResponse.data;
    chatMessages.value = messagesResponse.data.sort((a, b) => a.id_mensaje - b.id_mensaje);
  } catch (err) {
    console.error('Error detallado al cargar la conversación:', err.response || err);
    error.value = 'No se pudo cargar la conversación. Revisa la consola para más detalles.';
  } finally {
    isLoading.value = false;
  }
};

// --- Ciclo de Vida y Observadores ---
onMounted(() => {
  currentUser.value = getUser();
  loadConversation(route.params.id);
});

watch(() => route.params.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    loadConversation(newId);
  }
});

// --- Propiedades Computadas ---
const userName = computed(() => {
  if (currentUser.value && currentUser.value.nombre) {
    const firstName = currentUser.value.nombre.split(' ')[0];
    return firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();
  }
  return 'Usuario';
});

// --- Manejadores de Eventos ---
const goBackToChat = () => {
  router.push({name: 'Chat'});
};

const handleLogout = async () => {
  const result = await Swal.fire({
    title: '¿Quieres cerrar la sesión?',
    text: 'Serás redirigido a la página de inicio.',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Sí, cerrar sesión',
    cancelButtonText: 'Cancelar',
  });
  if (result.isConfirmed) {
    removeSession();
    router.push({ name: 'Home' });
  }
};

const handleRenameChat = async () => {
  const { value: newTitle } = await Swal.fire({
    title: 'Cambiar nombre del chat',
    input: 'text',
    inputValue: chatDetails.value.title,
    showCancelButton: true,
    confirmButtonText: 'Guardar',
    cancelButtonText: 'Cancelar',
  });
  if (newTitle && newTitle !== chatDetails.value.title) {
    try {
      await updateChatTitle(route.params.id, newTitle);
      chatDetails.value.title = newTitle;
      Swal.fire('¡Éxito!', 'El nombre del chat ha sido actualizado.', 'success');
    } catch (err) {
      console.error('Error al renombrar el chat:', err);
      Swal.fire('Error', 'No se pudo cambiar el nombre del chat.', 'error');
    }
  }
};

const handleDeleteCurrentChat = async () => {
  const result = await Swal.fire({
    title: '¿Estás seguro de que quieres borrar este chat?',
    text: "Esta acción no se puede deshacer.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, ¡bórralo!',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#d33',
  });

  if (result.isConfirmed) {
    try {
      await deleteChat(route.params.id);
      await Swal.fire('¡Borrado!', 'El chat ha sido eliminado.', 'success');
      router.push({ name: 'Chat' });
    } catch (err) {
      console.error('Error al borrar el chat:', err);
      Swal.fire('Error', 'No se pudo borrar el chat.', 'error');
    }
  }
};
</script>

<template>
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userName="userName" @logout="handleLogout"/>

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div class="col-md-3 col-lg-2 d-none d-md-block p-0 h-100">
          <Aside :redirect-on-delete="true" :active-chat-id="route.params.id"/>
        </div>
        <main ref="mainContent" @scroll="handleScroll"
              class="col-md-9 col-lg-10 d-flex flex-column h-100 p-4 overflow-auto position-relative">

          <div v-if="isLoading" class="text-center mt-5">
            <div class="spinner-border" role="status"><span
              class="visually-hidden">Cargando...</span></div>
          </div>
          <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
          <div v-else-if="chatDetails">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div class="d-flex align-items-center">
                <h2 class="fw-bold mb-0">{{ chatDetails.title }}</h2>
                <button @click="handleRenameChat" class="btn btn-sm btn-icon ms-2"
                        title="Renombrar chat">
                  <i class="bi bi-pencil-square fs-5"></i>
                </button>
                <button @click="handleDeleteCurrentChat" class="btn btn-sm btn-icon delete-btn"
                        title="Borrar chat">
                  <i class="bi bi-trash3 fs-5"></i>
                </button>
              </div>
              <button @click="goBackToChat" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-left me-2"></i>Volver al Chat
              </button>
            </div>
            <p class="text-muted mb-4">
              Iniciado por: <span class="fw-semibold">{{ currentUser?.nombre || 'Usuario' }}</span>
              | Chat ID: {{ route.params.id }}
            </p>
            <div class="chat-history">
              <div v-for="message in chatMessages" :key="message.id_mensaje"
                   class="message-row d-flex align-items-end mb-3"
                   :class="message.emisor === 'USER' ? 'justify-content-end' : 'justify-content-start'">
                <div v-if="message.emisor === 'IA'" class="avatar me-2">
                  <i class="bi bi-robot fs-4 text-secondary"></i>
                </div>
                <div class="message-bubble"
                     :class="message.emisor === 'USER' ? 'user-bubble' : 'ai-bubble'">
                  <p class="mb-0" style="white-space: pre-wrap;">{{ message.contenido }}</p>
                  <small class="message-time">{{
                      new Date(message.sent_at).toLocaleString()
                    }}</small>
                </div>
                <div v-if="message.emisor === 'USER'" class="avatar ms-2">
                  <i class="bi bi-person-circle fs-4 text-primary"></i>
                </div>
              </div>
            </div>
          </div>


        </main>
        <!-- Botón Flotante -->
        <button v-if="showScrollTopButton" @click="scrollToTop"
                class="btn btn-primary btn-floating">
          <i class="bi bi-arrow-up-short"></i>
        </button>
      </div>
    </div>
    <Footer/>
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

.message-time {
  display: block;
  font-size: 0.75rem;
  margin-top: 5px;
  text-align: right;
  opacity: 0.7;
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

.btn-floating {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 1.5rem;
  line-height: 1;
  z-index: 10;
}
</style>
