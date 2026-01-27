/**
 * @file useConversationInterface.js
 * @description Composable para gestionar la lógica de la interfaz de una conversación, como la inicialización de tooltips.
 */
import { ref, watch, onBeforeUnmount, nextTick } from 'vue';
import { Tooltip } from 'bootstrap';

export function useConversationInterface() {
  // --- Lógica de Tooltips ---
  const renameButtonRef = ref(null);
  const downloadButtonRef = ref(null);
  const deleteButtonRef = ref(null);

  const initializeTooltip = (elementRef) => {
    if (elementRef.value) {
      nextTick(() => {
        const existingTooltip = Tooltip.getInstance(elementRef.value);
        if (existingTooltip) existingTooltip.dispose();
        new Tooltip(elementRef.value);
      });
    }
  };

  const disposeTooltip = (elementRef) => {
    if (elementRef.value) {
      const existingTooltip = Tooltip.getInstance(elementRef.value);
      if (existingTooltip) existingTooltip.dispose();
    }
  };

  watch(renameButtonRef, (newVal) => newVal ? initializeTooltip(renameButtonRef) : disposeTooltip(renameButtonRef));
  watch(downloadButtonRef, (newVal) => newVal ? initializeTooltip(downloadButtonRef) : disposeTooltip(downloadButtonRef));
  watch(deleteButtonRef, (newVal) => newVal ? initializeTooltip(deleteButtonRef) : disposeTooltip(deleteButtonRef));

  onBeforeUnmount(() => {
    disposeTooltip(renameButtonRef);
    disposeTooltip(downloadButtonRef);
    disposeTooltip(deleteButtonRef);
  });

  return {
    renameButtonRef,
    downloadButtonRef,
    deleteButtonRef,
  };
}
