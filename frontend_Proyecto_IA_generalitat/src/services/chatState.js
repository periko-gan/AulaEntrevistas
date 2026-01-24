/**
 * @file chatState.js
 * @description Estado global reactivo para la comunicación entre componentes relacionados con el chat.
 * Se utiliza para pasar información de manera indirecta, como indicar qué chat cargar o si se debe forzar la creación de uno nuevo.
 */
import { reactive } from 'vue';

/**
 * @description Objeto reactivo que funciona como un 'store' o estado global simple.
 * @property {number|null} loadChatId - Si tiene un valor, indica a `ChatInterface.vue` que debe cargar este chat específico. Se limpia después de su uso.
 * @property {boolean} forceNewChat - Si es `true`, indica a `ChatInterface.vue` que debe ignorar cualquier otro estado y empezar un chat completamente nuevo. Se resetea a `false` después de su uso.
 */
export const chatState = reactive({
  loadChatId: null,
  forceNewChat: false,
});
