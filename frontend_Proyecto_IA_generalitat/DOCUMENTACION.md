# Documentación Oficial del Proyecto: AulaEntrevistas

**Versión:** 1.0
**Fecha:** 2024-08-01
**Autor:** Pedro Miguel Pérez

---

## Índice

1.  [Introducción](#1-introducción)
    1.1. [Propósito del Documento](#11-propósito-del-documento)
    1.2. [Alcance del Proyecto](#12-alcance-del-proyecto)
    1.3. [Público Objetivo](#13-público-objetivo)
2.  [Arquitectura General](#2-arquitectura-general)
    2.1. [Visión General](#21-visión-general)
    2.2. [Frontend (Cliente Vue.js)](#22-frontend-cliente-vuejs)
    2.3. [Backend (API FastAPI)](#23-backend-api-fastapi)
    2.4. [Comunicación](#24-comunicación)
3.  [Detalles de la Aplicación Frontend](#3-detalles-de-la-aplicación-frontend)
    3.1. [Tecnologías Utilizadas](#31-tecnologías-utilizadas)
    3.2. [Estructura de Carpetas](#32-estructura-de-carpetas)
    3.3. [Flujo de Datos y Estado](#33-flujo-de-datos-y-estado)
    3.4. [Componentes Clave](#34-componentes-clave)
    3.5. [Sistema de Enrutamiento](#35-sistema-de-enrutamiento)
    3.6. [Estilos y Tema Visual](#36-estilos-y-tema-visual)
4.  [Guía de Instalación y Despliegue](#4-guía-de-instalación-y-despliegue)
    4.1. [Prerrequisitos](#41-prerrequisitos)
    4.2. [Instalación de Dependencias](#42-instalación-de-dependencias)
    4.3. [Configuración de Entorno](#43-configuración-de-entorno)
    4.4. [Ejecución en Modo Desarrollo](#44-ejecución-en-modo-desarrollo)
    4.5. [Compilación para Producción](#45-compilación-para-producción)
5.  [Guía de Uso](#5-guía-de-uso)
    5.1. [Registro y Autenticación](#51-registro-y-autenticación)
    5.2. [Interfaz Principal del Chat](#52-interfaz-principal-del-chat)
    5.3. [Gestión de Conversaciones](#53-gestión-de-conversaciones)
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

### 3.2. Estructura de Carpetas

La estructura del proyecto está organizada para promover la modularidad y la escalabilidad:

```
/src
├── assets/         # Archivos estáticos (CSS, Sass)
├── components/     # Componentes de Vue (Vistas y Partes)
│   ├── parts/      # Sub-componentes reutilizables (Header, Footer, Aside)
│   └── ...View.vue # Componentes que actúan como páginas completas
├── composables/    # Lógica reutilizable extraída de los componentes
│   └── use...js    # Cada archivo contiene la lógica de un componente
├── router/         # Configuración de Vue Router
│   └── index.js
├── services/       # Lógica de negocio y comunicación con el exterior
│   ├── api.js      # Configuración central de Axios
│   ├── authService.js # Funciones relacionadas con la autenticación
│   ├── chatService.js # Funciones para la API de chats
│   ├── alertService.js# Funciones centralizadas para SweetAlert2
│   └── chatState.js   # Estado global simple para comunicación entre componentes
├── App.vue         # Componente raíz
└── main.js         # Punto de entrada de la aplicación
```

### 3.3. Flujo de Datos y Estado

-   **Props y Eventos:** Es el método principal de comunicación entre componentes padre-hijo.
-   **Composables:** La lógica y el estado local de cada vista se gestionan dentro de su composable correspondiente (ej. `useChatView.js`).
-   **Estado Global Simple (`chatState.js`):** Para casos específicos de comunicación entre componentes no relacionados directamente (ej. `Aside` -> `ChatView`), se utiliza un objeto reactivo simple. Esto evita la sobrecarga de una librería de estado completa como Vuex o Pinia para una necesidad puntual.
-   **`sessionStorage`:** Se utiliza para mantener la persistencia del chat activo si el usuario recarga la página.

### 3.4. Componentes Clave

-   **`App.vue`:** Contenedor principal que renderiza las rutas.
-   **`ChatView.vue`:** Orquesta la vista principal del chat, uniendo el `Header`, `Aside` y `ChatInterface`.
-   **`ConversationView.vue`:** Muestra el historial de una conversación pasada.
-   **`ChatInterface.vue`:** El corazón de la aplicación, donde ocurre la interacción en tiempo real con la IA.
-   **`Aside.vue`:** Panel lateral que muestra el historial de chats y permite iniciar nuevas conversaciones.

### 3.5. Sistema de Enrutamiento

Gestionado por `vue-router`, el archivo `src/router/index.js` define todas las rutas de la aplicación. Incluye un **guardia de navegación global** (`router.beforeEach`) que protege las rutas que requieren autenticación (ej. `/chat`), redirigiendo a los usuarios no autenticados a la página de `/login`.

### 3.6. Estilos y Tema Visual

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
Este comando generará una carpeta `dist/` con los archivos estáticos optimizados, listos para ser desplegados en cualquier servidor web.

---

## 5. Guía de Uso

1.  **Registro/Login:** El usuario debe crear una cuenta o iniciar sesión para acceder a la funcionalidad principal.
2.  **Chat Principal:** Al acceder a `/chat`, se inicia automáticamente una nueva conversación. El usuario puede interactuar con la IA escribiendo en el área de texto.
3.  **Historial:** Las conversaciones pasadas aparecen en el panel lateral. El usuario puede hacer clic en ellas para ver el historial.
4.  **Reanudar Chat:** Desde una conversación antigua, el botón "Reanudar chat" lleva de vuelta a la interfaz principal, cargando la conversación seleccionada.
5.  **Nuevo Chat:** El enlace "Nuevo Chat" en el panel lateral permite iniciar una conversación desde cero en cualquier momento.

---

## 6. Documentación del Código (JSDoc)

Todo el código fuente en `src/` está documentado siguiendo el estándar JSDoc. Para generar una versión HTML de esta documentación, ejecute:

```sh
pnpm docs
```
La documentación estará disponible en la carpeta `docs/`.

---

## 7. Posibles Mejoras a Futuro

-   **Feedback de IA Avanzado:** Analizar las respuestas del usuario para dar feedback sobre claridad, uso de palabras clave, etc.
-   **Perfiles de Usuario:** Una sección donde los usuarios puedan ver estadísticas sobre su rendimiento.
-   **Testing:** Implementar tests unitarios (Vitest) y E2E (Cypress).
-   **CI/CD:** Automatizar el proceso de build y despliegue con herramientas como GitHub Actions.
```
