import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime'

const HARDCODED_ACCESS_KEY = 'ASIAXGT5W6N7QBNCBBLA'
const HARDCODED_SECRET_KEY = '8jICtoZ80TVsgN42Gw0JQMwmdimyZPhTTtcEUceA'
const HARDCODED_REGION = 'us-east-1'

//El token largo es OBLIGATORIO para claves que empiezan por ASIA...
const HARDCODED_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjECkaCmV1LXNvdXRoLTIiSDBGAiEA20rnOfKsfokiRHDu7xbx9nnkurPBLUvm5H6lQtv4gjcCIQDaR2oDlfPv87MyN5Zf1F0MI9XI2tMI2jiwYlSD9rb6jCqKAwh7EAAaDDQ5NTI1ODYyODk5MSIMwO+V/qWQ/Wn7bWTKKucCitia2DJbulOQb+kiTvfKX1SoQpuKdNR0AFFi8LIOhg0U4hhXzV1FQNUFks/d+1gW8kO49Aif6rmDyw0C5DZJsKQm+CpdSulTUycSvWEm4ujJxcXj7U9pjK1ew4GEzRUjVlFAigwLfWy2V4uQs3bBrc+2GjLrPMs5H0XvJmA/ayO/5bLoyB7zmgrEmSO3QGyaz1UwKnK0gd/kwnVL1CNEoqTHPXzu1gvkdpbDGBJFvR/rR2emDiOoQcGqbgnKSo26/jLpAT1wIHusgXjERaoTF3cLghxEGjPGmdyTcbjuTZsP7K9wQqu24+ssjFAQOfgstMG/en33Qa5gRYAby9vGD/X496IfWsIlQ3BBEhHS3o14wSuvDfpwuPVdafYgTZxTIYJjKbTq+2DZEMtmdJVIGh10mQuNI8lggN3Px4VkLVbkd8l74VKrRchnwO25g41EeYJ+FCxqUakRqoxVFw19tWTxQlw1xV0wsrz6ygY6owHNedYIeQjmTCjLmWaPwF9yiTlTjsALU9ugLb/I+7s9ktkkEO0Y+d7u40yU6g9gmUaWUeBRTQysOm6Kjym1M6QfxCBs0MjlzLDOj4VfQr4ZIEAHEvnnosbUrpkCTjhXVn4LJThSx+76fYR2S55u9uon2Nc8iax+9r0CVXcFbTwNCnupccI7w9Xr3U9pvHEeEKUkuWkKaNNWD9JFfG4+08g6s747'

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
