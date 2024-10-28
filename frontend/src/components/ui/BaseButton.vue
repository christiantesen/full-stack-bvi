<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}>();
</script>

<template>
  <button
    :class="[
      'base-button',
      `variant-${variant || 'primary'}`,
      `size-${size || 'md'}`
    ]"
    :disabled="disabled"
  >
    <slot></slot>
  </button>
</template>

<style scoped lang="scss">
.base-button {
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &.variant-primary {
    background: var(--primary-color);
    color: white;
  }

  &.variant-secondary {
    background: var(--secondary-color);
    color: white;
  }

  &.variant-danger {
    background: #dc3545;
    color: white;
  }

  &.size-sm { padding: 0.25rem 0.5rem; font-size: 0.875rem; }
  &.size-md { padding: 0.5rem 1rem; font-size: 1rem; }
  &.size-lg { padding: 0.75rem 1.5rem; font-size: 1.125rem; }
}
</style>