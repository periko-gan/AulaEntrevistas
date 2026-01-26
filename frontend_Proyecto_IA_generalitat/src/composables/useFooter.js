import { computed } from 'vue';

/**
 * @description Composable para gestionar la lógica del pie de página (Footer).
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useFooter() {
  /**
   * @description Propiedad computada que devuelve el año actual.
   * @type {number}
   */
  const currentYear = computed(() => new Date().getFullYear());

  return {
    currentYear
  };
}
