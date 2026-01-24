/**
 * @file index.js
 * @description Configuración principal de Vue Router. Define todas las rutas de la aplicación
 * y gestiona la lógica de autenticación a través de un guardia de navegación global.
 */

import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/LoginView.vue';
import RegisterView from '../components/RegisterView.vue';
import ChatView from '../components/ChatView.vue';
import HomeView from '../components/HomeView.vue';
import ConversationView from '../components/ConversationView.vue';

/**
 * @description Array que contiene la definición de todas las rutas de la aplicación.
 * @type {Array<object>}
 */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatView,
    meta: { requiresAuth: true },
  },
  {
    path: '/conversation/:id',
    name: 'Conversation',
    component: ConversationView,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

/**
 * @description Instancia del enrutador de Vue.
 * @type {object}
 */
const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * @description Guardia de navegación global que se ejecuta antes de cada cambio de ruta.
 * Se utiliza para proteger las rutas que requieren autenticación.
 * @param {object} to - La ruta de destino.
 * @param {object} from - La ruta de origen.
 * @param {Function} next - Función para resolver el hook de navegación.
 */
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('user-token');

  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
