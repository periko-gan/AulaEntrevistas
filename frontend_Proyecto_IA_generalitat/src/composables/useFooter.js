import { computed } from 'vue';

export function useFooter() {
  // Año actual dinámico
  const currentYear = computed(() => new Date().getFullYear());

  return {
    currentYear
  };
}
