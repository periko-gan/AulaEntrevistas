// update-creds.js
import clipboardy from 'clipboardy'
import fs from 'fs'
import path from 'path'

// 1. Leemos el portapapeles
const clipboardContent = clipboardy.readSync()

if (!clipboardContent.includes('aws_access_key_id')) {
  console.error('❌ Error: No detecto credenciales de AWS en tu portapapeles.')
  console.log('👉 Ve a Vocareum, copia el bloque "AWS CLI" e inténtalo de nuevo.')
  process.exit(1)
}

// 2. Parseamos las claves
const lines = clipboardContent.split('\n')
let envContent = ''

console.log('🔄 Procesando credenciales...')

lines.forEach((line) => {
  const cleanLine = line.trim()
  if (cleanLine.startsWith('aws_access_key_id')) {
    const val = cleanLine.split('=')[1]
    envContent += `VITE_AWS_ACCESS_KEY_ID=${val}\n`
  }
  if (cleanLine.startsWith('aws_secret_access_key')) {
    const val = cleanLine.split('=')[1]
    envContent += `VITE_AWS_SECRET_ACCESS_KEY=${val}\n`
  }
  if (cleanLine.startsWith('aws_session_token')) {
    const val = cleanLine.split('=')[1]
    envContent += `VITE_AWS_SESSION_TOKEN=${val}\n`
  }
})

// Añadimos la región (ajusta si tu lab usa us-west-2, etc.)
envContent += `VITE_AWS_REGION=us-east-1\n`

// 3. Escribimos en .env.local (este archivo es ignorado por git y tiene prioridad)
const envPath = path.resolve(process.cwd(), '.env.local')

try {
  // Leemos si había algo antes para no borrar otras variables tuyas (opcional)
  // Para simplificar, este script SOBRESCRIBE las credenciales de AWS
  fs.writeFileSync(envPath, envContent)

  console.log('✅ ¡Listo! Credenciales actualizadas en .env.local')
  console.log('📂 Variables generadas:')
  console.log(envContent)
  console.log(
    '⚠️  Si tu servidor de Vue está corriendo, Vite debería detectar el cambio automáticamente.',
  )
} catch (err) {
  console.error('❌ Error escribiendo el archivo:', err)
}
