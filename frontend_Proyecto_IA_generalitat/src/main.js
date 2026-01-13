import './assets/css/main.scss'
import 'bootstrap'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Importamos el router

const app = createApp(App)

app.use(router) // Le decimos a la app que use el router

app.mount('#app')
