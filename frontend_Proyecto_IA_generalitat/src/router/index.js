// --- Importaciones ---

// Importa las funciones principales de la librería vue-router.
// createRouter: la función para crear la instancia del enrutador.
// createWebHistory: una función que activa el modo de historial HTML5 (URLs limpias sin #).
import {createRouter, createWebHistory} from 'vue-router';

// Importa el componente para la vista de inicio de sesión.
import LoginView from '../components/LoginView.vue';
// Importa el componente para la vista de registro.
import RegisterView from '../components/RegisterView.vue';
// Importa el componente para la vista principal del chat.
import Chat from '../components/Chat.vue';
// Importa el componente para la página de inicio (landing page).
import Home from '../components/Home.vue';
// Importa el componente para la vista de una conversación individual.
import Conversation from '../components/Conversation.vue';

// --- Definición de Rutas ---
// 'routes' es un array de objetos donde cada objeto define una ruta de la aplicación.
const routes = [
  // Ruta para la página de inicio (landing page)
  {
    path: '/', // La URL en el navegador
    name: 'Home', // Un nombre único para la ruta, útil para la navegación programática (router.push({ name: 'Home' }))
    component: Home, // El componente de Vue que se renderizará en esta ruta
  },
  // Ruta para la página de inicio de sesión
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  // Ruta para la página de registro
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  // Ruta para la página principal del chat
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    // 'meta' contiene información adicional sobre la ruta.
    // Aquí la usamos para marcar esta ruta como una que requiere autenticación.
    meta: {requiresAuth: true},
  },
  // Ruta para ver una conversación específica. Es una ruta dinámica.
  {
    path: '/conversation/:id', // ':id' es un parámetro dinámico. Coincidirá con /conversation/1, /conversation/2, etc.
    name: 'Conversation',
    component: Conversation,
    meta: {requiresAuth: true}, // También requiere que el usuario esté logueado.
  },
  // Ruta "catch-all" (comodín)
  {
    path: '/:pathMatch(.*)*', // Esta expresión regular coincide con cualquier URL que no haya coincidido antes.
    redirect: '/', // Redirige cualquier URL no encontrada a la página de inicio.
  },
]

// --- Creación del Router ---
// Se crea la instancia del enrutador.
const router = createRouter({
  // 'history' define el modo de historial. createWebHistory() usa la History API del navegador
  // para lograr una navegación sin recargar la página y con URLs limpias (sin #).
  history: createWebHistory(),
  // Se le pasa el array de rutas que hemos definido.
  routes,
});

// --- Guardia de Navegación Global (Navigation Guard) ---
// 'router.beforeEach' es una función que se ejecuta ANTES de que se realice cada cambio de ruta.
// Es el lugar perfecto para poner la lógica de autenticación.
router.beforeEach((to, from, next) => {
  // 'to': la ruta a la que se quiere navegar.
  // 'from': la ruta desde la que se viene.
  // 'next': una función que se debe llamar para resolver el hook y continuar la navegación.

  // Comprobamos si el usuario está logueado revisando si existe el token en el localStorage.
  // El doble '!!' convierte el resultado (el token o null) en un booleano (true o false).
  const isLoggedIn = !!localStorage.getItem('user-token');

  // Si la ruta a la que se quiere ir (to.meta.requiresAuth) requiere autenticación
  // Y el usuario NO está logueado (!isLoggedIn)...
  if (to.meta.requiresAuth && !isLoggedIn) {
    // ...lo redirigimos a la página de Login.
    next({name: 'Login'});
  } else {
    // Si no, permitimos que la navegación continúe con normalidad.
    next();
  }
});

// --- Exportación ---
// Se exporta la instancia del router para que pueda ser usada en la aplicación principal (main.js).
export default router;
