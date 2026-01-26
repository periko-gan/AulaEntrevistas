# AulaEntrevistas - Frontend

Este es el frontend de la aplicación **AulaEntrevistas**, una plataforma diseñada para realizar entrevistas de trabajo simuladas con un asistente de inteligencia artificial llamado "Evalio". La aplicación permite a los usuarios registrarse, iniciar sesión, interactuar con la IA, y gestionar sus conversaciones.

## ✨ Características

- **Autenticación de Usuarios:** Sistema completo de registro e inicio de sesión.
- **Interfaz de Chat Interactiva:** Conversación en tiempo real con el asistente de IA "Evalio".
- **Gestión de Chats:**
  - Creación automática de nuevos chats.
  - Persistencia de la sesión de chat al recargar la página.
  - Historial de conversaciones.
  - Posibilidad de renombrar y eliminar chats.
- **Generación de Informes:** Descarga de un informe en PDF para las entrevistas finalizadas.
- **Interfaz Adaptable:**
  - Panel lateral de historial colapsable para maximizar el espacio.
  - Diseño responsivo construido con Bootstrap 5.
- **Tema Personalizado:** Paleta de colores y estilos unificados a través de Sass y SweetAlert2.
- **Código Documentado:** Todo el código fuente está documentado usando JSDoc.

## 🛠️ Tecnologías Utilizadas

- **Framework:** [Vue.js](https://vuejs.org/) (v3) con Composition API (`<script setup>`)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **Gestor de Paquetes:** [pnpm](https://pnpm.io/)
- **Routing:** [Vue Router](https://router.vuejs.org/)
- **Estilos:**
  - [Bootstrap 5](https://getbootstrap.com/) para el layout y componentes.
  - [Sass](https://sass-lang.com/) para la personalización de estilos.
  - [Bootstrap Icons](https://icons.getbootstrap.com/) para la iconografía.
- **Cliente HTTP:** [Axios](https://axios-http.com/) para las peticiones a la API.
- **Notificaciones:** [SweetAlert2](https://sweetalert2.github.io/) para modales y alertas interactivas.
- **Documentación:** [JSDoc](https://jsdoc.app/) para la generación de documentación de código.

## 🚀 Configuración del Proyecto

Sigue estos pasos para levantar el proyecto en un entorno de desarrollo local.

### Prerrequisitos

- [Node.js](https://nodejs.org/) (versión 18 o superior)
- [pnpm](https://pnpm.io/installation)

### Instalación

1.  **Clonar el repositorio:**
    ```sh
    git clone https://github.com/periko-gan/AulaEntrevistas.git
    cd frontend_Proyecto_IA_generalitat
    ```

2.  **Instalar dependencias:**
    ```sh
    pnpm install
    ```

3.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade la URL base de tu API de backend.
    ```
    VITE_API_BASE_URL=http://localhost:8000
    ```
    *(Reemplaza `http://localhost:8000` por la URL correcta si tu backend corre en otro puerto).*

4.  **Ejecutar el servidor de desarrollo:**
    ```sh
    pnpm dev
    ```
    La aplicación estará disponible en la dirección que indique Vite (normalmente `http://localhost:5173`).

## 📜 Scripts Disponibles

- **`pnpm dev`**: Inicia el servidor de desarrollo con Hot-Reload.
- **`pnpm build`**: Compila la aplicación para producción en el directorio `dist/`.
- **`pnpm preview`**: Sirve localmente el contenido de la carpeta `dist/` para previsualizar la build de producción.
- **`pnpm docs`**: Genera la documentación del código fuente en la carpeta `docs/`.

## 📜 Documentación

Este proyecto utiliza [JSDoc](https://jsdoc.app/) para generar la documentación del código a partir de comentarios.

Para generar la documentación, ejecuta:
```sh
pnpm docs
```
Esto creará una carpeta `docs/` en la raíz del proyecto. Puedes abrir el archivo `docs/index.html` en tu navegador para explorar la documentación del código.

## 📁 Estructura del Proyecto

```
/
├── public/
├── src/
│   ├── assets/         # Archivos estáticos (CSS, Sass, imágenes)
│   ├── components/     # Componentes de Vue (Vistas y Partes)
│   │   ├── parts/      # Sub-componentes (Header, Footer, Aside)
│   │   ├── ChatView.vue
│   │   ├── ConversationView.vue
│   │   └── ...
│   ├── composables/    # Lógica reutilizable (hooks de Vue)
│   │   ├── useAside.js
│   │   ├── useChatInterface.js
│   │   ├── useChatView.js
│   │   ├── useConversationView.js
│   │   ├── useFooter.js
│   │   ├── useHeader.js
│   │   ├── useLoginView.js
│   │   └── useRegisterView.js
│   ├── router/         # Configuración de Vue Router
│   │   └── index.js
│   ├── services/       # Lógica de negocio y comunicación con la API
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── chatService.js
│   │   └── chatState.js
│   ├── App.vue         # Componente raíz de la aplicación
│   └── main.js         # Punto de entrada de la aplicación
├── .env.example        # Ejemplo de variables de entorno
├── index.html
├── package.json
└── README.md
```
