<script setup lang="ts">
// Default layout component
</script>

<template>
  <div class="default-layout">
    <header>
      <!-- Add your header content -->
    </header>
    
    <main>
      <router-view></router-view>
    </main>

    <footer>
      <!-- Add your footer content -->
    </footer>
  </div>
</template>

<style scoped lang="scss">
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}</style>