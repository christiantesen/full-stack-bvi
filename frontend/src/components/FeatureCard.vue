<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ title }}</h3>
    <p class="text-gray-600">{{ description }}</p>
  </div>
</template>

<script lang="ts" setup>
defineProps<{
  title: string;
  description: string;
}>();
</script>