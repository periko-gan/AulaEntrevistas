import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/LoginView.vue';
import RegisterView from '../components/RegisterView.vue';
import Chat from '../components/Chat.vue';
import Home from '../components/Home.vue';
import Conversation from '../components/Conversation.vue'; // Corregido para que coincida con el nombre del archivo

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
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
    component: Chat,
    meta: { requiresAuth: true },
  },
  {
    path: '/conversation/:id',
    name: 'Conversation',
    component: Conversation,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('user-token');

  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
