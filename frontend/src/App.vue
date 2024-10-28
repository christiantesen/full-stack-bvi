<script setup lang="ts">
import NotificationList from '@/components/common/NotificationList.vue';
</script>

<template>
  <div id="app">
    <NotificationList />
    <router-view></router-view>
  </div>
</template>

<style lang="scss">
#app {
  min-height: 100vh;
}
</style>