import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime';

// Configuración estándar de Vite para leer desde .env o .env.local
const accessKeyId = import.meta.env.VITE_AWS_ACCESS_KEY_ID;
const secretAccessKey = import.meta.env.VITE_AWS_SECRET_ACCESS_KEY;
const sessionToken = import.meta.env.VITE_AWS_SESSION_TOKEN;
const region = import.meta.env.VITE_AWS_REGION || 'us-east-1'; // us-east-1 como fallback

// Debug para ver qué está cogiendo (revisar consola del navegador)
console.log('--- DEBUG AWS ---');
console.log('Region:', region);
console.log('AccessKey:', accessKeyId ? `${accessKeyId.substring(0, 5)}...` : 'NO CARGADO');
console.log('SecretKey:', secretAccessKey ? 'CARGADO' : 'NO CARGADO');
console.log('SessionToken:', sessionToken ? 'CARGADO' : 'NO CARGADO');
console.log('-----------------');

if (!accessKeyId || !secretAccessKey || !sessionToken) {
  console.error(
    'ERROR: Faltan credenciales en el archivo .env.local. Asegúrate de que el archivo existe, tiene los nombres correctos (VITE_...) y reinicia el servidor.'
  );
}

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
    const modelId = 'amazon.titan-text-express-v1';

    const payload = {
      inputText: prompt,
      textGenerationConfig: {
        maxTokenCount: 1000,
        stopSequences: [],
        temperature: 0.7,
        topP: 1,
      },
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

    return responseBody.results[0].outputText;
  } catch (error) {
    console.error('Error invocando Bedrock:', error);
    throw error;
  }
};
