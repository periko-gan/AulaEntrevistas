<script setup>
/**
 * @file ConversationView.vue
 * @description Vista que muestra el historial completo de una conversación específica.
 * La lógica de este componente está gestionada por el composable `useConversationView`.
 */
import {useConversationView} from '../composables/useConversationView';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';
import ConversationInterface from './parts/ConversationInterface.vue'; // Importar el nuevo componente

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
          <ConversationInterface
            :isLoading="isLoading"
            :error="error"
            :chatDetails="chatDetails"
            :chatMessages="chatMessages"
            :route="route"
            :current-user-name="userName"
            @rename-chat="handleRenameChat"
            @generate-document="handleGenerateDocument"
            @delete-chat="handleDeleteCurrentChat"
            @go-back="goBackToChat"
          />
        </main>
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
/* No se necesitan estilos aquí, ya que están en el componente ConversationInterface.vue */
</style>
