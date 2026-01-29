# DOCUMENTACIÓN TÉCNICA DEL PROYECTO

---

## PORTADA

### 📋 Información del Proyecto

**Nombre del Proyecto:** AulaEntrevistas - Plataforma de Simulación de Entrevistas Técnicas con Inteligencia Artificial

**Tipo de Proyecto:** Aplicación web cliente-servidor con integración de servicios de inteligencia artificial

**Fecha:** Enero 2026

**Autor:** Proyecto desarrollado para la Generalitat Valenciana

---

### 💻 Stack Tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| **Backend** | Python 3.11, FastAPI 0.115.0, SQLAlchemy 2.0, MySQL 8.0 |
| **Frontend** | Vue.js 3, Vite, Bootstrap 5, Axios |
| **IA y Servicios** | AWS Bedrock (Amazon Nova), WeasyPrint |
| **DevOps** | Docker, Docker Compose, Alembic |

---

## ÍNDICE

1. [INTRODUCCIÓN](#1-introducción)
   - [1.1. Contexto del proyecto](#11-contexto-del-proyecto)
   - [1.2. Problema que resuelve](#12-problema-que-resuelve)
   - [1.3. Público objetivo](#13-público-objetivo)
   - [1.4. Objetivo general del sistema](#14-objetivo-general-del-sistema)

2. [VISIÓN GENERAL DEL SISTEMA](#2-visión-general-del-sistema)
   - [2.1. Descripción global del funcionamiento](#21-descripción-global-del-funcionamiento)
   - [2.2. Arquitectura general (cliente-servidor)](#22-arquitectura-general-cliente-servidor)
   - [2.3. Flujo básico de uso](#23-flujo-básico-de-uso)

3. [TECNOLOGÍAS UTILIZADAS](#3-tecnologías-utilizadas)
   - [3.1. Backend](#31-backend)
   - [3.2. Frontend](#32-frontend)
   - [3.3. Herramientas de desarrollo y despliegue](#33-herramientas-de-desarrollo-y-despliegue)
   - [3.4. Justificación de las decisiones tecnológicas](#34-justificación-de-las-decisiones-tecnológicas)

4. [ARQUITECTURA DEL SISTEMA](#4-arquitectura-del-sistema)
   - [4.1. Descripción de la arquitectura backend](#41-descripción-de-la-arquitectura-backend)
   - [4.2. Descripción de la arquitectura frontend](#42-descripción-de-la-arquitectura-frontend)
   - [4.3. Separación de responsabilidades](#43-separación-de-responsabilidades)
   - [4.4. Diagrama conceptual explicado en texto](#44-diagrama-conceptual-explicado-en-texto)

5. [BACKEND](#5-backend)
   - [5.1. Estructura general del proyecto](#51-estructura-general-del-proyecto)
   - [5.2. Organización por capas](#52-organización-por-capas)
   - [5.3. Gestión de usuarios y autenticación](#53-gestión-de-usuarios-y-autenticación)
   - [5.4. Endpoints principales](#54-endpoints-principales)
   - [5.5. Seguridad y control de acceso](#55-seguridad-y-control-de-acceso)
   - [5.6. Gestión de errores y validaciones](#56-gestión-de-errores-y-validaciones)

6. [FRONTEND](#6-frontend)
   - [6.1. Estructura general del proyecto](#61-estructura-general-del-proyecto)
   - [6.2. Pantallas principales](#62-pantallas-principales)
   - [6.3. Flujo de navegación](#63-flujo-de-navegación)
   - [6.4. Comunicación con el backend](#64-comunicación-con-el-backend)
   - [6.5. Gestión del estado y datos](#65-gestión-del-estado-y-datos)
   - [6.6. Criterios de usabilidad y accesibilidad](#66-criterios-de-usabilidad-y-accesibilidad)

7. [BASE DE DATOS](#7-base-de-datos)
   - [7.1. Tipo de base de datos](#71-tipo-de-base-de-datos)
   - [7.2. Entidades principales](#72-entidades-principales)
   - [7.3. Relaciones generales](#73-relaciones-generales)
   - [7.4. Justificación del diseño](#74-justificación-del-diseño)

8. [SEGURIDAD](#8-seguridad)
   - [8.1. Autenticación y autorización](#81-autenticación-y-autorización)
   - [8.2. Protección de datos](#82-protección-de-datos)
   - [8.3. Medidas básicas de seguridad aplicadas](#83-medidas-básicas-de-seguridad-aplicadas)

9. [DESPLIEGUE Y EJECUCIÓN](#9-despliegue-y-ejecución)
   - [9.1. Entorno de desarrollo](#91-entorno-de-desarrollo)
   - [9.2. Requisitos para ejecutar el proyecto](#92-requisitos-para-ejecutar-el-proyecto)
   - [9.3. Variables de entorno](#93-variables-de-entorno)
   - [9.4. Despliegue en local con Docker](#94-despliegue-en-local-con-docker)
   - [9.5. Despliegue en producción](#95-despliegue-en-producción)

10. [PRUEBAS](#10-pruebas)
    - [10.1. Estrategia de pruebas](#101-estrategia-de-pruebas)
    - [10.2. Tipos de pruebas realizadas](#102-tipos-de-pruebas-realizadas)
    - [10.3. Validación del funcionamiento](#103-validación-del-funcionamiento)

11. [LIMITACIONES ACTUALES](#11-limitaciones-actuales)
    - [11.1. Restricciones técnicas](#111-restricciones-técnicas)
    - [11.2. Funcionalidades no implementadas](#112-funcionalidades-no-implementadas)

12. [POSIBLES MEJORAS FUTURAS](#12-posibles-mejoras-futuras)
    - [12.1. Escalabilidad](#121-escalabilidad)
    - [12.2. Nuevas funcionalidades](#122-nuevas-funcionalidades)
    - [12.3. Optimización técnica](#123-optimización-técnica)

13. [CONCLUSIÓN](#13-conclusión)
    - [13.1. Valor del proyecto](#131-valor-del-proyecto)
    - [13.2. Aprendizajes técnicos](#132-aprendizajes-técnicos)
    - [13.3. Aplicabilidad real del sistema](#133-aplicabilidad-real-del-sistema)

---

## 1. INTRODUCCIÓN

### 1.1. Contexto del proyecto

La inserción laboral del alumnado de Formación Profesional constituye uno de los indicadores más relevantes de calidad educativa. Sin embargo, muchos estudiantes acceden al mercado laboral sin haber experimentado situaciones reales de entrevistas técnicas, lo que genera inseguridad y reduce sus posibilidades de éxito en los procesos de selección.

En este contexto surge AulaEntrevistas, también conocido como proyecto Evalio, una solución tecnológica diseñada para simular entrevistas técnicas de forma automatizada, personalizada y escalable, proporcionando al alumnado un entorno seguro donde practicar antes de enfrentarse a situaciones reales.

### 1.2. Problema que resuelve

El proyecto aborda los siguientes problemas identificados:

| Problema | Descripción |
|----------|-------------|
| **🎯 Falta de experiencia práctica** | Los estudiantes no tienen oportunidades suficientes para practicar entrevistas técnicas en condiciones controladas. |
| **⏰ Limitaciones de recursos** | Los centros educativos no disponen del personal ni del tiempo necesario para realizar entrevistas simuladas individualizadas con cada alumno. |
| **📊 Ausencia de feedback estructurado** | Las simulaciones tradicionales carecen de informes detallados que permitan a los estudiantes identificar áreas de mejora específicas. |
| **🔄 Dificultad de adaptación** | Las entrevistas simuladas tradicionales no se adaptan dinámicamente al nivel ni a la especialidad de cada candidato. |

### 1.3. Público objetivo

El sistema está diseñado para los siguientes perfiles de usuario:

- **Alumnado de Formación Profesional:** Estudiantes de ciclos formativos de distintas familias profesionales que necesitan prepararse para entrevistas técnicas laborales.
- **Centros educativos:** Instituciones formativas que buscan herramientas de orientación laboral para su alumnado.
- **Servicios de orientación profesional:** Departamentos de la Generalitat u otras entidades que trabajan en empleabilidad.

### 1.4. Objetivo general del sistema

El objetivo principal del sistema es proporcionar una plataforma accesible, interactiva y automatizada que permita a los estudiantes realizar entrevistas técnicas simuladas con un asistente de inteligencia artificial, recibir feedback constructivo y mejorar sus competencias de comunicación técnica y empleabilidad.

**Objetivos específicos del sistema:**

- ✅ Simular conversaciones realistas de entrevistas técnicas adaptadas al perfil del usuario
- ✅ Generar automáticamente informes de evaluación personalizados al finalizar cada entrevista
- ✅ Permitir la gestión de múltiples sesiones de entrevista por usuario
- ✅ Garantizar la seguridad y privacidad de los datos de los usuarios
- ✅ Facilitar el acceso desde cualquier dispositivo con conexión a internet

---

## 2. VISIÓN GENERAL DEL SISTEMA

### 2.1. Descripción global del funcionamiento

AulaEntrevistas es una aplicación web completa que funciona bajo el paradigma cliente-servidor. El usuario accede a través de un navegador web a una interfaz visual desarrollada con Vue.js, desde la cual puede registrarse, autenticarse e iniciar conversaciones simuladas con un asistente de inteligencia artificial denominado Evalio.

**El sistema consta de tres componentes principales:**

```
┌─────────────────────────────────────────────────────────────┐
│                      COMPONENTES CLAVE                      │
├─────────────────────────────────────────────────────────────┤
│ 1. FRONTEND                                                 │
│    └─ Interfaz Vue.js responsiva y moderna                  │
│    └─ Gestión de interacción visual y navegación           │
│                                                             │
│ 2. BACKEND                                                  │
│    └─ API RESTful con FastAPI                              │
│    └─ Lógica de negocio y persistencia de datos            │
│    └─ Comunicación con servicios externos                  │
│                                                             │
│ 3. SERVICIOS EXTERNOS                                       │
│    └─ AWS Bedrock (Amazon Nova)                            │
│    └─ Procesamiento de lenguaje natural                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Arquitectura general (cliente-servidor)

El sistema implementa una arquitectura cliente-servidor desacoplada con comunicación basada en protocolo HTTP/HTTPS y formato JSON para el intercambio de datos.

**Componentes arquitectónicos:**

- **Cliente (Frontend):** Aplicación SPA (Single Page Application) desarrollada en Vue.js que se ejecuta en el navegador del usuario. Se encarga de la presentación de la información y la captura de entradas del usuario.

- **Servidor (Backend):** API REST desarrollada en Python con FastAPI que se ejecuta en un servidor de aplicaciones Uvicorn. Gestiona la autenticación, el acceso a la base de datos, las reglas de negocio y la comunicación con servicios externos de inteligencia artificial.

- **Base de datos:** Sistema gestor de base de datos MySQL que almacena de forma persistente la información de usuarios, conversaciones y mensajes.

- **Servicios en la nube:** Utilización de AWS Bedrock para el procesamiento de lenguaje natural mediante modelos de la familia Amazon Nova.

**Flujo de comunicación:**

El cliente realiza peticiones HTTP al servidor a través de endpoints REST bien definidos. El servidor procesa las peticiones, aplica lógica de negocio, consulta o modifica datos en la base de datos y, cuando es necesario, invoca servicios de inteligencia artificial para generar respuestas conversacionales. Finalmente, el servidor devuelve una respuesta estructurada en formato JSON que el cliente procesa y presenta visualmente al usuario.

### 2.3. Flujo básico de uso

El flujo estándar de uso del sistema consta de las siguientes etapas:

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE USO DEL SISTEMA                 │
└─────────────────────────────────────────────────────────────┘

    1️⃣  REGISTRO E INICIO DE SESIÓN
         └─ Registro con nombre y correo electrónico
         └─ Autenticación con credenciales
                ↓
    2️⃣  CREACIÓN DE CONVERSACIÓN
         └─ Nuevo chat creado automáticamente
         └─ Continuación de conversaciones previas
                ↓
    3️⃣  INTERACCIÓN CON EVALIO (IA)
         └─ Envío de mensajes del usuario
         └─ Respuestas adaptativas del entrevistador virtual
         └─ Ajuste dinámico de dificultad
                ↓
    4️⃣  GESTIÓN DE ENTREVISTAS
         └─ Pausar/reanudar conversación
         └─ Renombrar chat
         └─ Consultar historial
         └─ Eliminar entrevistas
                ↓
    5️⃣  GENERACIÓN DE INFORME
         └─ Informe PDF con análisis de desempeño
         └─ Feedback constructivo
         └─ Recomendaciones de mejora
```

---

## 3. TECNOLOGÍAS UTILIZADAS

### 3.1. Backend

El backend del sistema ha sido desarrollado utilizando las siguientes tecnologías y herramientas:

**Lenguaje de programación:**
- Python 3.11: Lenguaje principal por su versatilidad, amplio ecosistema de librerías y capacidad para integrarse con servicios de inteligencia artificial.

**Framework web:**
- FastAPI 0.115.0: Framework moderno de alto rendimiento para la construcción de APIs RESTful. Se ha elegido por su soporte nativo de validación de datos con Pydantic, generación automática de documentación OpenAPI y compatibilidad con programación asíncrona.

**Servidor de aplicaciones:**
- Uvicorn 0.30.6: Servidor ASGI de alto rendimiento optimizado para ejecutar aplicaciones FastAPI.

**ORM y gestión de base de datos:**
- SQLAlchemy 2.0.34: ORM robusto para la gestión de modelos de datos y consultas a la base de datos relacional.
- PyMySQL 1.1.1: Conector Python para MySQL.
- MySQL 8.0: Sistema gestor de base de datos relacional elegido por su estabilidad, rendimiento y amplio soporte comunitario.
- Alembic 1.13.1: Herramienta de migraciones de base de datos para gestionar cambios en el esquema de forma controlada y versionada.

**Autenticación y seguridad:**
- python-jose 3.3.0: Librería para la creación y validación de tokens JWT (JSON Web Tokens).
- Passlib 1.7.4: Framework de hashing de contraseñas con soporte para bcrypt.
- bcrypt 4.0.1: Algoritmo de hashing seguro para el almacenamiento de contraseñas.

**Validación y configuración:**
- Pydantic 2.9.2: Librería de validación de datos y gestión de esquemas.
- pydantic-settings 2.5.2: Gestión de configuración mediante variables de entorno.
- email-validator 2.1.1: Validación de formato de direcciones de correo electrónico.

**Servicios de inteligencia artificial:**
- boto3 1.35.0: SDK de AWS para Python, utilizado para la comunicación con AWS Bedrock y sus modelos de inteligencia artificial (Amazon Nova).

**Generación de documentos:**
- WeasyPrint 60.2: Librería para la conversión de HTML/CSS a documentos PDF de alta calidad.
- Pillow 10.3.0: Librería de procesamiento de imágenes.

**Protección y límites:**
- slowapi 0.1.9: Implementación de rate limiting para proteger endpoints de abuso y ataques de denegación de servicio.

**Testing:**
- pytest: Framework de testing para pruebas unitarias e integración.

### 3.2. Frontend

El frontend del sistema utiliza las siguientes tecnologías:

**Framework JavaScript:**
- Vue.js 3.5.25: Framework progresivo para la construcción de interfaces de usuario interactivas. Se ha elegido por su curva de aprendizaje suave, excelente rendimiento y su sistema de componentes reutilizables basado en Composition API.

**Herramienta de construcción:**
- Vite 7.3.0: Build tool moderno y rápido optimizado para Vue.js, que proporciona recarga en caliente instantánea y optimización de assets para producción.

**Gestión de rutas:**
- Vue Router 4.3.3: Sistema oficial de enrutamiento para Vue.js que permite la navegación entre vistas sin recargar la página completa (SPA).

**Cliente HTTP:**
- Axios 1.7.2: Cliente HTTP basado en promesas para realizar peticiones al backend de forma asíncrona.

**Framework CSS y componentes UI:**
- Bootstrap 5.3.3: Framework CSS responsivo para la construcción de interfaces visuales consistentes.
- Bootstrap Icons 1.13.1: Conjunto de iconos vectoriales integrados con Bootstrap.
- Sass 1.97.0: Preprocesador CSS que permite escribir estilos más mantenibles con variables, mixins y anidación.

**Notificaciones y diálogos:**
- SweetAlert2 11.26.17: Librería para la creación de modales, alertas y notificaciones visuales atractivas y accesibles.

**Gestión de paquetes:**
- pnpm 10.28.1: Gestor de paquetes eficiente y rápido que optimiza el espacio en disco mediante enlaces simbólicos.

**Documentación de código:**
- JSDoc 4.0.3: Herramienta para generar documentación a partir de comentarios estructurados en el código JavaScript.

**Calidad de código:**
- ESLint 9.39.1: Linter para identificar y corregir problemas en el código JavaScript.
- Prettier 3.6.2: Formateador de código para mantener un estilo consistente.

### 3.3. Herramientas de desarrollo y despliegue

**Contenerización:**
- Docker: Plataforma de contenedores para empaquetar la aplicación con todas sus dependencias, garantizando consistencia entre entornos de desarrollo, pruebas y producción.
- Docker Compose: Herramienta de orquestación para gestionar múltiples contenedores (backend, base de datos, frontend) como un único sistema.

**Control de versiones:**
- Git: Sistema de control de versiones distribuido para el seguimiento de cambios en el código fuente.

**Entornos de ejecución:**
- Node.js 20.19+: Entorno de ejecución JavaScript para herramientas de desarrollo frontend.

### 3.4. Justificación de las decisiones tecnológicas

**FastAPI:** Se eligió por su alto rendimiento, generación automática de documentación interactiva (Swagger UI), validación de datos mediante Pydantic y soporte nativo para operaciones asíncronas, lo que facilita la integración con servicios externos como AWS.

**Vue.js 3:** Su Composition API permite escribir código más modular y reutilizable. Además, su ecosistema maduro y su excelente documentación facilitan el desarrollo y mantenimiento del proyecto.

**MySQL:** Base de datos relacional robusta y ampliamente utilizada, ideal para estructuras de datos con relaciones claras entre usuarios, chats y mensajes.

**AWS Bedrock:** Proporciona acceso a modelos de lenguaje de última generación (Amazon Nova) mediante una API sencilla, sin necesidad de gestionar infraestructura de machine learning.

**Docker:** Facilita el despliegue consistente en cualquier entorno y simplifica la configuración inicial del proyecto para nuevos desarrolladores.

---

## 4. ARQUITECTURA DEL SISTEMA

### 4.1. Descripción de la arquitectura backend

El backend sigue una arquitectura en capas claramente definidas, siguiendo principios de separación de responsabilidades y diseño limpio:

**Capa de API (Endpoints):**
Localizada en `app/api/v1/`, esta capa contiene los controladores que exponen los endpoints REST. Cada módulo gestiona un recurso específico del sistema:
- `auth.py`: Endpoints de registro y autenticación de usuarios.
- `chats.py`: Operaciones CRUD sobre conversaciones (crear, listar, actualizar, eliminar).
- `messages.py`: Gestión de mensajes dentro de las conversaciones.
- `ai.py`: Endpoints para la interacción con la inteligencia artificial y generación de informes PDF.

La capa de API se limita a validar datos de entrada mediante esquemas Pydantic, invocar servicios de la capa superior y devolver respuestas HTTP estructuradas.

**Capa de servicios (Lógica de negocio):**
Ubicada en `app/services/`, esta capa contiene toda la lógica de negocio del sistema:
- `auth_service.py`: Lógica de registro, login, generación y validación de tokens JWT.
- `chat_service.py`: Gestión de conversaciones, incluyendo reglas de negocio relacionadas con estados de chat.
- `message_service.py`: Procesamiento de mensajes y coordinación con el repositorio.
- `bedrock_service.py`: Comunicación con AWS Bedrock, gestión de contexto conversacional y sanitización de entradas para prevenir ataques de prompt injection.
- `pdf_service.py`: Generación de documentos PDF a partir de plantillas HTML.

Esta capa orquesta las operaciones entre repositorios, aplica reglas de negocio y gestiona transacciones complejas.

**Capa de repositorio (Acceso a datos):**
Situada en `app/repositories/`, esta capa abstrae el acceso a la base de datos mediante el patrón Repository:
- `user_repo.py`: Consultas relacionadas con usuarios.
- `chat_repo.py`: Operaciones de persistencia de conversaciones.
- `message_repo.py`: Gestión de mensajes en base de datos.

Los repositorios utilizan SQLAlchemy para construir consultas y nunca contienen lógica de negocio, únicamente operaciones de acceso a datos.

**Capa de modelos (Esquema de base de datos):**
Definida en `app/models/`, contiene las entidades del dominio mapeadas con SQLAlchemy ORM:
- `user.py`: Modelo de usuario con campos de identificación y autenticación.
- `chat.py`: Modelo de conversación con estado, timestamps y relaciones.
- `message.py`: Modelo de mensaje con contenido, emisor y marca temporal.

**Capa de configuración (Core):**
Localizada en `app/core/`, contiene módulos transversales:
- `config.py`: Gestión de configuración mediante variables de entorno.
- `database.py`: Configuración de conexión a base de datos y sesiones SQLAlchemy.
- `security.py`: Funciones de seguridad (hashing, generación de tokens JWT).
- `exceptions.py`: Manejadores globales de excepciones para garantizar respuestas consistentes.

### 4.2. Descripción de la arquitectura frontend

El frontend está organizado siguiendo las convenciones de Vue.js 3 con Composition API:

**Componentes (`src/components/`):**
Vistas y componentes reutilizables que implementan la interfaz de usuario:
- `LoginView.vue`: Pantalla de inicio de sesión.
- `RegisterView.vue`: Formulario de registro de nuevos usuarios.
- `HomeView.vue`: Vista principal tras el login.
- `ChatView.vue`: Interfaz de conversación con la inteligencia artificial.
- `ConversationView.vue`: Vista de historial y gestión de conversaciones.
- `parts/`: Componentes reutilizables más pequeños (header, footer, sidebar, etc.).

**Composables (`src/composables/`):**
Funciones reutilizables que encapsulan lógica reactiva según el patrón Composition API:
- `useChatView.js`: Lógica de gestión del chat activo.
- `useConversationView.js`: Gestión del historial de conversaciones.
- `useLoginView.js`: Lógica de formulario de login.
- `useRegisterView.js`: Lógica de formulario de registro.

Los composables mantienen el estado reactivo, coordinan peticiones al backend y manejan eventos de interfaz.

**Servicios (`src/services/`):**
Capa de abstracción para comunicación con el backend:
- `api.js`: Configuración de Axios con interceptores para tokens JWT.
- `authService.js`: Funciones de autenticación (login, register, logout).
- `chatService.js`: Operaciones sobre chats (crear, listar, eliminar, obtener mensajes).
- `alertService.js`: Utilidades para mostrar notificaciones con SweetAlert2.
- `chatState.js`: Gestión de estado global del chat activo.

**Enrutamiento (`src/router/`):**
Configuración de Vue Router con rutas protegidas mediante guards de autenticación.

**Utilidades (`src/utils/`):**
Funciones auxiliares como procesamiento de mensajes en formato Markdown.

**Assets (`src/assets/`):**
Recursos estáticos como estilos CSS/SCSS e imágenes.

### 4.3. Separación de responsabilidades

El sistema aplica estrictamente el principio de separación de responsabilidades:

- **Frontend:** Presentación, validación básica de formularios y gestión de estado de interfaz.
- **Backend:** Lógica de negocio, validación de datos, autenticación, autorización, persistencia y coordinación con servicios externos.
- **Base de datos:** Almacenamiento persistente de información estructurada.
- **Servicios externos:** Procesamiento de lenguaje natural mediante modelos de inteligencia artificial.

Esta separación permite modificar, escalar o sustituir componentes sin afectar al resto del sistema.

### 4.4. Diagrama conceptual explicado en texto

El flujo completo del sistema puede describirse de la siguiente manera:

1. El usuario interactúa con la interfaz Vue.js en su navegador.
2. La interfaz realiza peticiones HTTP al backend mediante Axios.
3. El backend FastAPI recibe la petición en la capa de API y valida los datos de entrada.
4. La petición se delega a la capa de servicios, donde se aplica la lógica de negocio.
5. Si es necesario consultar o persistir datos, el servicio invoca al repositorio correspondiente.
6. El repositorio ejecuta consultas SQL a través de SQLAlchemy contra la base de datos MySQL.
7. En el caso de interacción con IA, el servicio de Bedrock construye un contexto conversacional y envía una petición a AWS Bedrock.
8. AWS Bedrock procesa la petición con el modelo Amazon Nova y devuelve una respuesta generada.
9. El servicio procesa la respuesta, la almacena en base de datos si procede y la devuelve al controlador.
10. El controlador construye una respuesta HTTP con formato JSON y la envía al cliente.
11. El frontend recibe la respuesta, actualiza el estado reactivo y renderiza la nueva información en la interfaz.

---

## 5. BACKEND

### 5.1. Estructura general del proyecto

El código del backend está organizado en el directorio `backend_Proyecto_IA_generalitat/` con la siguiente estructura principal:

- `app/`: Código fuente de la aplicación.
- `alembic/`: Configuración y scripts de migraciones de base de datos.
- `tests/`: Suite de pruebas unitarias e integración.
- `docs/`: Documentación técnica del backend.
- `db/`: Scripts SQL de inicialización.
- `docker-compose.yml`: Orquestación de contenedores.
- `Dockerfile`: Definición de imagen Docker del backend.
- `requirements.txt`: Dependencias Python de producción.
- `requirements-dev.txt`: Dependencias de desarrollo y testing.

### 5.2. Organización por capas

La aplicación backend implementa una arquitectura en capas con separación clara de responsabilidades:

**Controladores (`app/api/v1/`):**
Reciben peticiones HTTP, validan esquemas con Pydantic y delegan la ejecución a servicios. No contienen lógica de negocio.

**Servicios (`app/services/`):**
Implementan toda la lógica de negocio del sistema. Coordinan repositorios, aplican reglas de dominio, gestionan transacciones y se comunican con servicios externos.

**Repositorios (`app/repositories/`):**
Abstraen el acceso a datos. Encapsulan consultas SQL mediante SQLAlchemy y exponen métodos de alto nivel para operaciones CRUD.

**Modelos (`app/models/`):**
Definen el esquema de base de datos mediante clases SQLAlchemy. Establecen relaciones entre tablas y restricciones de integridad.

**Esquemas (`app/schemas/`):**
Definen modelos Pydantic para validación de datos de entrada y salida de la API. Garantizan que los datos cumplan con el formato esperado antes de procesarlos.

### 5.3. Gestión de usuarios y autenticación

El sistema implementa un mecanismo de autenticación basado en tokens JWT (JSON Web Tokens):

**Registro de usuarios:**
Los nuevos usuarios proporcionan nombre, correo electrónico y contraseña. El sistema valida que el correo no esté registrado previamente, hashea la contraseña mediante bcrypt y crea un nuevo registro en la tabla `users`.

**Inicio de sesión:**
El usuario proporciona correo y contraseña. El sistema verifica las credenciales comparando el hash almacenado con la contraseña proporcionada. Si la autenticación es exitosa, genera un token JWT firmado que contiene el ID del usuario y una fecha de expiración.

**Protección de endpoints:**
Los endpoints protegidos requieren incluir el token JWT en la cabecera `Authorization` de las peticiones HTTP. El sistema valida la firma del token, comprueba que no haya expirado y extrae el ID del usuario para identificarlo en las operaciones posteriores.

**Seguridad de contraseñas:**
Las contraseñas se almacenan hasheadas mediante bcrypt con factor de coste elevado, lo que dificulta ataques de fuerza bruta incluso en caso de filtración de base de datos.

### 5.4. Endpoints principales

El sistema expone los siguientes grupos de endpoints:

#### 📡 API REST Endpoints

| Grupo | Método | Ruta | Descripción | Auth |
|-------|--------|------|-------------|------|
| **Autenticación** | POST | `/api/v1/auth/register` | Registro de nuevos usuarios | ❌ |
| | POST | `/api/v1/auth/login` | Autenticación y obtención de token JWT | ❌ |
| **Gestión de Chats** | GET | `/api/v1/chats` | Lista todas las conversaciones del usuario | ✅ |
| | POST | `/api/v1/chats` | Crea una nueva conversación vacía | ✅ |
| | GET | `/api/v1/chats/{chat_id}` | Obtiene detalles de una conversación | ✅ |
| | PUT | `/api/v1/chats/{chat_id}` | Actualiza propiedades (título, etc.) | ✅ |
| | DELETE | `/api/v1/chats/{chat_id}` | Elimina conversación y mensajes | ✅ |
| **Mensajes** | GET | `/api/v1/messages/{chat_id}` | Obtiene mensajes ordenados cronológicamente | ✅ |
| | POST | `/api/v1/messages` | Crea nuevo mensaje (uso interno) | ✅ |
| **Inteligencia Artificial** | POST | `/api/v1/ai/initialize` | Inicializa conversación con mensaje de bienvenida | ✅ |
| | POST | `/api/v1/ai/reply` | Envía mensaje y obtiene respuesta de IA | ✅ |
| | POST | `/api/v1/ai/finalize` | Finaliza conversación y genera informe | ✅ |
| | GET | `/api/v1/ai/pdf/{chat_id}` | Descarga informe PDF de evaluación | ✅ |
| **Sistema** | GET | `/health` | Verificación del estado del servicio | ❌ |

> **Nota:** Los endpoints marcados con ✅ requieren autenticación mediante token JWT en la cabecera `Authorization`.

### 5.5. Seguridad y control de acceso

El backend implementa múltiples capas de seguridad:

**Autenticación JWT:**
Todos los endpoints protegidos validan la presencia y validez del token. Los tokens tienen una duración limitada (configurable, típicamente 24 horas) para reducir el riesgo en caso de interceptación.

**Autorización por usuario:**
Cada operación sobre chats o mensajes verifica que el recurso pertenezca al usuario autenticado. Un usuario no puede acceder a conversaciones de otros usuarios.

**Validación de entrada:**
Todos los datos de entrada se validan mediante esquemas Pydantic antes de procesarse. Esto previene inyección de código malicioso y garantiza la integridad de los datos.

**Sanitización anti-prompt-injection:**
El servicio de Bedrock implementa filtros de entrada que detectan y bloquean intentos de manipular el comportamiento de la IA mediante instrucciones maliciosas embebidas en los mensajes del usuario.

**Rate limiting:**
Se aplican límites de tasa en endpoints críticos (como los de IA) para prevenir abuso de recursos y ataques de denegación de servicio.

**CORS configurado:**
El middleware CORS permite peticiones únicamente desde orígenes específicos configurados (frontend conocido), previniendo ataques desde sitios maliciosos.

**Hashing de contraseñas:**
Las contraseñas nunca se almacenan en texto plano. Se utiliza bcrypt con alto factor de coste.

### 5.6. Gestión de errores y validaciones

El sistema implementa un manejo de errores robusto y consistente:

**Validación automática:**
FastAPI y Pydantic validan automáticamente los datos de entrada. Si los datos no cumplen con el esquema esperado, se devuelve un error HTTP 422 con detalles de los campos incorrectos.

**Excepciones de negocio:**
El código lanza excepciones específicas cuando se detectan situaciones anómalas (ej: usuario no encontrado, chat no pertenece al usuario, conversación ya finalizada).

**Manejadores globales:**
Se han definido manejadores de excepciones globales que capturan errores no controlados y los transforman en respuestas HTTP coherentes con información útil para el cliente, sin exponer detalles internos del sistema.

**Logging estructurado:**
Todos los errores significativos se registran en logs para facilitar la depuración y el monitoreo del sistema.

**Respuestas consistentes:**
Todas las respuestas de error siguen el mismo formato JSON con campos `detail` o `message`, facilitando el manejo en el frontend.

---

## 6. FRONTEND

### 6.1. Estructura general del proyecto

El código del frontend está organizado en el directorio `frontend_Proyecto_IA_generalitat/` con la siguiente estructura:

- `src/`: Código fuente de la aplicación Vue.js.
- `public/`: Recursos estáticos públicos.
- `docs/`: Documentación generada con JSDoc.
- `package.json`: Definición de dependencias y scripts npm.
- `vite.config.js`: Configuración de Vite.
- `Dockerfile`: Definición de imagen Docker con Nginx para producción.

### 6.2. Pantallas principales

La aplicación consta de las siguientes vistas principales:

**Vista de registro (`RegisterView.vue`):**
Formulario donde los nuevos usuarios introducen nombre, correo electrónico y contraseña para crear una cuenta. Incluye validación en tiempo real y mensajes de error claros.

**Vista de inicio de sesión (`LoginView.vue`):**
Formulario de autenticación con campos de correo y contraseña. Tras autenticarse correctamente, almacena el token JWT en localStorage y redirige al usuario a la vista principal.

**Vista principal (`HomeView.vue`):**
Pantalla de bienvenida tras el login que muestra opciones para iniciar una nueva entrevista o acceder al historial de conversaciones.

**Vista de chat (`ChatView.vue`):**
Interfaz de conversación con la inteligencia artificial. Presenta un área de mensajes con scroll automático, campo de entrada de texto y barra lateral con historial de conversaciones. Permite enviar mensajes, visualizar respuestas de la IA en tiempo real y gestionar el estado de la conversación (finalizar, descargar informe).

**Vista de historial de conversaciones (`ConversationView.vue`):**
Listado de todas las entrevistas previas del usuario con información de fecha, título y estado. Permite renombrar, eliminar o reanudar conversaciones.

### 6.3. Flujo de navegación

El sistema implementa las siguientes rutas protegidas mediante Vue Router:

1. `/login`: Acceso público. Punto de entrada para usuarios no autenticados.
2. `/register`: Acceso público. Creación de nuevas cuentas.
3. `/`: Ruta protegida. Redirige al chat activo o muestra pantalla de bienvenida.
4. `/chat`: Ruta protegida. Interfaz de conversación con Evalio.
5. `/conversations`: Ruta protegida. Gestión del historial de entrevistas.

Las rutas protegidas verifican la presencia de un token JWT válido antes de permitir el acceso. Si el usuario no está autenticado, se le redirige automáticamente a la vista de login.

### 6.4. Comunicación con el backend

La comunicación con el backend se realiza mediante Axios, un cliente HTTP basado en promesas:

**Configuración centralizada:**
El módulo `api.js` configura una instancia de Axios con la URL base del backend y define interceptores que añaden automáticamente el token JWT a todas las peticiones protegidas.

**Servicios especializados:**
Cada recurso del backend tiene un módulo de servicio asociado en el frontend:
- `authService.js`: Llamadas de login y registro.
- `chatService.js`: Operaciones sobre conversaciones y mensajes.

Estos servicios encapsulan las peticiones HTTP y exponen funciones asíncronas que devuelven promesas, simplificando el manejo de respuestas y errores en los componentes.

**Gestión de errores:**
Los interceptores de Axios detectan errores de autenticación (HTTP 401) y redirigen automáticamente al login. Otros errores se capturan en los componentes y se presentan al usuario mediante notificaciones visuales.

### 6.5. Gestión del estado y datos

El frontend utiliza múltiples estrategias de gestión de estado:

**Estado local reactivo:**
Los composables y componentes Vue mantienen estado reactivo mediante `ref` y `reactive`, siguiendo el patrón Composition API. Esto permite que la interfaz se actualice automáticamente cuando cambian los datos.

**Almacenamiento persistente:**
El token JWT se almacena en `localStorage` del navegador para mantener la sesión activa entre recargas de página. El ID del chat activo también se persiste para permitir continuar conversaciones interrumpidas.

**Estado compartido:**
El módulo `chatState.js` implementa un estado reactivo global compartido entre componentes mediante el patrón Singleton, permitiendo sincronizar información del chat activo sin necesidad de un store complejo como Vuex.

**Sincronización con servidor:**
El frontend no mantiene caché de datos del backend. Cada vez que se accede a una vista, se realiza una petición al servidor para obtener los datos más recientes, garantizando consistencia.

### 6.6. Criterios de usabilidad y accesibilidad

El diseño de la interfaz sigue principios de usabilidad:

**Diseño responsivo:**
La interfaz se adapta a diferentes tamaños de pantalla mediante Bootstrap y media queries CSS, garantizando una experiencia óptima en dispositivos móviles, tablets y ordenadores de escritorio.

**Feedback visual:**
Todas las acciones del usuario generan feedback inmediato: estados de carga durante peticiones asíncronas, confirmaciones de acciones exitosas y mensajes de error claros y accionables.

**Navegación intuitiva:**
El flujo de navegación es lineal y coherente. Los elementos interactivos tienen affordances claras (botones claramente identificables, enlaces subrayados, iconos descriptivos).

**Mensajes claros:**
Los textos de interfaz utilizan lenguaje sencillo y directo. Los errores se presentan en lenguaje natural con indicaciones sobre cómo solucionarlos.

**Accesibilidad básica:**
Se utilizan elementos HTML semánticos, etiquetas descriptivas en formularios y contraste de color adecuado para facilitar el uso con lectores de pantalla.

---

## 7. BASE DE DATOS

### 7.1. Tipo de base de datos

El sistema utiliza MySQL 8.0, un sistema gestor de bases de datos relacional de código abierto ampliamente utilizado en aplicaciones web. Se eligió por su estabilidad, rendimiento, compatibilidad con SQLAlchemy y amplio soporte comunitario.

### 7.2. Entidades principales

El esquema de base de datos consta de tres entidades principales:

**Tabla users:**
Almacena la información de los usuarios registrados en el sistema.
- `id_usuario`: Identificador único autoincrementable (clave primaria).
- `email`: Dirección de correo electrónico única.
- `password_hash`: Contraseña hasheada con bcrypt.
- `nombre`: Nombre completo del usuario.
- `created_at`: Fecha y hora de registro.

**Tabla chats:**
Representa las conversaciones de entrevista entre usuarios y la IA.
- `id_chat`: Identificador único autoincrementable (clave primaria).
- `id_usuario`: Referencia al usuario propietario (clave foránea).
- `title`: Título descriptivo de la conversación.
- `status`: Estado de la conversación (`active` o `completed`).
- `created_at`: Fecha y hora de creación.
- `last_message_at`: Timestamp del último mensaje.
- `completed_at`: Fecha y hora de finalización (null si está activo).

**Tabla messages:**
Almacena los mensajes individuales dentro de cada conversación.
- `id_message`: Identificador único autoincrementable (clave primaria).
- `id_chat`: Referencia a la conversación (clave foránea).
- `sender`: Emisor del mensaje (`user` o `assistant`).
- `contenido`: Texto del mensaje.
- `created_at`: Fecha y hora de envío.

### 7.3. Relaciones generales

El esquema implementa las siguientes relaciones:

**Usuario - Chats (1:N):**
Un usuario puede tener múltiples conversaciones. Cada conversación pertenece a un único usuario. Esta relación se implementa mediante clave foránea `id_usuario` en la tabla `chats` con restricción de integridad referencial.

**Chat - Mensajes (1:N):**
Una conversación contiene múltiples mensajes. Cada mensaje pertenece a una única conversación. Relación implementada mediante clave foránea `id_chat` en la tabla `messages`.

**Eliminación en cascada:**
Cuando se elimina un usuario, se eliminan automáticamente todos sus chats y mensajes asociados. Cuando se elimina un chat, se eliminan automáticamente todos sus mensajes. Esto garantiza la integridad referencial del sistema.

### 7.4. Justificación del diseño

El diseño relacional es apropiado para este sistema por las siguientes razones:

**Integridad referencial:**
Las relaciones entre usuarios, chats y mensajes garantizan la consistencia de los datos. No pueden existir conversaciones huérfanas ni mensajes sin conversación asociada.

**Consultas eficientes:**
Las consultas más frecuentes (listar chats de un usuario, obtener mensajes de un chat) se benefician de índices en claves foráneas que optimizan el rendimiento.

**Escalabilidad controlada:**
Aunque el volumen de mensajes puede crecer, el diseño permite particionar datos por usuario o implementar estrategias de archivado si es necesario en el futuro.

**Simplicidad:**
El esquema es sencillo y fácil de entender, facilitando el mantenimiento y la evolución del sistema.

---

## 8. SEGURIDAD

### 8.1. Autenticación y autorización

El sistema implementa un esquema de autenticación robusto basado en JWT:

**Autenticación:**
Los usuarios deben proporcionar credenciales válidas (correo y contraseña) para acceder al sistema. Tras verificar las credenciales, se genera un token JWT firmado digitalmente que identifica al usuario y tiene una fecha de expiración.

**Autorización:**
Cada petición a endpoints protegidos debe incluir el token JWT. El sistema valida la firma, verifica que no haya expirado y extrae el ID del usuario. Las operaciones sobre recursos (chats, mensajes) comprueban que el usuario autenticado sea el propietario del recurso antes de permitir el acceso o modificación.

**Separación de privilegios:**
Un usuario solo puede acceder a sus propias conversaciones y mensajes. El sistema previene accesos no autorizados verificando la propiedad de cada recurso antes de procesarlo.

### 8.2. Protección de datos

**Hashing de contraseñas:**
Las contraseñas se almacenan hasheadas con bcrypt, un algoritmo diseñado específicamente para este propósito con alto coste computacional que dificulta ataques de fuerza bruta.

**Comunicación segura:**
En producción, el sistema debe configurarse para utilizar HTTPS, cifrando toda la comunicación entre cliente y servidor para prevenir interceptación de credenciales y tokens.

**Gestión de sesiones:**
Los tokens JWT tienen duración limitada, reduciendo la ventana de oportunidad en caso de robo de token. El frontend almacena el token en localStorage, que es accesible únicamente desde el mismo dominio.

**Validación de datos:**
Todos los datos de entrada se validan estrictamente antes de procesarse o almacenarse, previniendo inyección de código SQL, XSS y otros vectores de ataque comunes.

### 8.3. Medidas básicas de seguridad aplicadas

**CORS restrictivo:**
El middleware CORS está configurado para aceptar únicamente peticiones desde el dominio del frontend conocido, previniendo ataques desde sitios maliciosos.

**Rate limiting:**
Los endpoints críticos (especialmente los de IA) tienen límites de tasa que previenen abuso de recursos y ataques de denegación de servicio distribuido (DDoS).

**Sanitización anti-injection:**
El sistema implementa filtros que detectan y bloquean intentos de manipular el comportamiento de la IA mediante técnicas de prompt injection.

**Manejo seguro de excepciones:**
Los errores internos no exponen información sensible del sistema. Los mensajes de error visibles para el usuario son genéricos y no revelan detalles de implementación.

**Separación de secretos:**
Las credenciales sensibles (claves de AWS, secreto JWT, contraseña de base de datos) se gestionan mediante variables de entorno, nunca en código fuente.

**Actualización de dependencias:**
El proyecto utiliza versiones actualizadas de todas las librerías con parches de seguridad conocidos aplicados.

---

## 9. DESPLIEGUE Y EJECUCIÓN

### 9.1. Entorno de desarrollo

El proyecto está preparado para ejecutarse en entornos de desarrollo local con las siguientes características:

**Backend:**
- Python 3.11 o superior instalado.
- Entorno virtual Python (venv o virtualenv).
- MySQL 8.0 ejecutándose localmente o mediante Docker.
- Variables de entorno configuradas en archivo `.env`.

**Frontend:**
- Node.js versión 18 o superior.
- pnpm instalado globalmente.
- Variables de entorno configuradas en archivo `.env`.

### 9.2. Requisitos para ejecutar el proyecto

**Requisitos mínimos del sistema:**
- Sistema operativo: Windows 10/11, macOS 10.15+, o distribución Linux moderna.
- RAM: 4 GB mínimo (8 GB recomendado).
- Espacio en disco: 2 GB libres.
- Conexión a internet para instalación de dependencias y comunicación con AWS Bedrock.

**Software necesario:**
- Docker Desktop (recomendado) o instalación manual de Python 3.11, Node.js 18 y MySQL 8.0.
- Git para control de versiones.

### 9.3. Variables de entorno

#### 🔧 Configuración del Backend

Crear archivo `.env` en el directorio del backend:

```bash
# Configuración de Base de Datos
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_bd

# Seguridad JWT
SECRET_KEY=clave_secreta_para_jwt_muy_larga_y_aleatoria
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Credenciales AWS
AWS_ACCESS_KEY_ID=tu_access_key_aws
AWS_SECRET_ACCESS_KEY=tu_secret_key_aws
AWS_REGION=us-east-1

# Modelo de IA
BEDROCK_MODEL_ID=amazon.nova-micro-v1:0
```

#### 🌐 Configuración del Frontend

Crear archivo `.env` en el directorio del frontend:

```bash
# URL del Backend
VITE_API_BASE_URL=http://localhost:8000
```

> **⚠️ Requisito importante:** Las claves de AWS requieren permisos de acceso a **AWS Bedrock** (servicio Amazon Nova). Configurar estos permisos en la consola de IAM de AWS.

### 9.4. Despliegue en local con Docker

**Opción recomendada para desarrollo y pruebas:**

1. Clonar el repositorio y situarse en el directorio del backend.
2. Crear archivo `.env` con las variables de entorno necesarias.
3. Ejecutar `docker-compose up --build` en el directorio del backend.
4. Aplicar migraciones de base de datos: `docker-compose exec backend alembic upgrade head`.
5. Situarse en el directorio del frontend y crear archivo `.env`.
6. Ejecutar `pnpm install` para instalar dependencias.
7. Ejecutar `pnpm dev` para iniciar el servidor de desarrollo.

El backend estará disponible en `http://localhost:8000` y el frontend en `http://localhost:5173`.

**Ejecución sin Docker:**

Si no se utiliza Docker, es necesario instalar y configurar manualmente Python, Node.js y MySQL, crear bases de datos, instalar dependencias con `pip install -r requirements.txt` y `pnpm install`, y ejecutar el backend con `uvicorn app.main:app --reload` y el frontend con `pnpm dev`.

### 9.5. Despliegue en producción

Para despliegue en producción se recomienda:

**Backend:**
- Servidor con sistema operativo Linux (Ubuntu Server, Debian, CentOS).
- Contenedor Docker o instalación directa con servicio systemd.
- Servidor web Nginx o similar como proxy inverso para servir peticiones HTTPS.
- Configuración de certificados SSL/TLS (Let's Encrypt).
- Base de datos MySQL en servidor dedicado o servicio gestionado (AWS RDS, Google Cloud SQL).

**Frontend:**
- Compilación de producción mediante `pnpm build`.
- Servir archivos estáticos mediante Nginx, Apache o servicio CDN.
- Contenedor Docker con imagen optimizada de Nginx.

**Infraestructura recomendada:**
- Servidores virtuales o contenedores gestionados (AWS EC2, Google Compute Engine, Azure VMs).
- Servicios gestionados de base de datos para mayor disponibilidad.
- Configuración de copias de seguridad automáticas de la base de datos.
- Monitorización de logs y métricas de rendimiento.

---

## 10. PRUEBAS

### 10.1. Estrategia de pruebas

El proyecto implementa una estrategia de pruebas multinivel centrada en garantizar la calidad y estabilidad del código:

**Pruebas unitarias:**
Verifican el funcionamiento correcto de funciones y métodos individuales de forma aislada. Se centran en la lógica de servicios y repositorios.

**Pruebas de integración:**
Validan la interacción entre diferentes capas del sistema (API - Servicio - Repositorio - Base de datos). Utilizan una base de datos en memoria (SQLite) para ejecutar pruebas sin afectar los datos reales.

**Pruebas de API:**
Comprueban los endpoints REST de forma completa, simulando peticiones HTTP reales y verificando respuestas, códigos de estado y formatos de datos.

### 10.2. Tipos de pruebas realizadas

**Backend:**
El directorio `tests/` contiene pruebas implementadas con pytest:
- `test_auth.py`: Pruebas de registro, login, validación de tokens y control de acceso.
- `test_chats.py`: Pruebas de creación, listado, actualización y eliminación de conversaciones.

Las pruebas utilizan fixtures definidas en `conftest.py` que configuran un entorno de testing aislado con base de datos en memoria y cliente de pruebas FastAPI.

**Frontend:**
Aunque el proyecto está documentado con JSDoc, no se han implementado pruebas automatizadas de frontend en el alcance actual del proyecto.

### 10.3. Validación del funcionamiento

La validación del funcionamiento se realiza mediante:

**Ejecución de suite de pruebas:**
Las pruebas se ejecutan con el comando `pytest` desde el directorio del backend. Todos los tests deben pasar correctamente antes de desplegar cambios.

**Pruebas manuales:**
Se realizan pruebas exploratorias manuales de la interfaz de usuario verificando flujos completos de uso: registro, login, creación de conversaciones, interacción con IA, generación de informes y gestión de historial.

**Validación de endpoints:**
La documentación automática Swagger UI (`/docs`) permite probar manualmente todos los endpoints de la API de forma interactiva.

**Revisión de logs:**
Durante el desarrollo se revisan logs del sistema para detectar excepciones, errores de validación o comportamientos anómalos.

---

## 11. LIMITACIONES ACTUALES

### 11.1. Restricciones técnicas

El sistema presenta las siguientes limitaciones técnicas identificadas:

| Limitación | Descripción | Impacto |
|------------|-------------|----------|
| ⚠️ **Dependencia de servicios externos** | Funcionamiento dependiente de AWS Bedrock | Si el servicio no está disponible o se agotan cuotas, la IA no funciona |
| 🌍 **Sin soporte multiidioma** | Interfaz y mensajes únicamente en español | Limita el uso a usuarios hispanohablantes |
| 📊 **Escalabilidad limitada de historial** | Carga completa sin paginación | Afecta rendimiento en conversaciones muy extensas (>100 mensajes) |
| ⏱️ **Generación de PDF síncrona** | Proceso bloqueante | Tiempos de espera elevados en conversaciones largas |
| 📎 **Sin archivos adjuntos** | Solo mensajes de texto | No permite enviar currículums, portfolios o documentos |

### 11.2. Funcionalidades no implementadas

Las siguientes funcionalidades quedan fuera del alcance actual:

**Roles diferenciados:**
No existe distinción entre estudiantes, profesores o administradores. Todos los usuarios tienen los mismos permisos.

**Análisis estadístico:**
No se generan métricas agregadas de desempeño, progreso temporal ni comparaciones entre usuarios.

**Notificaciones:**
El sistema no envía notificaciones por correo electrónico ni otros canales.

**Edición de mensajes:**
Una vez enviado, un mensaje no puede editarse ni eliminarse individualmente.

**Exportación en otros formatos:**
Los informes solo se generan en PDF, sin opción de exportar a Word, Excel u otros formatos.

**Personalización de prompts:**
El prompt del sistema de la IA está fijado en el código. No existe interfaz administrativa para modificarlo.

**Historial de versiones:**
No se mantiene un registro de cambios en los datos (auditoría completa).

---

## 12. POSIBLES MEJORAS FUTURAS

### 12.1. Escalabilidad

**Paginación de mensajes:**
Implementar carga perezosa de mensajes antiguos en conversaciones largas para mejorar el rendimiento inicial de carga.

**Caché de respuestas:**
Implementar caché Redis para respuestas frecuentes o contextos de conversación, reduciendo latencia y llamadas a servicios externos.

**Procesamiento asíncrono:**
Migrar la generación de PDFs a un sistema de colas (Celery + RabbitMQ) para procesamiento en segundo plano sin bloquear peticiones HTTP.

**Balanceo de carga:**
Implementar múltiples instancias del backend con balanceador de carga (Nginx, HAProxy) para soportar mayor número de usuarios concurrentes.

### 12.2. Nuevas funcionalidades

**Sistema de roles:**
Implementar perfiles diferenciados (estudiante, profesor, administrador) con permisos específicos. Los profesores podrían supervisar el progreso de sus estudiantes.

**Dashboard de análisis:**
Crear panel de control con métricas de uso: número de entrevistas realizadas, tiempo promedio de conversación, temas más consultados, puntuaciones medias.

**Exportación múltiple formato:**
Permitir descargar informes en Word, Markdown y envío directo por correo electrónico.

**Banco de preguntas personalizable:**
Interfaz administrativa para que profesores puedan definir bancos de preguntas específicos o modificar el comportamiento de la IA según módulos formativos concretos.

**Modo colaborativo:**
Permitir que profesores puedan observar entrevistas en tiempo real o revisar transcripciones completas de entrevistas de estudiantes.

**Gamificación:**
Implementar sistema de logros, insignias o puntuaciones para motivar la práctica continua.

**Integración con LMS:**
Permitir integración con plataformas educativas (Moodle, Google Classroom) mediante estándares LTI.

### 12.3. Optimización técnica

**Compresión de respuestas:**
Implementar compresión Gzip/Brotli en respuestas HTTP para reducir ancho de banda.

**Optimización de imágenes:**
Implementar lazy loading y formatos modernos (WebP, AVIF) para recursos gráficos del frontend.

**Service Workers:**
Implementar PWA (Progressive Web App) con funcionamiento offline limitado y caché de recursos estáticos.

**Testing automatizado completo:**
Ampliar cobertura de tests incluyendo tests end-to-end con herramientas como Playwright o Cypress.

**Internacionalización:**
Implementar sistema i18n para soportar múltiples idiomas en interfaz y mensajes de IA.

**Monitorización avanzada:**
Integrar herramientas de observabilidad (Prometheus, Grafana, Sentry) para detectar errores en producción y analizar rendimiento.

**Migraciones automáticas:**
Configurar pipeline CI/CD con ejecución automática de tests y despliegue continuo.

---

## 13. CONCLUSIÓN

### 13.1. Valor del proyecto

AulaEntrevistas representa una solución tecnológica innovadora al problema de la preparación para entrevistas laborales del alumnado de Formación Profesional. El proyecto demuestra cómo la inteligencia artificial puede aplicarse de forma práctica en contextos educativos para mejorar la empleabilidad de los estudiantes.

El valor principal del sistema radica en su capacidad para proporcionar experiencias de práctica ilimitadas, personalizadas y sin coste humano adicional para los centros educativos. Cada estudiante puede realizar tantas entrevistas simuladas como necesite, en cualquier momento y lugar, recibiendo feedback inmediato y constructivo que le permita mejorar progresivamente.

Desde el punto de vista institucional, el proyecto ofrece una herramienta escalable que puede beneficiar simultáneamente a miles de estudiantes sin requerir recursos humanos proporcionales, optimizando el uso de recursos públicos y democratizando el acceso a servicios de orientación laboral de calidad.

### 13.2. Aprendizajes técnicos

El desarrollo de este proyecto ha permitido aplicar e integrar un conjunto amplio de tecnologías modernas y buenas prácticas de ingeniería de software:

**Arquitectura en capas:**
La separación estricta de responsabilidades entre controladores, servicios y repositorios ha demostrado su valor facilitando el mantenimiento, testing y evolución del código.

**Integración con servicios de IA:**
La implementación de comunicación con AWS Bedrock ha requerido comprender conceptos de gestión de contexto conversacional, limitaciones de tokens y técnicas de prompt engineering aplicadas.

**Seguridad en aplicaciones web:**
El proyecto ha integrado múltiples capas de seguridad: autenticación JWT, hashing de contraseñas, validación de entrada, protección contra prompt injection y rate limiting.

**Desarrollo frontend moderno:**
El uso de Vue.js 3 con Composition API ha permitido crear una interfaz reactiva, modular y mantenible, aprovechando las capacidades de los frameworks modernos.

**Contenerización:**
Docker y Docker Compose han simplificado significativamente el despliegue y la configuración del entorno de desarrollo, garantizando consistencia entre equipos.

**Gestión de base de datos:**
El uso de SQLAlchemy como ORM y Alembic para migraciones ha demostrado ser una combinación potente para gestionar el esquema de base de datos de forma profesional y versionada.

### 13.3. Aplicabilidad real del sistema

El sistema desarrollado está preparado para su uso real en entornos educativos con las siguientes consideraciones:

**Viabilidad técnica:**
La arquitectura implementada es robusta y escalable para el contexto de centros educativos o servicios de la Generalitat. Puede soportar cientos de usuarios concurrentes con la infraestructura adecuada.

**Coste operativo:**
El principal coste operativo deriva del uso de AWS Bedrock, que se factura por tokens procesados. Para un uso moderado educativo, este coste es asumible. El resto de componentes pueden ejecutarse en infraestructura propia o servicios en la nube con costes predecibles.

**Integración institucional:**
El sistema puede integrarse en la infraestructura existente de centros educativos mediante Single Sign-On (SSO) o mediante integración con plataformas LMS existentes (desarrollo futuro).

**Impacto educativo:**
Las pruebas piloto indicarían que los estudiantes que utilizan el sistema mejoran su confianza en entrevistas reales y desarrollan mejor sus competencias de comunicación técnica.

**Cumplimiento normativo:**
El sistema debe adaptarse al cumplimiento de RGPD y normativa de protección de datos educativos, asegurando que los datos de estudiantes se tratan con las garantías legales requeridas.

En conclusión, AulaEntrevistas constituye una base sólida para una herramienta de orientación laboral tecnológica que puede generar un impacto real positivo en la empleabilidad del alumnado de Formación Profesional, demostrando la aplicabilidad práctica de la inteligencia artificial en contextos educativos.

---

**FIN DEL DOCUMENTO**
