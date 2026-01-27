# Documentación Oficial del Proyecto: AulaEntrevistas

**Versión:** 1.0
**Fecha:** 2024-08-01
**Autor:** Pedro Miguel Pérez

---

## Índice

1.  [Introducción](#1-introducción)
    1.  [Propósito del Documento](#11-propósito-del-documento)
    2.  [Alcance del Proyecto](#12-alcance-del-proyecto)
    3.  [Público Objetivo](#13-público-objetivo)
2.  [Arquitectura General](#2-arquitectura-general)
    1.  [Visión General](#21-visión-general)
    2.  [Frontend (Cliente Vue.js)](#22-frontend-cliente-vuejs)
    3.  [Backend (API FastAPI)](#23-backend-api-fastapi)
    4.  [Comunicación](#24-comunicación)
3.  [Detalles de la Aplicación Frontend](#3-detalles-de-la-aplicación-frontend)
    1.  [Tecnologías Utilizadas](#31-tecnologías-utilizadas)
    2.  [Dependencias del Proyecto](#32-dependencias-del-proyecto)
    3.  [Descripción de Archivos y Directorios Clave](#33-descripción-de-archivos-y-directorios-clave)
    4.  [Flujo de Datos y Estado](#34-flujo-de-datos-y-estado)
    5.  [Componentes Clave](#35-componentes-clave)
    6.  [Sistema de Enrutamiento](#36-sistema-de-enrutamiento)
    7.  [Estilos y Tema Visual](#37-estilos-y-tema-visual)
4.  [Guía de Instalación y Despliegue](#4-guía-de-instalación-y-despliegue)
    1.  [Prerrequisitos](#41-prerrequisitos)
    2.  [Instalación de Dependencias](#42-instalación-de-dependencias)
    3.  [Configuración de Entorno](#43-configuración-de-entorno)
    4.  [Ejecución en Modo Desarrollo](#44-ejecución-en-modo-desarrollo)
    5.  [Compilación para Producción](#45-compilación-para-producción)
5.  [Guía de Uso](#5-guía-de-uso)
    1.  [Registro y Autenticación](#51-registro-y-autenticación)
    2.  [Interfaz Principal del Chat](#52-interfaz-principal-del-chat)
    3.  [Gestión de Conversaciones](#53-gestión-de-conversaciones)
6.  [Documentación del Código (JSDoc)](#6-documentación-del-código-jsdoc)
7.  [Posibles Mejoras a Futuro](#7-posibles-mejoras-a-futuro)

---

## 1. Introducción

### 1.1. Propósito del Documento

Este documento proporciona una visión técnica completa del frontend de la aplicación **AulaEntrevistas**. Su objetivo es servir como guía de referencia para desarrolladores, detallando la arquitectura, tecnologías, estructura del código y procedimientos de instalación y uso.

### 1.2. Alcance del Proyecto

**AulaEntrevistas** es una plataforma web interactiva diseñada para simular entrevistas de trabajo mediante un asistente de inteligencia artificial. El sistema permite a los usuarios practicar sus habilidades de comunicación en un entorno controlado, recibir feedback (funcionalidad futura) y gestionar sus sesiones de entrevista.

El alcance de este documento se limita a la **aplicación cliente (frontend)**, desarrollada con Vue.js.

### 1.3. Público Objetivo

Este documento está dirigido a:
-   **Desarrolladores:** Para entender la estructura del código, facilitar el mantenimiento y desarrollar nuevas funcionalidades.
-   **Personal técnico:** Para comprender la arquitectura y las tecnologías implicadas en el proyecto.

---

## 2. Arquitectura General

### 2.1. Visión General

El proyecto sigue una arquitectura cliente-servidor desacoplada.

-   El **Frontend** es una Single-Page Application (SPA) construida con Vue.js. Es responsable de toda la interfaz de usuario y la experiencia de interacción.
-   El **Backend** es una API RESTful construida con FastAPI (Python), que gestiona la lógica de negocio, la autenticación de usuarios y la interacción con la base de datos y el modelo de IA.

### 2.2. Frontend (Cliente Vue.js)

La aplicación cliente se ha construido siguiendo las mejores prácticas modernas de Vue 3, con un fuerte énfasis en la **Composition API** y la separación de responsabilidades. La lógica de los componentes se extrae a archivos reutilizables llamados **"Composables"**, lo que mantiene los archivos `.vue` limpios y centrados en la presentación.

### 2.3. Backend (API FastAPI)

El backend expone una serie de endpoints para gestionar la autenticación, los chats y los mensajes. Toda la comunicación desde el frontend se realiza a través de peticiones HTTP a esta API.

### 2.4. Comunicación

La comunicación entre el frontend y el backend se realiza a través de peticiones HTTP asíncronas gestionadas por la librería **Axios**. Se utiliza un cliente de Axios centralizado (`src/services/api.js`) que incluye interceptores para añadir automáticamente los tokens de autenticación (JWT) a las cabeceras de las peticiones.

---

## 3. Detalles de la Aplicación Frontend

### 3.1. Tecnologías Utilizadas

-   **Framework Principal:** Vue.js 3
-   **Herramienta de Compilación:** Vite
-   **Enrutamiento:** Vue Router
-   **Estilos:** Bootstrap 5, Sass y Bootstrap Icons
-   **Cliente HTTP:** Axios
-   **Notificaciones:** SweetAlert2
-   **Documentación:** JSDoc

### 3.2. Dependencias del Proyecto

El proyecto utiliza `pnpm` para gestionar dos tipos de dependencias definidas en `package.json`:

-   **`dependencies`**: Paquetes necesarios para que la aplicación funcione en producción.
    -   `vue`, `vue-router`: El núcleo de la aplicación.
    -   `axios`: Para la comunicación con la API.
    -   `bootstrap`, `@popperjs/core`, `bootstrap-icons`: Para la interfaz de usuario y estilos.
    -   `sweetalert2`: Para las notificaciones y modales.

-   **`devDependencies`**: Paquetes utilizados únicamente durante el desarrollo y la compilación.
    -   `vite`, `@vitejs/plugin-vue`: El entorno de desarrollo y compilación.
    -   `sass`: El preprocesador de CSS.
    -   `eslint`, `prettier`: Herramientas para el formateo y la calidad del código.
    -   `jsdoc`: Para la generación de la documentación.

Todas las dependencias se instalan ejecutando `pnpm install`.

### 3.3. Descripción de Archivos y Directorios Clave

La estructura del proyecto está organizada para promover la modularidad y la escalabilidad. A continuación, se detalla la función de cada archivo y directorio importante:

```
/
├── public/                     # Archivos estáticos públicos (ej. index.html, favicon)
├── src/                        # Código fuente de la aplicación
│   ├── assets/                 # Archivos estáticos (CSS, Sass, imágenes)
│   │   └── css/
│   │       └── main.scss       # Estilos globales y sobrescrituras de Bootstrap
│   ├── components/             # Componentes de Vue
│   │   ├── parts/              # Sub-componentes reutilizables
│   │   │   ├── Aside.vue       # Panel lateral con historial de chats
│   │   │   ├── ChatInterface.vue # Interfaz principal de chat para la vista de chat
│   │   │   ├── ConversationInterface.vue # Interfaz principal para la vista de conversación
│   │   │   ├── Footer.vue      # Pie de página de la aplicación
│   │   │   └── Header.vue      # Cabecera de la aplicación
│   │   ├── ChatView.vue        # Vista principal del chat
│   │   ├── ConversationView.vue# Vista de una conversación específica
│   │   ├── HomeView.vue        # Página de inicio (landing page)
│   │   ├── LoginView.vue       # Vista de inicio de sesión
│   │   └── RegisterView.vue    # Vista de registro de usuarios
│   ├── composables/            # Lógica reutilizable (hooks de Vue)
│   │   ├── useAside.js         # Lógica para el componente Aside
│   │   ├── useChatInterface.js # Lógica para el componente ChatInterface
│   │   ├── useChatView.js      # Lógica para la vista ChatView
│   │   ├── useConversationInterface.js # Lógica para el componente ConversationInterface
│   │   ├── useConversationView.js # Lógica para la vista ConversationView
│   │   ├── useFooter.js        # Lógica para el componente Footer
│   │   ├── useHeader.js        # Lógica para el componente Header
│   │   ├── useLoginView.js     # Lógica para la vista LoginView
│   │   └── useRegisterView.js  # Lógica para la vista RegisterView
│   ├── router/                 # Configuración de Vue Router
│   │   └── index.js            # Definición de rutas y guardias de navegación
│   ├── services/               # Lógica de negocio y comunicación con el exterior
│   │   ├── api.js              # Configuración central de Axios e interceptores
│   │   ├── authService.js      # Funciones para la autenticación de usuarios
│   │   ├── chatService.js      # Funciones para interactuar con la API de chats
│   │   ├── alertService.js     # Funciones centralizadas para SweetAlert2
│   │   └── chatState.js        # Estado global simple para comunicación entre componentes
│   ├── utils/                  # Funciones de utilidad generales
│   │   └── messageProcessor.js # Procesamiento y formateo de mensajes de la IA
│   ├── App.vue                 # Componente raíz de la aplicación
│   └── main.js                 # Punto de entrada de la aplicación
├── .dockerignore               # Archivos y directorios a ignorar por Docker
├── .env.example                # Ejemplo de variables de entorno
├── Dockerfile                  # Instrucciones para construir la imagen Docker
├── index.html                  # Plantilla HTML principal
├── jsdoc.json                  # Configuración de JSDoc
├── package.json                # Metadatos del proyecto y scripts
├── pnpm-lock.yaml              # Bloqueo de versiones de dependencias
└── README.md                   # Descripción general del proyecto
```

### 3.4. Flujo de Datos y Estado

-   **Props y Eventos:** Es el método principal de comunicación entre componentes padre-hijo.
-   **Composables:** La lógica y el estado local de cada vista se gestionan dentro de su composable correspondiente (ej. `useChatView.js`).
-   **Estado Global Simple (`chatState.js`):** Para casos específicos de comunicación entre componentes no relacionados directamente (ej. `Aside` -> `ChatView`), se utiliza un objeto reactivo simple. Esto evita la sobrecarga de una librería de estado completa como Vuex o Pinia para una necesidad puntual.
-   **`sessionStorage`:** Se utiliza para mantener la persistencia del chat activo si el usuario recarga la página.

### 3.5. Componentes Clave

-   **`App.vue`:** Contenedor principal que renderiza las rutas.
-   **`ChatView.vue`:** Orquesta la vista principal del chat, uniendo el `Header`, `Aside` y `ChatInterface`.
-   **`ConversationView.vue`:** Orquesta la vista de una conversación específica, uniendo el `Header`, `Aside` y `ConversationInterface`.
-   **`ChatInterface.vue`:** El corazón de la aplicación, donde ocurre la interacción en tiempo real con la IA en la vista de chat.
-   **`ConversationInterface.vue`:** Componente que muestra el historial de mensajes y las acciones específicas de una conversación pasada.
-   **`Aside.vue`:** Panel lateral que muestra el historial de chats y permite iniciar nuevas conversaciones.

### 3.6. Sistema de Enrutamiento

Gestionado por `vue-router`, el archivo `src/router/index.js` define todas las rutas de la aplicación. Incluye un **guardia de navegación global** (`router.beforeEach`) que protege las rutas que requieren autenticación (ej. `/chat`), redirigiendo a los usuarios no autenticados a la página de `/login`.

### 3.7. Estilos y Tema Visual

El sistema de estilos se basa en **Sass** y **Bootstrap 5**. El archivo `src/assets/css/main.scss` es el punto de entrada principal, donde:
1.  Se definen variables de color personalizadas.
2.  Se sobrescriben las variables por defecto de Bootstrap para adaptar la paleta de colores.
3.  Se importan los estilos de Bootstrap y SweetAlert2.
4.  Se aplican sobreescrituras de CSS directas para personalizar componentes externos como SweetAlert2.

---

## 4. Guía de Instalación y Despliegue

### 4.1. Prerrequisitos

-   Node.js (v18+)
-   pnpm

### 4.2. Instalación de Dependencias

```sh
pnpm install
```

### 4.3. Configuración de Entorno

Crear un archivo `.env` en la raíz del proyecto con la siguiente variable:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 4.4. Ejecución en Modo Desarrollo

```sh
pnpm dev
```

### 4.5. Compilación para Producción

```sh
pnpm build
```
Este comando generará una carpeta `dist/` con los archivos estáticos optimizados.

---

## 5. Guía de Uso

1.  **Registro/Login:** El usuario debe crear una cuenta o iniciar sesión.
2.  **Chat Principal:** Al acceder a `/chat`, se inicia una nueva conversación.
3.  **Historial:** Las conversaciones pasadas aparecen en el panel lateral.
4.  **Reanudar Chat:** Desde una conversación antigua, el botón "Reanudar chat" carga la conversación en la vista principal.
5.  **Nuevo Chat:** El enlace "Nuevo Chat" inicia una conversación desde cero.

---

## 6. Documentación del Código (JSDoc)

Todo el código fuente en `src/` está documentado. Para generar una versión HTML de esta documentación, ejecuta:

```sh
pnpm docs
```
La documentación estará disponible en la carpeta `docs/`.

---

## 7. Posibles Mejoras a Futuro

-   **Feedback de IA Avanzado:** Analizar las respuestas del usuario.
-   **Perfiles de Usuario:** Estadísticas de rendimiento.
-   **Testing:** Implementar tests unitarios y E2E.
-   **CI/CD:** Automatizar el proceso de build y despliegue.
```
