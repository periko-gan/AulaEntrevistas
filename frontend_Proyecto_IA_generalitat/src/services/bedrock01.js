import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime';

// Configuración estándar de Vite para leer desde .env o .env.local
const accessKeyId = import.meta.env.VITE_AWS_ACCESS_KEY_ID;
const secretAccessKey = import.meta.env.VITE_AWS_SECRET_ACCESS_KEY;
const sessionToken = import.meta.env.VITE_AWS_SESSION_TOKEN;
const region = import.meta.env.VITE_AWS_REGION; // Leído desde .env

// CORRECCIÓN: Usamos un modelo de Cohere que espera la clave 'prompt'
const modelId = 'meta.llama3-70b-instruct-v1:0'

// Debug
console.log('--- DEBUG AWS ---');
console.log('Region:', region);
console.log('Model ID:', modelId);
console.log('AccessKey:', accessKeyId ? 'CARGADO' : 'NO CARGADO');
console.log('-----------------');

const client = new BedrockRuntimeClient({
  region: region,
  credentials: {
    accessKeyId: accessKeyId,
    secretAccessKey: secretAccessKey,
    sessionToken: sessionToken,
  },
});

export const invokeBedrock = async (prompt) => {
  try {
    // CORRECCIÓN: La estructura del payload para los modelos Cohere.
    const payload = {
      prompt: prompt,
      max_tokens: 1024,
      temperature: 0.7,
    };

    const command = new InvokeModelCommand({
      modelId: modelId,
      contentType: 'application/json',
      accept: 'application/json',
      body: JSON.stringify(payload),
    });

    const response = await client.send(command);
    const decodedResponseBody = new TextDecoder().decode(response.body);
    const responseBody = JSON.parse(decodedResponseBody);

    // La respuesta de Cohere tiene una estructura diferente.
    return responseBody.generations[0].text;
  } catch (error) {
    console.error('Error invocando Bedrock:', error);
    throw error;
  }
};
