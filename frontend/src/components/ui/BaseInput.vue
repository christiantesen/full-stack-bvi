<script setup lang="ts">
defineProps<{
  modelValue: string | number
  label?: string
  type?: string
  error?: string
  placeholder?: string
}>();

defineEmits<{
  (e: 'update:modelValue', value: string): void
}>();
</script>

<template>
  <div class="base-input">
    <label v-if="label">{{ label }}</label>
    <input
      :value="modelValue"
      :type="type || 'text'"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="error" class="error">{{ error }}</span>
  </div>
</template>

<style scoped lang="scss">
.base-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  label {
    font-size: 0.875rem;
    color: var(--secondary-color);
  }

  input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;

    &:focus {
      outline: none;
      border-color: var(--primary-color);
    }
  }

  .error {
    color: #dc3545;
    font-size: 0.75rem;
  }
}
</style>