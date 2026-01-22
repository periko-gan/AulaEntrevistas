import './assets/css/main.scss'
import 'bootstrap' // Restauramos la importación global de Bootstrap JS
import 'bootstrap-icons/font/bootstrap-icons.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Importamos el router

const app = createApp(App);

app.use(router);

app.mount('#app');
