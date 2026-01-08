<script setup>
import { ref } from 'vue';
import { invokeBedrock } from '../services/bedrock';

const prompt = ref('');
const response = ref('');
const loading = ref(false);
const error = ref('');

const askBedrock = async () => {
  if (!prompt.value) return;

  loading.value = true;
  error.value = '';
  response.value = '';

  try {
    const result = await invokeBedrock(prompt.value);
    response.value = result;
  } catch (err) {
    error.value = "Error al conectar con Bedrock. Revisa la consola y tus credenciales.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h2 class="h5 mb-0">Prueba de AWS Bedrock (Claude 3)</h2>
      </div>
      <div class="card-body">
        <div class="mb-3">
          <label for="promptInput" class="form-label">Escribe tu pregunta:</label>
          <input
            id="promptInput"
            v-model="prompt"
            class="form-control"
            placeholder="Ej: Explícame qué es la Generalitat Valenciana..."
          >
        </div>

        <button
          @click="askBedrock"
          class="btn btn-primary"
          :disabled="loading || !prompt"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          {{ loading ? 'Generando...' : 'Enviar a la IA' }}
        </button>

        <div v-if="error" class="alert alert-danger mt-3" role="alert">
          {{ error }}
        </div>

        <div v-if="response" class="mt-4">
          <h5 class="text-secondary">Respuesta:</h5>
          <div class="p-3 bg-light border rounded">
            <p class="mb-0">{{ response }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
