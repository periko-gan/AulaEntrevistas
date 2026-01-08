import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // Cargar variables de entorno
  const env = loadEnv(mode, process.cwd(), '')

  // --- DIAGNÓSTICO EN TERMINAL ---
  console.log("------------------------------------------------")
  console.log(" DIAGNÓSTICO DE VARIABLES DE ENTORNO (VITE) ")
  console.log("------------------------------------------------")
  console.log("VITE_AWS_REGION:", env.VITE_AWS_REGION ? "OK" : "FALTA")
  console.log("VITE_AWS_ACCESS_KEY_ID:", env.VITE_AWS_ACCESS_KEY_ID ? "OK (" + env.VITE_AWS_ACCESS_KEY_ID.substring(0,5) + "...)" : "FALTA")
  console.log("VITE_AWS_SECRET_ACCESS_KEY:", env.VITE_AWS_SECRET_ACCESS_KEY ? "OK" : "FALTA")
  console.log("VITE_AWS_SESSION_TOKEN:", env.VITE_AWS_SESSION_TOKEN ? "OK (Longitud: " + env.VITE_AWS_SESSION_TOKEN.length + ")" : "FALTA O VACÍO")

  // Verificar si existe sin el prefijo VITE_
  if (env.AWS_SESSION_TOKEN) {
    console.log("¡AVISO! Encontrada 'AWS_SESSION_TOKEN' pero falta el prefijo 'VITE_'. Renómbrala en .env.local")
  }
  console.log("------------------------------------------------")
  // -------------------------------

  return {
    base: command === 'build' ? './' : '/',
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'if-function', 'mixed-decls'],
          quietDeps: true,
        },
      },
    },
  }
})
