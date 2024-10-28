<script setup lang="ts">
import { useNotification } from '@/composables/useNotification';

const { notifications, remove } = useNotification();
</script>

<template>
  <div class="notification-list">
    <transition-group name="notification">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="['notification', notification.type]"
        @click="remove(notification.id)"
      >
        {{ notification.message }}
      </div>
    </transition-group>
  </div>
</template>

<style scoped lang="scss">
.notification-list {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.notification {
  padding: 1rem;
  border-radius: 4px;
  cursor: pointer;
  min-width: 300px;
  
  &.success { background: #28a745; color: white; }
  &.error { background: #dc3545; color: white; }
  &.warning { background: #ffc107; color: black; }
  &.info { background: #17a2b8; color: white; }
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>