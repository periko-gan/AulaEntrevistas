<script setup>
import { ref, computed } from 'vue';
import { invokeBedrock } from '../services/bedrock';
import * as formDataService from '../services/formDataService';
import JsonSelect from './JsonSelect.vue';

// --- Estado del Componente ---
const prompt = ref('');
const response = ref('');
const loading = ref(false);
const error = ref('');

const selectedProvincia = ref('');
const selectedMunicipio = ref('');
const selectedCentro = ref('');

// --- Lógica de Datos (usando el servicio) ---
const provincias = formDataService.getProvincias();
const municipios = formDataService.getMunicipios();
const centros = formDataService.getCentros();

const filteredMunicipios = computed(() => {
  if (!selectedProvincia.value) {
    // Si no hay provincia, mostrar todos los municipios
    return municipios;
  }
  return formDataService.getMunicipiosByProvincia(selectedProvincia.value);
});

const filteredCentros = computed(() => {
  if (!selectedProvincia.value) {
    // Si no hay provincia, mostrar todos los centros
    return centros;
  }
  return formDataService.getCentrosByProvincia(selectedProvincia.value);
});

// --- Manejadores de Eventos ---
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    askBedrock();
  }
};

const askBedrock = async () => {
  if (!prompt.value || loading.value) return;

  loading.value = true;
  error.value = '';
  response.value = '';

  try {
    let finalPrompt = prompt.value;
    let context = '';

    if (selectedCentro.value) {
      const centroObj = centros.find(c => c.codigo_centro === selectedCentro.value);
      if (centroObj) context = `Centro educativo ${centroObj.nombre}, en ${centroObj.localidad}`;
    } else if (selectedMunicipio.value) {
      const municipioObj = municipios.find(m => m.codigo === selectedMunicipio.value);
      if (municipioObj) context = `Municipio de ${municipioObj.nombre}`;
    } else if (selectedProvincia.value) {
      const provinciaObj = provincias.find(p => p.codigo === selectedProvincia.value);
      if (provinciaObj) context = `Provincia de ${provinciaObj.nombre}`;
    }

    if (context) {
      finalPrompt += ` (Contexto: ${context})`;
    }

    const result = await invokeBedrock(finalPrompt);
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
        <h2 class="h5 mb-0">Prueba de AWS Bedrock (Titan Express)</h2>
      </div>
      <div class="card-body">

<!--        <div class="row">-->
<!--          <div class="col-12 mb-3">-->
<!--            <label class="form-label">1. Selecciona una provincia (Opcional):</label>-->
<!--            <JsonSelect-->
<!--              v-model="selectedProvincia"-->
<!--              :options="provincias"-->
<!--              labelKey="nombre"-->
<!--              valueKey="codigo"-->
<!--              placeholder="&#45;&#45; Selecciona provincia &#45;&#45;"-->
<!--            />-->
<!--          </div>-->
<!--          <div class="col-md-6 mb-3">-->
<!--            <label class="form-label">2. Filtra por municipio (Opcional):</label>-->
<!--            <JsonSelect-->
<!--              v-model="selectedMunicipio"-->
<!--              :options="filteredMunicipios"-->
<!--              labelKey="nombre"-->
<!--              valueKey="codigo"-->
<!--              placeholder="&#45;&#45; Selecciona municipio &#45;&#45;"-->
<!--            />-->
<!--          </div>-->
<!--          <div class="col-md-6 mb-3">-->
<!--            <label class="form-label">O filtra por centro (Opcional):</label>-->
<!--            <JsonSelect-->
<!--              v-model="selectedCentro"-->
<!--              :options="filteredCentros"-->
<!--              labelKey="nombre"-->
<!--              valueKey="codigo_centro"-->
<!--              placeholder="&#45;&#45; Selecciona centro &#45;&#45;"-->
<!--            />-->
<!--          </div>-->
<!--        </div>-->

        <div class="mb-3">
          <label for="promptInput" class="form-label">Escribe tu pregunta:</label>
          <textarea
            id="promptInput"
            v-model="prompt"
            class="form-control"
            rows="3"
            placeholder="Ej: ¿Qué ciclos formativos de informática hay?"
            @keydown="handleKeydown"
          ></textarea>
          <div class="form-text text-muted">
            Presiona <strong>Enter</strong> para enviar, <strong>Shift + Enter</strong> para nueva línea.
          </div>
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
            <p class="mb-0" style="white-space: pre-wrap;">{{ response }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
