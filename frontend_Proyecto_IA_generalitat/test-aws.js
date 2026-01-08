import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

// --- CONFIGURACIÓN MANUAL PARA PRUEBA ---
// Por favor, pega aquí tus credenciales directamente para probar.
// Si esto funciona, el problema es cómo Vite lee el archivo .env
const REGION = "us-east-1";
const ACCESS_KEY = 'ASIAXGT5W6N76ZMTY3W3'
const SECRET_KEY = 'olX7eCWG4HEPMyd3hPz46F90Kcdvh+MrfROYWDJI'
const SESSION_TOKEN =
  'IQoJb3JpZ2luX2VjEHgaCmV1LXNvdXRoLTIiRjBEAiAP2E7BKl6rP7GoYae0lipoWjeBYU4USoCG/T7dNe6GogIgJvVI05ST4DSWG7ix0tLS1FF6qtO5D5RMTX1RTskbbcQqkwMIyv//////////ARAAGgw0OTUyNTg2Mjg5OTEiDM28tq7pSx2dAdKoXCrnAqEVxF8mNw66+dm4E0DePRAci0whnnHLfUp/1J3NyEqfhyosWx33N592xZMvIrT8wImLU7UCFlZYdAK+EqqzXjQ2kA68p9ap3AOGt385ExRMiCeciAnX5J2LWppE3mxISG4qDcWPM/t8mTOUJycsxUO8u8TQs5NSeYGuokev62JhDuQe8ALS/D2dm6yly/FJzqAlY/5jBYh+rPvhFwwPMRDMAnTE0ICfI5fqgkkWTerYxg2a2gc7BquitTXlxnJV/Ms+fbCsSgtJOmAHuLgJ8KubXNhIN+uTjeYH4s3jv8ggqvtbVI22Lxym/BMrP72qu3AeZLAQ8AUB8uUpb/DNM2TDqkOtraM++qXT+m9c1XkbwxkhGwW8IQKuOMVwgIdaMacY/qpHfyaQdYbgebDsZ+S3+9AgbPZPoIOiB/YitGBw+03Rh6PODiSTCiUPb2REa+Yo1EGBKLKEEyIAKpJmsO/DvwKlIkCeMNuwm8oGOqUBmoSHXn0Vr7DbmMl3Umr96sqc4aASvbGRGy50jNwljnZJ2qHag5UpfUJ/e5tQ55OjkulWtHT7SL9KW9uC3qZQphoYXklHy8ovfQvYJkMIQXsmi9pUS73FeTgxbg5QDnw90a/xCPKHaEfYE6AocR+ynC3Lbc6qJUY9XvrZyp1qcnZMeNKZgXDUfAZNTw1e/G+HhnGxejibVW6SzfO8jiqdGjxWp4uj' // Déjalo vacío si no usas credenciales temporales

console.log("Iniciando prueba de conexión a AWS Bedrock...");

const client = new BedrockRuntimeClient({
    region: REGION,
    credentials: {
        accessKeyId: ACCESS_KEY,
        secretAccessKey: SECRET_KEY,
        sessionToken: SESSION_TOKEN || undefined,
    },
});

const run = async () => {
    try {
        const prompt = "Hola, ¿estás funcionando?";
        const payload = {
            anthropic_version: "bedrock-2023-05-31",
            max_tokens: 100,
            messages: [{ role: "user", content: [{ type: "text", text: prompt }] }]
        };

        const command = new InvokeModelCommand({
            modelId: "anthropic.claude-3-sonnet-20240229-v1:0",
            contentType: "application/json",
            accept: "application/json",
            body: JSON.stringify(payload),
        });

        console.log("Enviando solicitud...");
        const response = await client.send(command);
        console.log("¡ÉXITO! Conexión establecida correctamente.");

    } catch (error) {
        console.error("\n❌ ERROR DE CONEXIÓN:");
        console.error(error.name);
        console.error(error.message);

        if (error.name === 'UnrecognizedClientException') {
            console.log("\nPOSIBLE CAUSA: Las credenciales (Access Key / Secret Key) son incorrectas.");
        } else if (error.name === 'AccessDeniedException') {
            console.log("\nPOSIBLE CAUSA: Las credenciales son válidas, pero el usuario no tiene permisos para usar Bedrock o el modelo Claude 3.");
        }
    }
};

run();
