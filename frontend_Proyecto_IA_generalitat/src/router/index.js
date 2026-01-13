import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/LoginView.vue';
import RegisterView from '../components/RegisterView.vue';
import BedrockTest from '../components/BedrockTest.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
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
    component: BedrockTest,
    // Marcamos esta ruta como que requiere autenticación
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guarda de navegación global
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('user-token'); // Comprueba si el token existe

  // Si la ruta requiere autenticación y el usuario no está logueado...
  if (to.meta.requiresAuth && !isLoggedIn) {
    // ...redirige a la página de login.
    next({ name: 'Login' });
  } else {
    // En cualquier otro caso, permite la navegación.
    next();
  }
});

export default router;
