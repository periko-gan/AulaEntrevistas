<script setup>
import { ref } from 'vue'
import Footer from './Footer.vue'

const email = ref('')
const password = ref('')
const errorMessage = ref('')

// Definimos los eventos que este componente puede emitir hacia el padre (App.vue)
const emit = defineEmits(['login-success'])

const handleLogin = () => {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor, introduce tu correo y contraseña.'
    return
  }

  // AQUÍ IRÍA LA LÓGICA REAL DE AUTENTICACIÓN
  // Por ahora, simulamos un login exitoso con cualquier dato
  console.log('Login intentado con:', email.value)

  // Emitimos el evento para avisar a App.vue que el usuario ha entrado
  emit('login-success', { email: email.value })
}
</script>

<template>
  <div class="login-container d-flex flex-column min-vh-100 bg-light">
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <div class="card shadow-lg border-0" style="max-width: 400px; width: 100%">
        <div class="card-header bg-primary text-white text-center py-4">
          <!-- Logo o Título -->
          <h3 class="mb-0 fw-bold">Generalitat Valenciana</h3>
          <small>Acceso al sistema IA</small>
        </div>

        <div class="card-body p-4">
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label text-secondary fw-semibold"
                >Correo Electrónico</label
              >
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                placeholder="usuario@gva.es"
                required
              />
            </div>

            <div class="mb-4">
              <label for="password" class="form-label text-secondary fw-semibold">Contraseña</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                placeholder="••••••••"
                minlength="4"
                required
              />
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2 small" role="alert">
              {{ errorMessage }}
            </div>

            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg fw-bold">Iniciar Sesión</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Footer reutilizable -->
    <Footer />
  </div>
</template>

<style scoped>
/* Ajustes finos adicionales si fueran necesarios */
.login-container {
  background-color: #f8f9fa; /* Un gris muy suave de fondo */
}
.card {
  border-radius: 10px; /* Bordes un poco más redondeados */
}
</style>
