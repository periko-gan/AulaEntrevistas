// src/services/chatState.js
import { reactive } from 'vue';

// Este es un objeto reactivo simple que actúa como un 'store' o estado global.
// Lo usaremos para comunicar qué chat debe cargarse en la página principal.
export const chatState = reactive({
  // Si loadChatId tiene un valor, ChatInterface.vue cargará este chat.
  // Si es null, iniciará uno nuevo.
  loadChatId: null,
});
