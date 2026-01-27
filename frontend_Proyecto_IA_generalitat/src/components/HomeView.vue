<script setup>
/**
 * @file HomeView.vue
 * @description Página de inicio (landing page) de la aplicación.
 * Es un componente puramente presentacional.
 */
import Header from './parts/Header.vue';
import Footer from './parts/Footer.vue';
</script>

<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header :isLoggedIn="false"/>

    <main class="flex-grow-1">
      <!-- Hero Section -->
      <section class="py-5 text-center container">
        <div class="row py-lg-5">
          <div class="col-lg-6 col-md-8 mx-auto">
            <h1 class="fw-bold">Simulador de Entrevistas con IA</h1>
            <p class="lead text-muted">
              Perfecciona tus habilidades de entrevista y consigue el trabajo de tus sueños.
              Nuestra IA te guiará a través de una experiencia de entrevista realista,
              proporcionándote preguntas y feedback valioso.
            </p>
            <p>
              <router-link to="/login" class="btn btn-primary my-2 mx-1">Iniciar Sesión
              </router-link>
              <router-link to="/register" class="btn btn-secondary my-2 mx-1">Registrarse
              </router-link>
            </p>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <div class="album py-5 bg-white">
        <div class="container">
          <div class="row text-center mb-4">
            <h2 class="fw-light">Características Principales</h2>
          </div>
          <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
            <div class="col">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body text-center d-flex flex-column">
                  <i class="bi bi-robot fs-1 text-primary mb-3"></i>
                  <h5 class="card-title">Entrevistas Realistas</h5>
                  <p class="card-text">Participa en simulaciones de entrevistas que imitan
                    escenarios del mundo real para una gran variedad de puestos.</p>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body text-center d-flex flex-column">
                  <i class="bi bi-lightbulb-fill fs-1 text-primary mb-3"></i>
                  <h5 class="card-title">Feedback Instantáneo</h5>
                  <p class="card-text">Recibe análisis y sugerencias sobre tus respuestas para
                    identificar áreas de mejora de forma inmediata.</p>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body text-center d-flex flex-column">
                  <i class="bi bi-graph-up-arrow fs-1 text-primary mb-3"></i>
                  <h5 class="card-title">Seguimiento de Progreso</h5>
                  <p class="card-text">Guarda tu historial de entrevistas y observa cómo mejoras con
                    el tiempo a través de nuestras analíticas.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer/>
  </div>
</template>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
