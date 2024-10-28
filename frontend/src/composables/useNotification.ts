import { ref } from 'vue';

interface Notification {
  id: number;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  timeout?: number;
}

const notifications = ref<Notification[]>([]);

export function useNotification() {
  const show = (message: string, type: Notification['type'] = 'info', timeout = 3000) => {
    const id = Date.now();
    notifications.value.push({ id, message, type });

    if (timeout) {
      setTimeout(() => {
        remove(id);
      }, timeout);
    }
  };

  const remove = (id: number) => {
    notifications.value = notifications.value.filter(n => n.id !== id);
  };

  return {
    notifications,
    show,
    remove
  };
}