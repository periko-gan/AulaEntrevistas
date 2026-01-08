<script setup>
defineProps({
  // El valor seleccionado (para v-model)
  modelValue: {
    type: [String, Number],
    default: ''
  },
  // Array de objetos JSON
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  // Nombre de la propiedad a mostrar como texto (ej: 'nombre')
  labelKey: {
    type: String,
    default: 'nombre'
  },
  // Nombre de la propiedad a usar como valor (ej: 'codigo')
  valueKey: {
    type: String,
    default: 'id'
  },
  // Texto del placeholder (opción por defecto deshabilitada)
  placeholder: {
    type: String,
    default: 'Selecciona una opción'
  }
});

const emit = defineEmits(['update:modelValue']);

const handleChange = (event) => {
  emit('update:modelValue', event.target.value);
};
</script>

<template>
  <select
    class="form-select"
    :value="modelValue"
    @change="handleChange"
  >
    <option value="" disabled selected>{{ placeholder }}</option>
    <option
      v-for="(option, index) in options"
      :key="index"
      :value="option[valueKey]"
    >
      {{ option[labelKey] }}
    </option>
  </select>
</template>
