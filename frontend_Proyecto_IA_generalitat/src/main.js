/**
 * @file main.js
 * @description Punto de entrada principal de la aplicación Vue.
 * Se encarga de inicializar la aplicación, el enrutador y los estilos globales.
 */

// --- Importaciones de Estilos ---
import './assets/css/main.scss'; // Estilos personalizados y sobreescrituras de Bootstrap/Sass.
import 'bootstrap'; // JavaScript de Bootstrap (requiere @popperjs/core).
import 'bootstrap-icons/font/bootstrap-icons.css'; // Iconos de Bootstrap.

// --- Importaciones de Vue y la Aplicación ---
import { createApp } from 'vue';
import App from './App.vue'; // Componente raíz.
import router from './router'; // Configuración de Vue Router.

/**
 * @description Creación de la instancia de la aplicación Vue.
 * @type {object}
 */
const app = createApp(App);

// Se registra el plugin de Vue Router en la instancia de la aplicación.
app.use(router);

// Se monta la aplicación en el elemento del DOM con el id 'app'.
app.mount('#app');
