import { useNotification } from '../composables/useNotification';
import { useAuthStore } from '../stores/auth';

interface ApiError {
  response?: {
    data?: {
      message?: string;
    };
    status?: number;
  };
  message?: string;
}

export function handleError(error: ApiError) {
  const { show } = useNotification();
  const message = error.response?.data?.message || error.message || 'An unexpected error occurred';
  
  show(message, 'error');
  
  if (error.response?.status === 401) {
    // Handle unauthorized access
    const authStore = useAuthStore();
    authStore.logout();
  }
  
  return Promise.reject(error);
}