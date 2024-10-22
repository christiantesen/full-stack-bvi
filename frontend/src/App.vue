<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <router-view></router-view>
    </main>
  </div>
</template>

<script lang="ts" setup>
import Navbar from './components/Navbar.vue';
</script>