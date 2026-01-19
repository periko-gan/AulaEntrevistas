<script setup>
// --- Importaciones ---
// ref: para crear variables reactivas.
// onMounted: un hook del ciclo de vida que se ejecuta cuando el componente se monta.
// defineExpose: para exponer funciones internas al componente padre.
import { ref, onMounted, defineExpose } from 'vue';

// Importa la función para obtener el historial de chats desde el servicio de chat.
import { getChatHistory } from '../../services/chatService';


// --- Props (Propiedades) ---
// defineProps permite al componente recibir datos de su componente padre.
const props = defineProps({
  // ID del chat que se está viendo actualmente en la página de conversación.
  // Se usa para resaltar el elemento activo en la lista.
  activeChatId: {
    type: [String, Number], // Puede ser un string (de la URL) o un número.
    default: null // Por defecto, no hay ningún chat activo.
  },
  // Un booleano que indica si el panel lateral debe mostrarse en modo colapsado (solo iconos).
  isCollapsed: {
    type: Boolean,
    default: false // Por defecto, el panel no está colapsado.
  }
});

// --- Emits (Eventos) ---
// defineEmits declara los eventos personalizados que este componente puede enviar a su padre.
const emit = defineEmits(['toggle-aside']);

// --- Estado del Componente ---
// 'ref' crea variables reactivas, lo que significa que si su valor cambia, la vista se actualiza.
const chatHistory = ref([]); // Almacenará la lista de chats del historial.
const isLoading = ref(false); // Controla si se muestra el spinner de carga.
const error = ref(''); // Almacena un mensaje de error si la carga falla.

// --- Lógica de Carga del Historial ---
// Función asíncrona para obtener los datos del historial desde la API.
const fetchChatHistory = async () => {
  isLoading.value = true; // Muestra el spinner.
  error.value = ''; // Limpia errores anteriores.
  try {
    const response = await getChatHistory(); // Llama a la función del servicio.
    // Ordena los chats por fecha de creación, de más antiguo a más nuevo.
    const sortedChats = response.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    chatHistory.value = sortedChats; // Actualiza la variable reactiva con los datos ordenados.
  } catch (err) {
    console.error('Error al cargar el historial:', err);
    error.value = 'No se pudo cargar el historial.'; // Guarda el mensaje de error para mostrarlo.
  } finally {
    isLoading.value = false; // Oculta el spinner, tanto si hubo éxito como si hubo error.
  }
};

// --- Hooks de Ciclo de Vida ---
// onMounted es un "hook" que ejecuta una función justo después de que el componente se ha montado en el DOM.
onMounted(fetchChatHistory); // Llama a la función para cargar el historial en cuanto el componente está listo.

// --- Exposición de Métodos ---
// defineExpose hace que una o más funciones internas del componente sean accesibles
// desde su componente padre a través de una referencia de plantilla (template ref).
defineExpose({
  fetchChatHistory // El padre puede llamar a esta función para forzar una recarga del historial.
});
</script>

<template>
  <!-- El 'aside' es el contenedor principal. Se le añade la clase 'collapsed' si la prop isCollapsed es true. -->
  <aside class="d-flex flex-column p-3 bg-light h-100" :class="{ 'collapsed': isCollapsed }">

    <!-- Cabecera del panel lateral -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- El título 'Historial' solo se muestra si el panel NO está colapsado. -->
      <h5 v-if="!isCollapsed" class="text-secondary fw-bold mb-0">
        <i class="bi bi-clock-history me-2"></i>
        Historial
      </h5>
      <!-- El botón de hamburguesa siempre es visible. Al hacer clic, emite el evento 'toggle-aside' al padre. -->
      <button class="btn btn-icon" @click="$emit('toggle-aside')" title="Ocultar/Mostrar historial">
        <i class="bi bi-list fs-4"></i>
      </button>
    </div>

    <!-- Estado de Carga: se muestra un spinner mientras isLoading es true. -->
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Estado de Error: se muestra una alerta si la variable 'error' tiene contenido. -->
    <div v-if="error" class="alert alert-warning small py-2">{{ error }}</div>

    <!-- Estado Vacío: se muestra un mensaje si no está cargando, no hay errores y el historial está vacío. -->
    <div v-if="!isLoading && chatHistory.length === 0 && !error" class="text-center text-muted small">
      <!-- El mensaje cambia dependiendo de si el panel está colapsado o no. -->
      <span v-if="!isCollapsed">No hay chats anteriores.</span>
      <i v-else class="bi bi-archive"></i>
    </div>

    <!-- Lista del Historial: se renderiza un enlace por cada chat en el array 'chatHistory'. -->
    <div class="list-group list-group-flush flex-grow-1 overflow-auto">
      <router-link
        v-for="chat in chatHistory"
        :key="chat.id_chat"
        :to="{ name: 'Conversation', params: { id: chat.id_chat } }"
        class="list-group-item list-group-item-action"
        :class="{ 'active': chat.id_chat == activeChatId }"
      >
        <!-- Si el panel no está colapsado, muestra el título del chat. -->
        <span v-if="!isCollapsed" class="chat-title text-truncate">
          {{ chat.title }}
        </span>
        <!-- Si está colapsado, muestra un icono genérico de chat. -->
        <i v-else class="bi bi-chat-left-text"></i>
      </router-link>
    </div>
  </aside>
</template>

<style scoped>
aside {
  border-right: 1px solid #dee2e6;
  transition: width 0.3s ease; /* Animación suave para el cambio de ancho. */
}
.list-group-item {
  border: none;
  background-color: transparent;
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
  border-radius: 5px;
  color: var(--bs-dark);
  text-decoration: none;
}
.list-group-item:hover {
  background-color: #e9ecef;
}
/* Estilos para el elemento del historial que está activo (el que se está viendo). */
.list-group-item.active {
  background-color: var(--bs-primary);
  color: white;
  border-color: var(--bs-primary);
}
.chat-title {
  flex-grow: 1;
  margin-right: 10px;
}
.btn-icon {
  padding: 0.1rem 0.4rem;
  color: var(--bs-secondary);
  background: none;
  border: none;
}
.btn-icon:hover {
  color: var(--bs-primary);
}

/* Estilos específicos para cuando el panel está en modo colapsado. */
aside.collapsed {
  align-items: center; /* Centra los iconos. */
}
aside.collapsed .list-group-item {
  text-align: center; /* Centra el contenido de cada elemento de la lista. */
}
</style>
