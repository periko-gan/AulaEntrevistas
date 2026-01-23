<script setup>
import { useConversationView } from '../composables/useConversationView';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';

const {
  route,
  chatDetails,
  chatMessages,
  isLoading,
  error,
  asideComponent,
  isAsideCollapsed,
  mainContent,
  showScrollTopButton,
  userName,
  toggleAside,
  handleScroll,
  scrollToTop,
  goBackToChat,
  handleLogout,
  handleRenameChat,
  handleDeleteCurrentChat,
  handleGenerateDocument
} = useConversationView();
</script>

<template>
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userName="userName" @logout="handleLogout"/>

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div
          class="d-none d-md-block p-0 h-100"
          :class="isAsideCollapsed ? 'col-auto' : 'col-md-3'"
        >
          <Aside
            ref="asideComponent"
            :is-collapsed="isAsideCollapsed"
            @toggle-aside="toggleAside"
            :redirect-on-delete="true"
            :active-chat-id="route.params.id"
          />
        </div>
        <main
          ref="mainContent"
          @scroll="handleScroll"
          class="d-flex flex-column h-100 p-4 overflow-auto position-relative"
          :class="isAsideCollapsed ? 'col' : 'col-md-9'"
        >
          <div v-if="isLoading" class="text-center mt-5">
            <div class="spinner-border" role="status"><span
              class="visually-hidden">Cargando...</span></div>
          </div>
          <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
          <div v-else-if="chatDetails">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div class="d-flex align-items-center">
                <h2 class="fw-bold mb-0">{{ chatDetails.title }}</h2>
                <button @click="handleRenameChat" class="btn btn-sm btn-icon ms-2" title="Renombrar chat">
                  <i class="bi bi-pencil-square fs-5"></i>
                </button>
                <button v-if="chatDetails.status === 'completed'" @click="handleGenerateDocument" class="btn btn-sm btn-icon" title="Generar documento">
                  <i class="bi bi-file-earmark-arrow-down fs-5"></i>
                </button>
                <button @click="handleDeleteCurrentChat" class="btn btn-sm btn-icon delete-btn" title="Borrar chat">
                  <i class="bi bi-trash3 fs-5"></i>
                </button>
              </div>
              <button @click="goBackToChat" class="btn btn-outline-secondary">
                Reanudar chat
              </button>
            </div>
            <p class="text-muted mb-4">
              Iniciado por: <span class="fw-semibold">{{ chatDetails.user_name || 'Usuario' }}</span> | Chat ID: {{ route.params.id }}
            </p>
            <div class="chat-history">
              <div v-for="message in chatMessages" :key="message.id_mensaje" class="message-row d-flex align-items-end mb-3" :class="message.emisor === 'USER' ? 'justify-content-end' : 'justify-content-start'">
                <div v-if="message.emisor === 'IA'" class="avatar me-2">
                  <i class="bi bi-robot fs-4 text-secondary"></i>
                </div>
                <div class="message-bubble" :class="message.emisor === 'USER' ? 'user-bubble' : 'ai-bubble'">
                  <p class="mb-0" style="white-space: pre-wrap;">{{ message.contenido }}</p>
                </div>
                <div v-if="message.sender === 'USER'" class="avatar ms-2">
                  <i class="bi bi-person-circle fs-4 text-primary"></i>
                </div>
              </div>
            </div>
          </div>
        </main>
        <button v-if="showScrollTopButton" @click="scrollToTop" class="btn btn-primary btn-floating">
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
  right: 40px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 1.5rem;
  line-height: 1;
  z-index: 10;
}
</style>
