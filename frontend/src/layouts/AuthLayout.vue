<script setup lang="ts">
// Auth layout component
</script>

<template>
  <div class="auth-layout">
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped lang="scss">
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--secondary-color);
}</style>