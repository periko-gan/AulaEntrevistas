/**
 * @file messageProcessor.js
 * @description Utilidades para procesar y formatear mensajes de la IA.
 */

/**
 * @description Procesa un texto de la IA para resaltar palabras clave como "Evalio" y "empezar",
 * eliminando sus caracteres de formato originales (ej. **Evalio** o "empezar").
 * @param {string} content - El texto a procesar.
 * @returns {Array<object>} Un array de objetos, donde cada objeto es una parte del texto con su estilo.
 */
export const processAiMessage = (content) => {
  const parts = [];
  // Regex para encontrar **Evalio** o "empezar", insensible a mayúsculas.
  // Captura la palabra clave dentro de los caracteres de formato.
  const regex = /(\*\*Evalio\*\*|"[Ee]mpezar")/gi;
  const textParts = content.split(regex);

  textParts.forEach(part => {
    if (!part) return; // Ignorar partes vacías

    const lowerPart = part.toLowerCase();
    if (lowerPart.includes('evalio') && part.includes('**')) {
      parts.push({ text: 'Evalio', style: 'fw-bold' });
    } else if (lowerPart.includes('empezar') && part.includes('"')) {
      parts.push({ text: 'empezar', style: 'fw-bold' });
    } else {
      parts.push({ text: part, style: '' });
    }
  });
  return parts;
};
