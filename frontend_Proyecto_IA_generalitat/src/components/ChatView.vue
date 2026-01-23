<script setup>
import { useChatView } from '../composables/useChatView';
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
import Aside from './parts/Aside.vue';
import ChatInterface from './parts/ChatInterface.vue';

const {
  userData,
  chatInterfaceRef,
  isAsideCollapsed,
  userName,
  toggleAside,
  handleLogout
} = useChatView();
</script>

<template>
  <div class="d-flex flex-column vh-100">
    <Header :isLoggedIn="true" :userName="userName" @logout="handleLogout" />

    <div class="container-fluid flex-grow-1 overflow-hidden">
      <div class="row h-100">
        <div
          class="d-none d-md-block p-0 h-100"
          :class="isAsideCollapsed ? 'col-auto' : 'col-md-3'"
        >
          <Aside :is-collapsed="isAsideCollapsed" @toggle-aside="toggleAside" />
        </div>
        <div
          class="d-flex flex-column h-100 p-0"
          :class="isAsideCollapsed ? 'col' : 'col-md-9'"
        >
          <ChatInterface ref="chatInterfaceRef" :user-data="userData" />
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped>
/* No se necesitan estilos aquí, ya que están en los componentes hijos */
</style>
