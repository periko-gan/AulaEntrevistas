import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime'

const HARDCODED_ACCESS_KEY = 'ASIAXGT5W6N7VHP2ASIO'
const HARDCODED_SECRET_KEY = 'GZjc1DEKnRDnOwbxKxbxkzH4+CNjkmVJS7fR4tcJ'
const HARDCODED_REGION = 'us-east-2'

//El token largo es OBLIGATORIO para claves que empiezan por ASIA...
const HARDCODED_SESSION_TOKEN =
  'IQoJb3JpZ2luX2VjEEEaCmV1LXNvdXRoLTIiRjBEAiBYa8CTlKCyrE8XJZvL6szI+ALduoynd17iyIAj89HBywIgKs1o63w46gXtrtYErCWfdPgS8oeh8KGiuKeBv/4009gqkwMIk///////////ARAAGgw0OTUyNTg2Mjg5OTEiDNpekZAmi6pJ1msysirnAv7aIjyzlYRXDpz25Z/6FvQP/WtOdbzvLJRRcnCxG8YRA/jHbb7mHYm0gDqfJJQJvpoFXqCjRcTBuLiypyLjyfmSXF7lDW+3DIggp5syowlV9WC9rlm0hXx0pmKH1bx9lyPRzCeY4fkGEuV5PLVxGoA9Z9ijB4uiZoFGQLoddq3OBMS3q2TERGxSh1k5gZCLNdES7jlVQrxuLqKyBZKabnp80o+zNwjYM58vP4Zklg4Nsm7M7ZmYHHG1NsmHQF/G5lSZUWjBop6EZeaaWaD8QumfISO+jR1yrXWvtYbK6tleDQSIfQEJ3Qr3+XCyei8fHjuISx+9itJv4sqNRKjL61Px5+nvEZsX4Jn2g/U957Pkm/mnp3Ulqtp//+OiFZt6fC7zIp8E9Uo8h2Z1J5miKASZC+82a3ZZHFssLExDo/s+Szd8QpwCNVat4bh2XPdaAMKyqmLD+KRtb25kJZi4aIdgAQJTLc6TMI3d/8oGOqUBOqk/0/MSgiZXTWmWZ6lRGV2l6+nZrjeNvXz9vftTXCSUou2pXTs7Vn2jp0ahQEVwF/hoDKmljS5cwHZ0OGjyMmYmfxSrE+8+01Si0qRfDTTpddPY90vcOSU0gL1+wdNmCw1v3gUklwwuBqOgiJFDFLCuF4B7XveM/pIFEDMO3hB+ixoQtNvcDYmP2wOlh5xoZHzUKuBHc36CqUFx5RVhzShqnLkM'

// 1. Selección de credenciales (Hardcoded VS .env)
const accessKeyId = HARDCODED_ACCESS_KEY || import.meta.env.VITE_AWS_ACCESS_KEY_ID
// const accessKeyId = import.meta.env.VITE_AWS_ACCESS_KEY_ID
const secretAccessKey = HARDCODED_SECRET_KEY || import.meta.env.VITE_AWS_SECRET_ACCESS_KEY
// const secretAccessKey = import.meta.env.VITE_AWS_SECRET_ACCESS_KEY
const sessionToken = HARDCODED_SESSION_TOKEN || import.meta.env.VITE_AWS_SESSION_TOKEN
// const sessionToken = import.meta.env.VITE_AWS_SESSION_TOKEN
const region = HARDCODED_REGION || import.meta.env.VITE_AWS_REGION
// const region = import.meta.env.VITE_AWS_REGION

// Debug para ver qué está cogiendo (revisar consola del navegador)
console.log('--- DEBUG AWS ---')
console.log('Region:', region)
console.log('AccessKey:', accessKeyId ? `${accessKeyId.substring(0, 5)}...` : 'FALTA')
console.log('SessionToken:', sessionToken ? 'PRESENTE (OK)' : 'FALTA (ERROR SI ES ASIA...)')
console.log('-----------------')

// 2. Inicializar Cliente
const client = new BedrockRuntimeClient({
  region: region,
  credentials: {
    accessKeyId: accessKeyId,
    secretAccessKey: secretAccessKey,
    sessionToken: sessionToken,
  },
})

export const invokeBedrock = async (prompt) => {
  try {
    const modelId = 'amazon.titan-text-express-v1'

    const payload = {
      inputText: prompt,
      textGenerationConfig: {
        maxTokenCount: 1000,
        stopSequences: [],
        temperature: 0.7,
        topP: 1,
      },
    }

    const command = new InvokeModelCommand({
      modelId: modelId,
      contentType: 'application/json',
      accept: 'application/json',
      body: JSON.stringify(payload),
    })

    const response = await client.send(command)
    const decodedResponseBody = new TextDecoder().decode(response.body)
    const responseBody = JSON.parse(decodedResponseBody)

    return responseBody.results[0].outputText
  } catch (error) {
    console.error('Error invocando Bedrock:', error)
    throw error
  }
}
